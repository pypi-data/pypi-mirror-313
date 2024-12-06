import os
import tempfile
import json
import boto3
import rx
import requests
import sys
import sqlite3
import threading

from io import BytesIO
from typing import IO
from typing import Tuple, Optional

from rx import operators as ops
from rx.disposable import Disposable

from .event_receiver import EventReceiver

from .platform_specific.mqtt_base_interface import MqttBaseInterface
from .platform_specific.paho_mqtt_client import PahoMqttClient
from .platform_specific.greengrass_client import GreengrassClient
from .service.api_service import ApiService
from .service.config import Config
from .model.iot_credentials import IotCredentials
from .model.thing_config import ThingConfig
from .model.sensor_value import SensorValue
from .model.error_log import ErrorLog
from .model.log_base import LogBase

amazon_root_ca = """
-----BEGIN CERTIFICATE-----
MIIDQTCCAimgAwIBAgITBmyfz5m/jAo54vB4ikPmljZbyjANBgkqhkiG9w0BAQsF
ADA5MQswCQYDVQQGEwJVUzEPMA0GA1UEChMGQW1hem9uMRkwFwYDVQQDExBBbWF6
b24gUm9vdCBDQSAxMB4XDTE1MDUyNjAwMDAwMFoXDTM4MDExNzAwMDAwMFowOTEL
MAkGA1UEBhMCVVMxDzANBgNVBAoTBkFtYXpvbjEZMBcGA1UEAxMQQW1hem9uIFJv
b3QgQ0EgMTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALJ4gHHKeNXj
ca9HgFB0fW7Y14h29Jlo91ghYPl0hAEvrAIthtOgQ3pOsqTQNroBvo3bSMgHFzZM
9O6II8c+6zf1tRn4SWiw3te5djgdYZ6k/oI2peVKVuRF4fn9tBb6dNqcmzU5L/qw
IFAGbHrQgLKm+a/sRxmPUDgH3KKHOVj4utWp+UhnMJbulHheb4mjUcAwhmahRWa6
VOujw5H5SNz/0egwLX0tdHA114gk957EWW67c4cX8jJGKLhD+rcdqsq08p8kDi1L
93FcXmn/6pUCyziKrlA4b9v7LWIbxcceVOF34GfID5yHI9Y/QCB/IIDEgEw+OyQm
jgSubJrIqg0CAwEAAaNCMEAwDwYDVR0TAQH/BAUwAwEB/zAOBgNVHQ8BAf8EBAMC
AYYwHQYDVR0OBBYEFIQYzIU07LwMlJQuCFmcx7IQTgoIMA0GCSqGSIb3DQEBCwUA
A4IBAQCY8jdaQZChGsV2USggNiMOruYou6r4lK5IpDB/G/wkjUu0yKGX9rbxenDI
U5PMCCjjmCXPI6T53iHTfIUJrU6adTrCC2qJeHZERxhlbI1Bjjt/msv0tadQ1wUs
N+gDS63pYaACbvXy8MWy7Vu33PqUXHeeE6V/Uq2V8viTO96LXFvKWlJbYK8U90vv
o/ufQJVtMVT8QtPHRh8jrdkPSHCa2XV4cdFyQzR1bldZwgJcJmApzyMZFo6IQ6XU
5MsI+yMRQ+hDKXJioaldXgjUkK642M4UwtBV8ob2xJNDd2ZhwLnoQdeXeGADbkpy
rqXRfboQnoZsG4q5WTP468SQvvG5
-----END CERTIFICATE-----
"""


class IotAccessControl:
    def __init__(self, region="ap-northeast-1") -> None:
        thing_name = certificate = private_key = mqtt_host = None
        result = self.read_certificate_files()
        if result:
            thing_name, certificate, private_key, mqtt_host = result

        if all([thing_name, certificate, private_key, mqtt_host]):
            self.thing_name = thing_name
            self._certificate = certificate
            self._private_key = private_key
            self._mqtt_host = mqtt_host
        else:
            self.thing_name = os.getenv("AWS_IOT_THING_NAME")

        if self.thing_name is None:
            raise EnvironmentError("Cannot get thing name from environment")

        self.event_receiver: EventReceiver = EventReceiver(None)

        self._mqtt_client: MqttBaseInterface
        self._default_timeout = 5
        self._region = region
        self._api_service = ApiService()
        self._app_config = Config()
        self._aws_iot_core_client: any
        self._auto_refresh_iot_client: Disposable = None
        self._auto_reconnect: Disposable = None
        self._long_refresh_interval = 3000  # 50 minute
        self._short_refresh_interval = 60  # 1 minute
        self._config_file_path = "./thingConfig.json"

        # Initialize SQLite database for offline mode
        self._db_lock = threading.Lock()
        conn = sqlite3.connect('offline_data.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS data (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            topic TEXT,
                            payload TEXT,
                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                        )''')
        conn.commit()
        conn.close()

        self._auto_resend_offline_data = (
            rx.interval(60)
            .pipe(ops.do_action(lambda i: self._resend_data()))
            .subscribe()
        )

    def connect_to_iot_core_with_offline_mode_support(self) -> None:
        isConnectSucceed = self.connect_to_iot_core()
        if not isConnectSucceed:
            print("Start auto reconnect")
            self._auto_reconnect = (
                rx.interval(10)
                .pipe(ops.do_action(lambda i: self.connect_to_iot_core()))
                .subscribe()
            )

    def connect_to_iot_core(self) -> None:
        try:
            if self._auto_reconnect:
                print("Try auto reconnect")

            # Load environment variables
            ggc_version = os.getenv("GGC_VERSION")

            dev_access_key = os.getenv("DEV_ACCESS_KEY")
            dev_seccurity_key = os.getenv("DEV_SECURITY_KEY")

            # Check if running in Greengrass environment
            if ggc_version is not None:
                self._mqtt_client = self._create_greengrass_client()

            elif all([dev_access_key, dev_seccurity_key]):
                self._mqtt_client = self._create_dev_client(
                    dev_access_key, dev_seccurity_key
                )
            elif all([self._certificate, self._private_key]):
                self._mqtt_client = self._create_standard_client(
                    self._certificate, self._private_key, self._mqtt_host
                )
            else:
                raise EnvironmentError(
                    "No credentials detected, cannot connect to KASO IoT platform"
                )

            self._mqtt_client.connect()

            # initial a iot client of aws sdk from temp credentials
            self._init_publish_client()

            # Refresh the temp iot credentios every 50 minutes
            if not self._auto_refresh_iot_client is None:
                self._auto_refresh_iot_client = (
                    rx.interval(self._long_refresh_interval)
                    .pipe(ops.do_action(lambda i: self._init_publish_client()))
                    .subscribe()
                )

            self.event_receiver.init(self._mqtt_client)

            if self._auto_reconnect != None:
                print("Stop auto reconnect")
                self._auto_reconnect.dispose()
                self._auto_reconnect = None

            return True

        except Exception as e:
            print(e, file=sys.stderr)
            return False

    def publish_sensor_value(self, sensor_value: SensorValue) -> bool:
        if not sensor_value.is_valid_package():
            print("Invalid sensor value pacakge", file=sys.stderr)
            return False

        topic = self._app_config.data_publish_topic
        payload = json.dumps(sensor_value.to_dict())
        self.mqtt_publish(topic=topic, payload=payload)

    def publish_error_log(self, error_log: ErrorLog):
        if not error_log.is_valid_package():
            print("Invalid error log pacakge", file=sys.stderr)
            return False

        topic = self._app_config.log_publish_topic
        payload = json.dumps(error_log.to_dict())
        self.mqtt_publish(topic=topic, payload=payload)

    def publish_system_log(self, sys_log: LogBase):
        if not sys_log.is_valid_package():
            print("Invalid log pacakge", file=sys.stderr)
            return False

        topic = self._app_config.log_publish_topic
        payload = json.dumps(sys_log.to_dict())
        self.mqtt_publish(topic=topic, payload=payload)

    def mqtt_publish(self, topic: str, payload: str):
        try:
            res = self._aws_iot_core_client.publish(
                topic=topic, payload=payload, qos=1)
            return res
        except Exception as e:
            print("Failed to publish data save the data into local storage")
            self._queueing_mqtt_message(topic=topic, payload=payload)

    def get_thing_config(self) -> ThingConfig:
        try:
            response = self._api_service.get_thing_config_url(
                self._mqtt_client)
            config_file_url = response["url"]

            # Download the JSON file from the URL
            response = requests.get(config_file_url)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            # Convert the downloaded JSON file content to a dictionary
            config_data = response.json()
            thing_config = ThingConfig(config_data)

            self.event_receiver.save_thing_config_to_local(thing_config)

            return thing_config
        except Exception as e:
            print(
                f"Failed to download or parse the JSON file: {e}", file=sys.stderr)

            thing_config = self.read_thing_config_from_local()
            return thing_config

    def upload_file_from_file_path(self, local_file_path: str, path_in_bucket: str):
        response = self._api_service.get_s3_presigned_url(
            self._mqtt_client, path_in_bucket, "putObject"
        )

        with open(local_file_path, "rb") as f:
            headers = {"Content-Type": "application/octet-stream"}
            response = requests.put(response["url"], data=f, headers=headers)
            return response

    def upload_file_from_file_file_buffer(
        self, file_buffer: IO[bytes], path_in_bucket: str
    ):
        response = self._api_service.get_s3_presigned_url(
            self._mqtt_client, path_in_bucket, "putObject"
        )

        headers = {"Content-Type": "application/octet-stream"}
        response = requests.put(
            response["url"], data=file_buffer, headers=headers)
        return response

    def download_file_to_local_file_path(
        self, local_file_path: str, path_in_bucket: str
    ):
        response = self._api_service.get_s3_presigned_url(
            self._mqtt_client, path_in_bucket, "getObject"
        )
        # Send a GET request to the URL
        response = requests.get(response["url"], stream=True)

        # Check if the request was successful
        if response.status_code == 200:
            # Open a local file with write-binary mode
            with open(local_file_path, "wb") as f:
                # Write the contents of the response to the file
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(
                f"File downloaded successfully and saved as {local_file_path}")
        else:
            print(
                f"Failed to download file. Status code: {response.status_code}")

    def download_file_as_file_buffer(self, path_in_bucket: str) -> BytesIO:
        response = self._api_service.get_s3_presigned_url(
            self._mqtt_client, path_in_bucket, "getObject"
        )
        # Send a GET request to the URL
        response = requests.get(response["url"], stream=True)
        # Check if the request was successful
        if response.status_code == 200:
            # Create a BytesIO object from the binary response content
            file_buffer = BytesIO(response.content)
            return file_buffer
        else:
            print(
                f"Failed to download file. Status code: {response.status_code}")
            return None

    def read_certificate_files(
        self, directory: str = "./certificate/"
    ) -> Optional[Tuple[str, str, str, str]]:
        if not os.path.exists(directory):
            print(f"The directory {directory} does not exist.")
            return None

        # List all files in the directory
        files = [
            f
            for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, f))
        ]

        if not files:
            print("No files found in the directory.")
            return None

        thingName = certificate = private_key = data_endpoint = None

        for file_name in files:
            file_path = os.path.join(directory, file_name)

            # Read private key for mqtt connection
            if file_name.endswith("--private.pem.key"):
                thingName = file_name.rsplit("--", 1)[0]
                with open(file_path, "r") as file:
                    private_key = file.read()
            # Read certificate for mqtt connection
            elif file_name.endswith("-certificate.pem.crt"):
                thingName = file_name.rsplit("-", 1)[0]
                os.environ["AWS_IOT_THING_NAME"] = thingName
                with open(file_path, "r") as file:
                    certificate = file.read()

            # Read mqtt endpoint info from mqtt connection
            elif file_name == "endpointInfo.txt":
                with open(file_path, "r") as file:
                    for line in file:
                        if line.startswith("DataATS:"):
                            data_endpoint = line.split("DataATS:")[1].strip()

            # Setup applicatioon name and environment
            elif file_name == "stackInfo.txt":
                with open(file_path, "r") as file:
                    for line in file:
                        if line.startswith("ApplicationName:"):
                            application_name = line.split(
                                "ApplicationName:")[1].strip()
                            os.environ["APPLICATION_NAME"] = application_name

                        elif line.startswith("Environment:"):
                            environment = line.split("Environment:")[1].strip()
                            os.environ["Environment"] = environment

        if thingName and certificate and private_key and data_endpoint:
            return thingName, certificate, private_key, data_endpoint
        else:
            return None

    def read_thing_config_from_local(self) -> ThingConfig:
        if os.path.exists(self._config_file_path):
            with open(self._config_file_path, 'r') as file:
                config_data = json.load(file)
                return ThingConfig(config_data)
        else:
            return ThingConfig()

    def _queueing_mqtt_message(self, topic: str, payload: str):
        with self._db_lock:
            conn = sqlite3.connect('offline_data.db')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO data (topic, payload) VALUES (?, ?)", (topic, payload))
            conn.commit()
            conn.close()

    def _resend_data(self):
        with self._db_lock:
            conn = sqlite3.connect('offline_data.db')
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, topic, payload FROM data ORDER BY timestamp ASC")
            rows = cursor.fetchall()
            if not rows:
                return

            print("Try resend offline data")
            for row in rows:
                try:
                    topic = row[1]
                    payload = row[2]
                    res = self._aws_iot_core_client.publish(
                        topic=topic, payload=payload, qos=1)
                    cursor.execute("DELETE FROM data WHERE id=?", (row[0],))
                    conn.commit()
                except Exception as e:
                    print(f"Failed to resend data: {e}")
                    break

    def _create_greengrass_client(self) -> MqttBaseInterface:
        mqtt_client = GreengrassClient()
        return mqtt_client

    def _create_dev_client(self, access_key, secret_key) -> MqttBaseInterface:
        app_name = os.getenv("APPLICATION_NAME")
        env = os.getenv("ENVIRONMENT")

        session = boto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=self._region,
        )

        # Get iot endpint
        iot_client = session.client("iot")
        endpoint_response = iot_client.describe_endpoint(
            endpointType="iot:Data-ATS")
        mqtt_host = endpoint_response["endpointAddress"]

        # Directly Get credentials from DynamoDB
        thing_name = os.getenv("AWS_IOT_THING_NAME")
        dynamodb = session.client("dynamodb")
        table_name = f"{app_name}IotCoreAccessKey_{env}"
        partition_key_name = "thingName"
        partition_key_value = thing_name

        response = dynamodb.query(
            TableName=table_name,
            KeyConditionExpression=f"{partition_key_name} = :v",
            ExpressionAttributeValues={":v": {"S": partition_key_value}},
        )
        item = response.get("Items", [None])[0]

        if item is None:
            raise Exception(f"thingName:{thing_name} not found from db")

        target_item = self._dynamodb_to_dict(item)

        certificate = target_item["certificatePem"]
        private_key = target_item["privateKey"]

        mqtt_client = self._create_standard_client(
            certificate, private_key, mqtt_host)

        return mqtt_client

    def _create_standard_client(
        self, certificate: str, private_key: str, mqtt_host: str
    ) -> MqttBaseInterface:
        ca_file = self._write_to_temp_file(amazon_root_ca, "ca.pem")
        cert_file = self._write_to_temp_file(certificate, "certificate.pem")
        key_file = self._write_to_temp_file(private_key, "private_key.pem")

        mqtt_client = PahoMqttClient(
            self.thing_name,
            ca_file.name,
            cert_file.name,
            key_file.name,
            mqtt_host,
            self._default_timeout,
        )
        return mqtt_client

    def _init_publish_client(self):
        try:
            print("_init_publish_client")
            response = self._api_service.get_iot_credentials(self._mqtt_client)
            iot_credentials = IotCredentials(response)

            if not iot_credentials.is_valid():
                raise Exception("Cannot get iot credentials from iot api")

            self.iot_credentials = iot_credentials

            session = boto3.Session(
                aws_access_key_id=iot_credentials.access_key_id,
                aws_secret_access_key=iot_credentials.secret_access_key,
                aws_session_token=iot_credentials.session_token,
                region_name=self._region,
            )

            # Create an IoT Data Plane client
            client = session.client("iot-data")
            self._aws_iot_core_client = client

            if not self._auto_refresh_iot_client is None:
                self._auto_refresh_iot_client.dispose()

            self._auto_refresh_iot_client = (
                rx.interval(self._long_refresh_interval)
                .pipe(ops.do_action(lambda i: self._init_publish_client()))
                .subscribe()
            )

        except Exception as e:
            print(
                "Failed to initial publish client, maybe becaue the connection is droped", file=sys.stderr)
            print(e, file=sys.stderr)
            self._auto_refresh_iot_client.dispose()
            self._auto_refresh_iot_client = (
                rx.interval(self._short_refresh_interval)
                .pipe(ops.do_action(lambda i: self._init_publish_client()))
                .subscribe()
            )

    def _write_to_temp_file(self, content, filename):
        temp_file = tempfile.NamedTemporaryFile(
            delete=False, mode="w+", suffix=filename
        )
        temp_file.write(content)
        temp_file.flush()
        return temp_file

    def _dynamodb_to_dict(self, item):
        return {k: list(v.values())[0] for k, v in item.items()}

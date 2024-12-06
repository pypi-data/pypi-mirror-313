import threading
import requests
import sys
import json

from rx import operators as ops
from rx.subject import Subject
from concurrent.futures import ThreadPoolExecutor

from .platform_specific.mqtt_base_interface import MqttBaseInterface
from .service.api_service import ApiService
from .service.config import Config

from .model.mqtt_message import MqttMessage
from .model.thing_config import ThingConfig
from .model.command import Command


class EventReceiver:
    def __init__(self, mqtt_client: MqttBaseInterface) -> None:

        self.new_thing_config_subject: Subject[ThingConfig] = Subject()
        self._config_file_path = "./thingConfig.json"

        if mqtt_client is None:
            print("No mqtt client found, initial empty receiver")
            return

        self.init(mqtt_client=mqtt_client)

    def init(self, mqtt_client: MqttBaseInterface):
        self._mqtt_client = mqtt_client
        self._config = Config()
        self._api_service = ApiService()

        self._thing_config_updated_event: threading.Event = threading.Event()
        self._command_receive_event: threading.Event = threading.Event()

        self._arrived_config_message: MqttMessage = None

        self._thread_executor = ThreadPoolExecutor(max_workers=2)
        self._thing_config_updated_event: threading.Event = threading.Event()

        self._arrived_command_message: MqttMessage = None
        self.new_command_subject: Subject[Command] = Subject()

        self._thread_executor.submit(self._handle_new_config_receive)
        self._thread_executor.submit(self._handle_new_command_receive)

        # Subscribe thing config topic and add handler
        self._mqtt_client.subscribe(self._config.config_subscribe_topic)
        self._mqtt_client.message_receive_subject.pipe(
            ops.filter(lambda msg: msg.topic == self._config.config_subscribe_topic)
        ).subscribe(self._triggered_new_config_receive)

        # Subscribe command topic and add handler
        self._mqtt_client.subscribe(self._config.command_subscribe_topic)
        self._mqtt_client.message_receive_subject.pipe(
            ops.filter(lambda msg: msg.topic == self._config.command_subscribe_topic)
        ).subscribe(self._triggered_new_command_receive)

    def _triggered_new_config_receive(self, msg: MqttMessage):
        print("Received new config")
        self._arrived_config_message = msg
        self._thing_config_updated_event.set()

    def _triggered_new_command_receive(self, msg: MqttMessage):
        print("Received new command")
        self._arrived_command_message = msg
        self._command_receive_event.set()

    def _handle_new_config_receive(self):
        while True:
            self._thing_config_updated_event.wait()
            # Download the JSON file from the URL
            try:
                config_path = self._arrived_config_message.message["configPath"]
                response = self._api_service.get_s3_presigned_url(
                    self._mqtt_client, config_path, "getObject"
                )
                response = requests.get(response["url"])
                response.raise_for_status()  # Raises an HTTPError for bad responses
                # Convert the downloaded JSON file content to a dictionary
                config_data = response.json()
                thing_config = ThingConfig(config_data)
                self.new_thing_config_subject.on_next(thing_config)
                self.save_thing_config_to_local(thing_config=thing_config)

            except requests.RequestException as e:
                print(
                    f"Failed to download or parse the JSON file: {e}", file=sys.stderr
                )
                self._thing_config_updated_event.clear()

            self._thing_config_updated_event.clear()

    def save_thing_config_to_local(self, thing_config: ThingConfig):
        # save the config file for offline usage
        with open(self._config_file_path, 'w') as file:
            json.dump(thing_config.to_dict(), file)
            
    def _handle_new_command_receive(self):
        while True:
            self._command_receive_event.wait()
            # Download the JSON file from the URL
            try:
                command = Command(self._arrived_command_message.message)
                self.new_command_subject.on_next(command)

            except requests.RequestException as e:
                print(
                    f"Failed to download or parse the JSON file: {e}", file=sys.stderr
                )
                self._command_receive_event.clear()

            self._command_receive_event.clear()

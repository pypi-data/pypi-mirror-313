from paho.mqtt import client as mqtt_client
from rx.subject import Subject
from ..model.mqtt_message import MqttMessage
from typing import Union
import threading
import json
import sys
import os
import ssl


class PahoMqttClient:
    def __init__(
        self,
        client_id: str,
        root_ca_path: str,
        certificate_path: str,
        private_key_path: str,
        mqtt_host: str,
        default_timeout: int = 5,
    ) -> None:
        self.is_connected = False
        self.message_receive_subject: Subject[MqttMessage] = Subject()
        self._connected_event = threading.Event()
        self._mqtt_host = mqtt_host
        self._mqtt_port = 8883
        self._default_timeout = default_timeout
        self._mqtt_client = mqtt_client.Client(
            mqtt_client.CallbackAPIVersion.VERSION1, client_id
        )
        self._mqtt_client.on_connect = self._on_connect
        self._mqtt_client.on_message = self._on_message
        self._mqtt_client.on_disconnect = self._on_disconnect

        # List to keep track of subscribed topics
        self._subscribed_topics = []

        # Check if the TLS certificate files exist
        if not os.path.isfile(root_ca_path):
            raise FileNotFoundError(
                f"The root CA file was not found at: {root_ca_path}"
            )
        if not os.path.isfile(certificate_path):
            raise FileNotFoundError(
                f"The certificate file was not found at: {certificate_path}"
            )
        if not os.path.isfile(private_key_path):
            raise FileNotFoundError(
                f"The private key file was not found at: {private_key_path}"
            )

        self._mqtt_client.tls_set(
            ca_certs=root_ca_path,
            certfile=certificate_path,
            keyfile=private_key_path,
            tls_version=ssl.PROTOCOL_TLSv1_2,
        )

    def connect(self):
        self._mqtt_client.connect(self._mqtt_host, self._mqtt_port, 60)
        self._mqtt_client.loop_start()
        res = self._connected_event.wait(self._default_timeout)
        if res == False:
            self._mqtt_client.loop_stop()
            raise TimeoutError(
                "Failed to connect to MQTT broker within the timeout period."
            )

    def publish(self, topic: str, payload: Union[dict, str], qos=1, retain=False)-> bool:
        byte_payload = None
        if isinstance(payload, str):
            byte_payload = payload.encode("utf-8")
        elif isinstance(payload, dict):
            byte_payload = json.dumps(payload)
        else:
            raise TypeError("Unknown payload type for MQTT publish")

        if byte_payload is None:
            print("Payload empty", file=sys.stderr)
            return False

        result = self._mqtt_client.publish(topic, byte_payload, qos, retain)
        
        # Check if the publish was successful
        if result.rc == mqtt_client.MQTT_ERR_SUCCESS:
            return True
        else:
            print(f"Publish failed with return code {result.rc}", file=sys.stderr)
            return False

    def subscribe(self, topic: str) -> bool:
        result = self._mqtt_client.subscribe(topic)
        if result[0] == 0:
            self._subscribed_topics.append(topic)
        return result[0] == 0

    def unsubscribe(self, topic: str) -> bool:
        result = self._mqtt_client.unsubscribe(topic)
        if result[0] == 0:
            self._subscribed_topics.remove(topic)
        return result[0] == 0

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.is_connected = True
            print("Connected successfully.")
            self._connected_event.set()
            # Re-subscribe to all previously subscribed topics
            for topic in self._subscribed_topics:
                self._mqtt_client.subscribe(topic)
                print(f"Re-subscribed to topic: {topic}")
        else:
            print(f"Failed to connect with error code {rc}")

    def _on_message(self, client, userdata, msg):
        print("Message received")
        msg_obj = MqttMessage(msg.topic, msg.payload.decode())
        self.message_receive_subject.on_next(msg_obj)

    def _on_disconnect(self, client, userdata, rc):
        self.is_connected = False
        if rc != 0:
            print("Unexpected disconnection.")

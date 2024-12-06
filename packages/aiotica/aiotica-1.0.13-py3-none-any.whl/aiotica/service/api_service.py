from ..platform_specific.mqtt_base_interface import MqttBaseInterface
from .config import Config
from ..model.mqtt_message import MqttMessage
from rx import operators as ops

import json
import uuid
import threading
import requests


class ApiService:
    _instance = None
    _is_initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ApiService, cls).__new__(cls)
        return cls._instance

    def __init__(self, default_timeout=5) -> None:
        if self._is_initialized:
            return
        # self._api_lock = threading.Lock()
        self._is_initialized = True
        self.default_timeout = default_timeout
        self.config = Config()

    def get_s3_presigned_url(
        self, mqtt_client: MqttBaseInterface, access_path: str, action: str
    ):
        request_body = {
            "accessPath": access_path,
            "action": action,
        }
        response = self.api_call(
            mqtt_client=mqtt_client,
            api_name="getS3PreSignedUrl",
            request_body=request_body,
        )

        return response

    def get_thing_config_url(self, mqtt_client: MqttBaseInterface):
        response = self.api_call(mqtt_client=mqtt_client, api_name="getThincConfig")
        return response

    def get_iot_credentials(self, mqtt_client: MqttBaseInterface):
        response = self.api_call(
            mqtt_client=mqtt_client, api_name="getIoTCoreCredential"
        )

        return response

    def api_call(
        self, mqtt_client: MqttBaseInterface, api_name: str, request_body: dict = None
    ) -> bool:
        request_id = str(uuid.uuid4())[:6]
        if request_body is None:
            request_body = {
                "request_id": request_id,
                "message": "Auto generate by KASO IoT SDK",
            }

        publish_topic = self.config.get_api_request_topic(api_name, request_id)
        subscribe_topic = self.config.get_api_response_topic(api_name, request_id)

        print(f"publish_topic:{publish_topic}")
        print(f"subscribe_topic:{subscribe_topic}")

        response_event = threading.Event()
        response_content = {}

        def handle_response(msg: MqttMessage):
            nonlocal response_content
            print(f"Api service receive response from {msg.topic}")

            if msg.topic == subscribe_topic:
                response_content = msg.message
                response_event.set()

        subscription = mqtt_client.message_receive_subject.pipe(
            ops.filter(lambda msg: msg.topic == subscribe_topic),
            ops.take(1),
        ).subscribe(on_next=handle_response)

        mqtt_client.subscribe(subscribe_topic)
        mqtt_client.publish(publish_topic, request_body)

        # Wait for the response or timeout
        if not response_event.wait(timeout=self.default_timeout):
            raise TimeoutError("Timeout waiting for response")
        subscription.dispose()
        mqtt_client.unsubscribe(subscribe_topic)

        return response_content

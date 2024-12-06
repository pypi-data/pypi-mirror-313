import threading
import json
import sys
import awsiot.greengrasscoreipc.clientv2 as clientV2
from rx.subject import Subject
from ..model.mqtt_message import MqttMessage
from typing import Dict, Union


class GreengrassClient:
    _instance = None
    _is_initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GreengrassClient, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if self._is_initialized:
            return

        self._is_initialized = True
        self.is_connected = False
        self.subscriptions: Dict[str, any] = {}

        self.message_receive_subject: Subject[MqttMessage] = Subject()
        self.connected_event = threading.Event()

        self.ipc_client = clientV2.GreengrassCoreIPCClientV2()

    def connect(self):
        pass  # The ipc clinet auto connect in greengrass

    def publish(self, topic: str, payload: Union[dict, str], qos=0, retain=False) -> bool:
        try:
            payload_bytes = json.dumps(payload).encode("utf-8")
            resp = self.ipc_client.publish_to_iot_core(
                topic_name=topic, qos=str(qos), payload=payload_bytes, retain=retain
            )
            
            if resp and hasattr(resp, 'status') and resp.status == 'SUCCESS':  # Adjust based on actual response object
                return True
            else:
                print(f"Publish failed with response: {resp}", file=sys.stderr)
                return False
            
        except Exception as err:
            print(err, file=sys.stderr)
            if self.ipc_client != None:
                self.ipc_client.close()
            return False

    def subscribe(self, topic: str, qos=0) -> bool:
        if topic in self.subscriptions:
            print(f"Already subscribed to {topic}")
            return False

        response, operation = self.ipc_client.subscribe_to_iot_core(
            topic_name=topic,
            qos=str(qos),
            on_stream_event=self._on_stream_event,
            on_stream_error=self._on_stream_error,
            on_stream_closed=self._on_stream_closed,
        )
        print(f"Subscribed {topic}")
        self.subscriptions[topic] = operation
        return True

    def unsubscribe(self, topic: str) -> bool:
        if topic in self.subscriptions:
            self.subscriptions[topic].close()
            del self.subscriptions[topic]
            print(f"Unsubscribed from {topic}")

    def unsubscribe_from_all(self):
        for topic in list(self.subscriptions.keys()):
            self.unsubscribe(topic)

    def _on_stream_event(self, event):
        try:
            print("Message received from greengrass client")
            topic_name = event.message.topic_name
            message = str(event.message.payload, "utf-8")            
            json_body = json.loads(message)
            mqtt_message = MqttMessage(topic_name, json_body)
            self.message_receive_subject.on_next(mqtt_message)

        except Exception as err:
            print(err, file=sys.stderr)

    def _on_stream_error(self, error):
        print(error, file=sys.stderr)
        return True  # Return True to close stream, False to keep stream open.

    def _on_stream_closed(self):
        print("Mqtt stream closed")

from paho.mqtt import client as mqtt_client
from rx.subject import Subject
from ..model.mqtt_message import MqttMessage
import threading
import json
import sys


class MqttBaseInterface:
    def __init__(self) -> None:
        self.is_connected = False
        self.message_receive_subject: Subject[MqttMessage] = Subject()

    def connect(self):
        pass

    def publish(self, topic: str, payload: dict, qos=0, retain=False) -> bool:
        pass

    def subscribe(self, topic: str) -> bool:
        return True

    def unsubscribe(self, topic: str) -> bool:
        return True

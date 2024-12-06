import json
import sys
from typing import Union

class MqttMessage:
    def __init__(self, topic: str, message:Union[dict, str]) -> None:
        self.topic: str = topic

        # Initialize self.message as an empty dict in case JSON decoding fails
        self.message: dict = {}

        # Check if the message is a string and attempt to parse it as JSON.
        if isinstance(message, str):
            try:
                message = json.loads(message)  # Attempt to parse the JSON string.
                self.message = message
            except json.JSONDecodeError:
                print(
                    f"Error decoding JSON string from topic {self.topic}. Using an empty dictionary as fallback.",
                    file=sys.stderr,
                )
        elif isinstance(message, dict):
            self.message = message
        else:
            raise TypeError("Message must be either a 'dict' or 'str' type.")

import json
import sys

from dataclasses import dataclass
from .log_base import LogBase


@dataclass
class ErrorLogBody:
    sensing_item: str = None
    error_value: str = None


class ErrorLog(LogBase):
    def __init__(self, json_payload=None):
        super().__init__(json_payload)
        self.log_body = ErrorLogBody()  # Override with structured log body

        if isinstance(json_payload, str):
            try:
                data = json.loads(json_payload)
                if "logBody" in data:
                    self.log_body.key = data["logBody"].get("key")
            except json.JSONDecodeError:
                print("Failed to decode JSON", file=sys.stderr)

    def to_dict(self):
        # Override to_dict to adapt to the new log_body structure
        return {
            "vendor": self.vendor,
            "model": self.model,
            "endpointId": self.endpoint_id,
            "date": self.date,
            "logBody": {
                "sensingItem": self.log_body.sensing_item,
                "errorValue": self.log_body.error_value,
            },
        }

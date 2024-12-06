import json
import sys
from datetime import datetime, timezone


class LogBase:
    def __init__(self, json_payload=None):

        current_time = datetime.now(timezone.utc)
        formatted_time = current_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        if json_payload is None:
            self.vendor = None
            self.model = None
            self.endpoint_id = None
            self.date = formatted_time
            self.log_body = None
            return

        # Parse the JSON payload if it's a string
        if isinstance(json_payload, str):
            try:
                json_payload = json.loads(json_payload)
            except json.JSONDecodeError:
                self.is_valid_package = False
                return  # Early exit if JSON is invalid

        # Set attributes based on the JSON keys
        self.vendor = json_payload.get("vendor")
        self.model = json_payload.get("model")
        self.endpoint_id = json_payload.get("endpointId")
        self.date = json_payload.get("date")
        self.log_body = json_payload.get("logBody")
        if self.is_valid_package() == False:
            print(
                f"Failed to initial SensorValueBase() {json_payload}", file=sys.stderr
            )

    def is_valid_package(self):
        return all(
            [self.vendor, self.model, self.endpoint_id, self.date, self.log_body]
        )

    def to_dict(self):
        if self.is_valid_package() == False:
            print("Invalid log package", file=sys.stderr)

        return {
            "vendor": self.vendor,
            "model": self.model,
            "endpointId": self.endpoint_id,
            "date": self.date,
            "logBody": self.log_body,
        }

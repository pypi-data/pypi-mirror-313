import json
import os
from typing import List, Dict, Any


class EndpointConfig:
    def __init__(self, vendor, model, endpoint_id, status, interval, setting):
        self.vendor: str = vendor
        self.model: str = model
        self.endpoint_id: str = endpoint_id
        self.status: bool = status
        self.interval: int = interval
        self.setting: Dict[str, Any] = setting

    def get_setting_value(self, key):
        """
        Safely retrieves a setting value using a key, returning None if the key doesn't exist.

        Args:
        key (str): The key for the setting item.

        Returns:
        Value or None: Returns the value if the key exists, None otherwise.
        """
        return self.setting.get(key, None)

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the EndpointConfig instance to a dictionary.

        Returns:
        dict: Dictionary representation of the EndpointConfig instance.
        """
        return {
            "vendor": self.vendor,
            "model": self.model,
            "endpoint_id": self.endpoint_id,
            "status": self.status,
            "interval": self.interval,
            "setting": self.setting,
        }


class ThingConfig:
    def __init__(self, json_payload=None):
        """
        Initializes the ThingConfig object with properties extracted from the JSON payload.

        Args:
        json_payload (dict): Dictionary containing thing configuration details.
        """
        self.endpoint_list: List[EndpointConfig] = []
        if json_payload is None:
            return

        for key in json_payload:
            devices_data = json_payload[key]
            for device_data in devices_data:
                vendor = device_data.get("vendor")
                model = device_data.get("model")
                endpoint_id = device_data.get("endpointId")
                status = device_data.get("status")
                interval = device_data.get("interval", 0)
                setting = device_data.get("setting", {})
                device_config = EndpointConfig(
                    vendor, model, endpoint_id, status, interval, setting
                )
                self.endpoint_list.append(device_config)

    def find_device_by_vendor_and_model(
        self, vendor: str, model: str, endpoint_id: str = None
    ) -> List[EndpointConfig]:
        endpoint_list: List[EndpointConfig] = []

        if endpoint_id is not None:
            for device in self.endpoint_list:
                if (
                    device.vendor == vendor
                    and device.model == model
                    and device.endpoint_id == endpoint_id
                ):
                    endpoint_list.append(device)
                    return endpoint_list

        else:
            for device in self.endpoint_list:
                if device.vendor == vendor and device.model == model:
                    endpoint_list.append(device)

        return endpoint_list

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the ThingConfig instance to a dictionary.

        Returns:
        dict: Dictionary representation of the ThingConfig instance.
        """
        return {"endpoints": [endpoint.to_dict() for endpoint in self.endpoint_list]}

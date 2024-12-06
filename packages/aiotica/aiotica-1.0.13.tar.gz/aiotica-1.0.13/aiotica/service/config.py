import os


class Config:
    _instance = None
    _is_initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._is_initialized:
            return

        self._is_initialized = True
        self.application_name = os.getenv("APPLICATION_NAME", None)
        self.environment = os.getenv("ENVIRONMENT", None)
        self.thing_name = os.getenv("AWS_IOT_THING_NAME", None)

        if (
            self.application_name is None
            or self.environment is None
            or self.thing_name is None
        ):
            raise Exception(
                "Setup APPLICATION_NAME, ENVIRONMENT and AWS_IOT_THING_NAME to environment virable before you start using KASO SDK"
            )

    @property
    def bucket_name(self) -> str:
        return f"{self.application_name.lower()}-{self.environment.lower()}"

    @property
    def data_publish_topic(self) -> str:
        return f"kaso/{self.application_name.lower()}_{self.environment.lower()}/gateway/{self.thing_name}/data"

    @property
    def log_publish_topic(self) -> str:
        return f"kaso/{self.application_name.lower()}_{self.environment.lower()}/gateway/{self.thing_name}/log"

    @property
    def command_publish_topic(self) -> str:
        return f"kaso/{self.application_name.lower()}_{self.environment.lower()}/gateway/{self.thing_name}/command"

    @property
    def status_publish_topic(self) -> str:
        return f"kaso/{self.application_name.lower()}_{self.environment.lower()}/gateway/{self.thing_name}/status"

    @property
    def status_subscribe_topic(self) -> str:
        return f"kaso/{self.application_name.lower()}_{self.environment.lower()}/ruleEngine/{self.thing_name}/status"

    @property
    def config_subscribe_topic(self) -> str:
        return f"kaso/{self.application_name.lower()}_{self.environment.lower()}/ruleEngine/{self.thing_name}/config"

    @property
    def command_subscribe_topic(self) -> str:
        return f"kaso/{self.application_name.lower()}_{self.environment.lower()}/ruleEngine/{self.thing_name}/command"

    @property
    def command_from_app_subscribe_topic(self) -> str:
        return f"kaso/{self.application_name.lower()}_{self.environment.lower()}/app/{self.thing_name}/command"

    def get_latest_firmware_version_subscribe_topic(self, app_name) -> str:
        return f"kaso/{self.application_name.lower()}_{self.environment.lower()}/ruleEngine/latestFirmwareVersion/{app_name}"

    def get_api_request_topic(self, api_name, request_id) -> str:
        return f"kaso/{self.application_name.lower()}_{self.environment.lower()}/gateway/{self.thing_name}/{api_name}/request/{request_id}"

    def get_api_response_topic(self, api_name, request_id) -> str:
        return f"kaso/{self.application_name.lower()}_{self.environment.lower()}/microservice/{self.thing_name}/{api_name}/response/{request_id}"

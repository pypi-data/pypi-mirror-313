import sys


class IotCredentials:
    def __init__(self, json_payload: dict):
        if json_payload is None:
            self.access_key_id: str = None
            self.secret_access_key: str = None
            self.session_token: str = None
            self.expiration: str = None
            self.connectionId: str = None
            self.policy: dict = None
            return

        self.access_key_id: str = json_payload.get("accessKeyId", None)
        self.secret_access_key: str = json_payload.get("secretAccessKey", None)
        self.session_token: str = json_payload.get("sessionToken", None)
        self.expiration: str = json_payload.get("expiration", None)
        self.connectionId: str = json_payload.get("connectionId", None)
        self.policy: dict = json_payload.get("policy", None)

        if not self.is_valid():
            print("Invalid credential", file=sys.stderr)

    def is_valid(self):
        # return all([self.access_key_id, self.secret_access_key, self.session_token, self.expiration, self.connectionId, self.policy])
        return all([self.access_key_id, self.secret_access_key, self.session_token, self.expiration, self.connectionId])

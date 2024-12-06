import grpc
from viaduct.dao.v1 import dao_pb2, dao_pb2_grpc
import httpx
import time
from threading import Lock
import base64
import json
from typing import Optional

import logging

# Enable gRPC debug logging
grpc_logger = logging.getLogger("grpc")
grpc_logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
grpc_logger.addHandler(ch)

DAO_OAUTH_CLIENT_ID = "0oaj1jvtzeldKZ7jw5d7"
DAO_OAUTH_SERVER_URL = "https://viaduct-cloud.okta.com/oauth2/ausitj9diu5UBx4QH5d7"
DAO_OAUTH_TOKEN_URL = f"{DAO_OAUTH_SERVER_URL}/v1/token"
DAO_OAUTH_DEVICE_AUTHORIZATION_URL = f"{DAO_OAUTH_SERVER_URL}/v1/device/authorize"


import os
import json


def is_token_valid(token):
    if not token:
        return False

    buffer_time = 60
    return time.time() + buffer_time < token.get("expires_at", 0)


def load_token(creds_file):
    try:
        with open(creds_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def save_token(token, creds_file):
    os.makedirs(os.path.dirname(creds_file), exist_ok=True)
    with open(creds_file, "w") as f:
        json.dump(token, f)


def get_token_expiration(jwt_access_token):
    """
    get_token_expiration takes a jwt access token, and returns the `exp` field
    """
    payload = jwt_access_token.split(".")[1]
    payload += "=" * ((4 - len(payload) % 4) % 4)
    decoded_payload = base64.b64decode(payload)
    payload_data = json.loads(decoded_payload)
    return payload_data["exp"]


def refresh_token(token, client_id, token_url):
    client = httpx.Client()
    response = client.post(
        token_url,
        data={
            "grant_type": "refresh_token",
            "refresh_token": token["refresh_token"],
            "client_id": client_id,
        },
    )
    response.raise_for_status()
    new_token = response.json()
    new_token["expires_at"] = get_token_expiration(new_token["access_token"])
    return new_token


def authenticate(client_id, token_url, device_authorization_url, scope):
    client = httpx.Client()
    response = client.post(
        device_authorization_url,
        data={"client_id": client_id, "scope": scope},
    )
    response.raise_for_status()
    device_auth_data = response.json()

    verification_uri = device_auth_data["verification_uri"]
    user_code = device_auth_data["user_code"]
    device_code = device_auth_data["device_code"]
    interval = device_auth_data.get("interval", 5)

    print(f"Please visit: {verification_uri}")
    print(f"And enter the code: {user_code}")

    while True:
        try:
            response = client.post(
                token_url,
                data={
                    "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                    "device_code": device_code,
                    "client_id": client_id,
                },
            )
            response.raise_for_status()
            token = response.json()
            token["expires_at"] = get_token_expiration(token["access_token"])
            return token
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 400:
                error = e.response.json().get("error")
                if error == "authorization_pending":
                    time.sleep(interval)
                elif error == "slow_down":
                    interval += 5
                    time.sleep(interval)
                else:
                    raise
            else:
                raise


class DeviceFlowAuth:
    def __init__(self, client_id, token_url, device_authorization_url, scope):
        self.client_id = client_id
        self.token_url = token_url
        self.device_authorization_url = device_authorization_url
        self.scope = scope
        self.lock = Lock()
        self.creds_file = os.path.expanduser("~/.viaduct/dao/_creds.json")

    def get_valid_access_token(self):
        with self.lock:
            token = load_token(self.creds_file)

            if is_token_valid(token):
                return token["access_token"]

            if token and "refresh_token" in token:
                try:
                    new_token = refresh_token(token, self.client_id, self.token_url)
                    save_token(new_token, self.creds_file)
                    return new_token["access_token"]
                except Exception:
                    # If refresh fails, fall through to re-authentication
                    pass

            # If we reach here, we need to re-authenticate
            new_token = authenticate(
                self.client_id,
                self.token_url,
                self.device_authorization_url,
                self.scope,
            )
            save_token(new_token, self.creds_file)
            return new_token["access_token"]


class OAuth2AuthPlugin(grpc.AuthMetadataPlugin):
    def __init__(self):
        self.oauth_manager = DeviceFlowAuth(
            client_id=DAO_OAUTH_CLIENT_ID,
            token_url=DAO_OAUTH_TOKEN_URL,
            device_authorization_url=DAO_OAUTH_DEVICE_AUTHORIZATION_URL,
            scope="offline_access",
        )

        self.org_id = ""
        self.access_token = self.oauth_manager.get_valid_access_token()

    def with_org_id(self, org_id: str) -> None:
        self.org_id = org_id

    def __call__(self, context, callback):
        # Authenticate the user using the device flow
        self.access_token = self.oauth_manager.get_valid_access_token()
        metadata = (
            ("x-org-id", self.org_id),
            ("authorization", f"Bearer {self.access_token}"),
        )
        callback(metadata, None)


class BasicAuthPlugin(grpc.AuthMetadataPlugin):
    def __init__(
        self,
        access_token: Optional[str] = None,
        is_super_admin: bool = True,
    ):
        self.org_id = ""
        self.access_token = access_token if access_token else ""
        self.is_super_admin = is_super_admin

    def with_org_id(self, org_id: str) -> None:
        self.org_id = org_id

    def __call__(self, context, callback):
        # Authenticate the user using the device flow
        metadata = (
            ("x-org-id", self.org_id),
            ("x-super-admin", "true" if self.is_super_admin else "false"),
            ("authorization", f"Bearer {self.access_token}"),
        )
        callback(metadata, None)
        
def get_client(
    server_url: str, org_id: Optional[str] = None, secure: bool = True, auth_plugin=None
) -> dao_pb2_grpc.DaoServiceStub:
    # Create the channel credentials
    if not auth_plugin:
        auth_plugin = OAuth2AuthPlugin()

    if org_id:
        auth_plugin.with_org_id(org_id)

    if not secure:
        channel_credentials = grpc.composite_channel_credentials(
            grpc.local_channel_credentials(),
            grpc.metadata_call_credentials(auth_plugin),
        )
    else:
        channel_credentials = grpc.composite_channel_credentials(
            grpc.ssl_channel_credentials(),
            grpc.metadata_call_credentials(auth_plugin),
        )

    # Create the channel and client stub
    channel = grpc.secure_channel(server_url, channel_credentials)
    return dao_pb2_grpc.DaoServiceStub(channel)


def daoql(c: dao_pb2_grpc.DaoServiceStub, query: str, limit: int = 10, return_debug_info: bool = False):
    rows = []
    debug_info = None
    for response in c.Query(dao_pb2.QueryRequest(daoql=query, limit=limit)):
        if response.HasField("debug_info"):
            debug_info = response.debug_info
        row = {}
        for k, v in response.row.attributes.items():
            of = v.WhichOneof("value")
            if of is None:
                row[k] = None
            elif of == "boolean_value":
                row[k] = v.boolean_value
            elif of == "string_value":
                row[k] = v.string_value
            elif of == "float_value":
                row[k] = v.float_value
            elif of == "timestamp_value":
                row[k] = v.timestamp_value.ToDatetime()
            else:
                raise ValueError(f"Unsupported attribute value {of}")
        rows.append(row)
    return (rows, debug_info) if return_debug_info else rows

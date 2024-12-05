import requests
from time import sleep
from ..datatypes import Method, Params
from typing import Any
import threading
from os import path


DEFAULT_TIMEOUT = 15
DEFAULT_MAX_RETRIES = 5
TOKEN_TMP_FILE = "/tmp/kramerius_token"
TOKEN_CALL = "{KEYCLOAK_HOST}/realms/kramerius/protocol/openid-connect/token"


class KrameriusBaseClient:
    def __init__(
        self,
        host: str,
        keycloak_host: str | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
        username: str | None = None,
        password: str | None = None,
        timeout: int | None = None,
        max_retries: int | None = None,
    ):
        self.base_url = host.strip("/")

        self._keycloak_host = None
        self._get_token_body = None
        if (
            keycloak_host
            and client_id
            and client_secret
            and username
            and password
        ):
            self._keycloak_host = keycloak_host
            self._get_token_body = {
                "client_id": client_id,
                "client_secret": client_secret,
                "username": username,
                "password": password,
                "grant_type": "password",
            }

        self._token = None
        if path.exists(TOKEN_TMP_FILE):
            with open(TOKEN_TMP_FILE, "r") as f:
                self._token = f.read().strip()

        self.lock = threading.Lock()
        self.timeout = timeout or DEFAULT_TIMEOUT
        self.max_retries = max_retries or DEFAULT_MAX_RETRIES

        self.retries = 0

    def _fetch_access_token(self):
        if self._get_token_body is None:
            raise Exception(
                "Authorization parameters are not provided. "
                "Please set them to use admin API."
            )

        response = requests.post(
            TOKEN_CALL.format(KEYCLOAK_HOST=self._keycloak_host),
            data=self._get_token_body,
        )

        if not response.ok:
            raise Exception("Failed to retrieve access token.")

        self._token = response.json().get("access_token")

        with open(TOKEN_TMP_FILE, "w+") as f:
            f.write(self._token)

    def _wait_for_retry(self, response: requests.Response) -> None:
        if self.retries == 5:
            response.raise_for_status()
        self.retries += 1
        sleep(self.timeout * self.retries)

    def _request(
        self,
        method: Method,
        endpoint: str,
        params: Params | None = None,
        data: Any | None = None,
        data_type: str | None = None,
    ):
        url = self.base_url + endpoint
        headers = {} if data_type or self._token else None
        if data_type:
            headers["Content-Type"] = data_type
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"

        response = requests.request(
            method, url, headers=headers, params=params, data=data
        )

        if response.status_code == 401 or (
            response.status_code == 403
            and (
                "user 'not_logged'" in response.json().get("message", "")
                or "not allowed" == response.json().get("message", "")
            )
        ):
            self._fetch_access_token()
            return self._request(method, endpoint, params, data, data_type)

        if not response.ok:
            self._wait_for_retry(response)
            return self._request(method, endpoint, params, data, data_type)

        self.curr_wait = 0
        self.retries = 0
        return response

    def admin_request_response(
        self,
        method: str,
        endpoint: str,
        params: Params | None = None,
        data: Any | None = None,
        data_type: str | None = None,
    ):
        with self.lock:
            return self._request(
                method, f"/api/admin/v7.0/{endpoint}", params, data, data_type
            )

    def admin_request(
        self,
        method: str,
        endpoint: str,
        params: Params | None = None,
        data: Any | None = None,
        data_type: str | None = None,
    ):
        return self.admin_request_response(
            method, endpoint, params, data, data_type
        ).json()

    def client_request_response(
        self,
        method: str,
        endpoint: str,
        params: Params | None = None,
        data: Any | None = None,
        data_type: str | None = None,
    ):
        with self.lock:
            return self._request(
                method, f"/api/client/v7.0/{endpoint}", params, data, data_type
            )

    def client_request(
        self,
        method: str,
        endpoint: str,
        params: Params | None = None,
        data: Any | None = None,
        data_type: str | None = None,
    ):
        return self.client_request_response(
            method, endpoint, params, data, data_type
        ).json()

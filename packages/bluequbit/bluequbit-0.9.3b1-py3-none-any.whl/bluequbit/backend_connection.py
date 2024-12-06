import json
import logging
import os
from pathlib import Path

from .exceptions import AUTH_ERROR_MESSAGE, BQAPIError, BQUnauthorizedAccessError
from .http_utils import request_retriable
from .version import __version__

logger = logging.getLogger("bluequbit-python-sdk")


class BackendConnection:
    def __init__(self, api_token=None):
        super().__init__()
        config_dir = Path.home() / ".config" / "bluequbit"
        config_location = config_dir / "config.json"

        main_endpoint_from_local_env = None
        ssl_verify_from_local_env = None
        token_from_env_variable = os.environ.get("BLUEQUBIT_API_TOKEN")

        if config_location.is_file():
            with config_location.open(encoding="utf-8") as f:
                config = json.load(f)
            main_endpoint_from_local_env = config.get("main_endpoint")
            ssl_verify_from_local_env = config.get("ssl_verify")
        main_endpoint_from_local_env = os.environ.get(
            "BLUEQUBIT_MAIN_ENDPOINT", main_endpoint_from_local_env
        )
        self._authenticated = None
        if api_token is None:
            if token_from_env_variable is None:
                logger.warning(AUTH_ERROR_MESSAGE)
                self._authenticated = False
            api_token = token_from_env_variable

        api_config = {
            "token": api_token,
            "main_endpoint": (
                "https://app.bluequbit.io/api/v1"
                if main_endpoint_from_local_env is None
                or main_endpoint_from_local_env == ""
                else main_endpoint_from_local_env
            ),
            "ssl_verify": (
                True if ssl_verify_from_local_env is None else ssl_verify_from_local_env
            ),
        }

        self._token = api_token

        self._default_headers = {
            "Authorization": f"SDK {self._token}",
            "Connection": "close",
            "User-Agent": f"BlueQubit SDK {__version__}",
        }

        self._main_endpoint = "https://app.bluequbit.io/api/v1"
        if self._main_endpoint != api_config["main_endpoint"]:
            self._main_endpoint = api_config["main_endpoint"]
            logger.warning("Using custom endpoint %s", self._main_endpoint)
        main_endpoint_from_env_variable = os.environ.get(
            "BLUEQUBIT_BACKEND_MAIN_ENDPOINT"
        )
        if main_endpoint_from_env_variable is not None:
            self._main_endpoint = main_endpoint_from_env_variable
            logger.warning(
                "Using custom endpoint %s from env variable", self._main_endpoint
            )
        self._verify = True
        if "ssl_verify" in api_config:
            self._verify = api_config["ssl_verify"]
        self._session = None
        if self._authenticated is not False:
            try:
                response = self.send_request(
                    req_type="GET",
                    path="/jobs",
                    params={"limit": 1},
                )
                if response.ok:
                    self._authenticated = True
                else:
                    self._authenticated = False
                    raise BQAPIError(
                        response.status_code,
                        f"Couldn't reach BlueQubit {response.text}.",
                    )
            except BQUnauthorizedAccessError:
                self._authenticated = False
                logger.warning(AUTH_ERROR_MESSAGE)
                return

    def send_request(
        self,
        req_type,
        path,
        params=None,
        data=None,
        json_req=None,
        headers=None,
    ):
        url = self._main_endpoint + path

        if params is not None:
            for key, value in params.items():
                if isinstance(value, str):
                    params[key] = value.replace("\\", "\\\\")
                if isinstance(value, list):
                    params[key] = ",".join(value)

        if headers is None:
            headers_to_send = self._default_headers
        else:
            headers_to_send = dict(self._default_headers, **headers)

        return request_retriable(
            method=req_type,
            url=url,
            data=data,
            json=json_req,
            params=params,
            headers=headers_to_send,
        )

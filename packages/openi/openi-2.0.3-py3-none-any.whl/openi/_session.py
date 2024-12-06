#!/usr/bin/env python
import json
import os
import warnings
from time import sleep
from typing import Any, Callable, Optional

import requests

from ._exceptions import (
    HttpConnectionError,
    HttpProxyError,
    PageNotFound,
    ServerError,
    TokenNotFoundError,
    TokenNotFoundWarn,
    UnauthorizedError,
)
from .constants import DEFAULT_BASE_URL, HTTP_MAX_RETRIES, HTTP_RETRY_DELAY, TOKEN_FILE_PATH
from .log import setup_logger

logger = setup_logger()


def retry(func: Callable) -> Callable:
    """
    Decorator that retries a function a certain number of times with a delay between each retry.

    Args:
        func (Callable): The function to be retried.

    Returns:
        Callable: The decorated function.

    """
    retries: int = HTTP_MAX_RETRIES
    delay: float = HTTP_RETRY_DELAY

    def _retry(*args, **kwargs) -> Any:
        for i in range(1, retries + 1):
            if func.__name__ == "put_upload":
                url = args[1] if len(args) > 1 else kwargs.get("url", None)

            if func.__name__ == "http_request":
                url = args[2] if len(args) > 2 else kwargs.get("route", None)

            try:
                return func(*args, **kwargs)

            except Exception as e:
                if i == retries:
                    logger.error(f"{i} failed; Error: {repr(e)}")
                    logger.error(f"`{url}` failed after {retries} retries; ")

                    if isinstance(e, requests.exceptions.ProxyError):
                        raise HttpProxyError()

                    if isinstance(e, requests.exceptions.ConnectionError):
                        raise HttpConnectionError()

                    else:
                        raise e

                else:
                    logger.error(f"{i} failed -> Retrying...; Error: {repr(e)}")
                    sleep(delay)

    return _retry


@retry
def put_upload(
    url,
    filedata: bytes,
    filename: str,
    upload_type: int = 0,
    **kwargs,
) -> Optional[str]:
    """Override the put method

    Args:
        url (str): URL of CloudStorage to upload file data
        filedata (bytes): Binary file data to upload
        upload_type (int, optional): 0 for minio, 1 for obs

    Returns:
        Response: Response object from requests
    """
    headers = {"Content-Type": "text/plain"} if upload_type == 0 else {}

    resp = requests.put(url, data=filedata, headers=headers, **kwargs)
    etag = resp.headers.get("ETag", None)

    logger.info(f"PUT {resp.status_code} `{filename}`; etag: {etag}")
    return etag


class OpenISession(requests.Session):
    def __init__(self, *args: list, **kwargs: dict):
        """
        Initialize OpenISession object
        """
        super(OpenISession, self).__init__(*args, **kwargs)
        self.endpoint: str = DEFAULT_BASE_URL
        self.token: Optional[str] = None
        self.dev_mode: bool = False

    def __repr__(self):
        return f"OpenISession(endpoint={self.endpoint}, token={self.token})"

    @staticmethod
    def get_local_auth() -> Optional[dict]:
        """
        Load saved `token.json` on local machine for set_basic_auth()

        Returns:
            tuple: (endpoint, token), loaded from `token.json`
        """
        try:
            return json.loads(TOKEN_FILE_PATH.read_text())

        except FileNotFoundError:
            logger.error(f"No token file found at `{TOKEN_FILE_PATH}`.")
            return None

        except json.decoder.JSONDecodeError:
            logger.error(f"Invalid JSON format at `{TOKEN_FILE_PATH}`.")
            return None

        except Exception as e:
            logger.error(f"Unknown Error: {repr(e)}")
            raise None

    def set_basic_auth(
        self,
        token: Optional[str],
        endpoint: Optional[str],
    ) -> None:
        """Set the credentials for Basic Auth on the session object
        Priority:
            1. provided arguments
            2. local saved token.json
            3. environment variables
        """
        # get from saved token file
        token_saved, endpoint_saved = None, None
        saved_auth = self.get_local_auth()
        if saved_auth:
            token_saved = saved_auth.get("token", None)
            endpoint_saved = saved_auth.get("endpoint", None)

        # get from environment variables
        token_env = os.getenv("OPENI_TOKEN", None)
        endpoint_env = os.getenv("OPENI_ENDPOINT", None)

        self.token = token or token_saved or token_env or self.token
        self.endpoint = endpoint or endpoint_saved or endpoint_env or self.endpoint
        self.endpoint = self.endpoint.rstrip("/")

    def _build_url(self, route: str) -> str:
        """Generate the full URL based on the self.endpoint plus the provided
        resource (API endpoint)

        Args:
            url (str): API Endpoint suffix as found in the API documentation

        Returns:
            str: Full URL for API call
        """
        return self.endpoint + "/api/v1" + route

    def _build_token_headers(self, headers: Optional[dict]) -> Optional[dict]:
        """Adding token to the request's parameters

        Returns:
            dict: Arbitrary Request's keyword arguments with `token` key,value added in
                query parameter `params`.
        """
        headers = dict() if headers is None else headers

        if self.token is not None:
            headers.update({"Authorization": f"token {self.token}"})

        return headers

    @staticmethod
    def request_info(resp: requests.Response) -> None:
        print(f"{'=' * 20}")
        print(f"{resp.request.method} {resp.status_code} {resp.url}")
        print(f"{resp.request.headers}")
        print(f"{'=' * 20}")

    def handle_status_code_error(self, resp: requests.Response, auth: Optional[dict]) -> None:
        if resp.status_code in [401, 403, 404]:
            if resp.status_code == 404 and not auth:
                # warnings.warn(
                #     "\033[0;31mNo local access token found."
                #     "If you cannot access the following, "
                #     "please `login` with your token.\033[0m",
                # )
                raise TokenNotFoundError()
            if resp.status_code == 404:
                raise PageNotFound()
            else:
                raise UnauthorizedError(status_code=resp.status_code)

        if resp.status_code in [500, 502]:
            raise ServerError(resp.status_code)

    # @retry
    def send_request(self, method: str, route: str, **kwargs) -> requests.Response:
        """Customized request method

        adding customized HTTP request mechanism here, e.g. retry mechanism


        Args:
            method (str): HTTP Method
            route (str): API Endpoint suffix as found in `AiForge/api`
            **kwargs: Arbitrary keyword arguments

        Returns:
            Response: Response object from requests
        """
        full_url = self._build_url(route)

        headers = kwargs.pop("headers", None)
        headers_with_token = self._build_token_headers(headers)

        auth = headers_with_token.get("Authorization", None)

        try:
            resp = super(OpenISession, self).request(
                method=method,
                url=full_url,
                headers=headers_with_token,
                **kwargs,
            )
            logger.info(f"{method} {resp.status_code} {resp.url};")
            if self.dev_mode:
                self.request_info(resp)

            self.handle_status_code_error(resp, auth=auth)

        except Exception as e:
            if isinstance(e, requests.exceptions.ProxyError):
                raise HttpProxyError()

            if isinstance(e, requests.exceptions.ConnectionError):
                raise HttpConnectionError()

        return resp

    def get(self, route, **kwargs):
        """Override the get method

        Args:
            route (str): API Endpoint suffix as found in `AiForge/api`
            **kwargs: Arbitrary keyword arguments

        Returns:
            Response: Response object from requests
        """
        return self.send_request("GET", route, **kwargs)

    def post(self, route, json: Optional[dict] = None, **kwargs):
        """Override the post method

        Args:
            route (str): API Endpoint suffix as found in `AiForge/api`
            json (dict, optional): Request's body data
            **kwargs: Arbitrary keyword arguments

        Returns:
            Response: Response object from requests
        """
        return self.send_request("POST", route, json=json, **kwargs)

    # @retry
    def put_upload(
        self,
        url,
        filedata: bytes,
        upload_type: int = 1,
        **kwargs,
    ) -> Optional[str]:
        """Override the put method

        Args:
            url (str): URL of CloudStorage to upload file data
            filedata (bytes): Binary file data to upload
            filename (str): Name of the file to upload
            upload_type (int, optional): 0 for minio, 1 for obs

        Returns:
            Response: Response object from requests
        """
        headers = {"Content-Type": "text/plain"} if upload_type == 0 else {}

        resp = super(OpenISession, self).request(
            method="PUT",
            url=url,
            data=filedata,
            headers=headers,
            **kwargs,
        )
        if not resp or resp.status_code != 200:
            logger.error(f"PUT upload failed to make requests")
            return None

        etag = resp.headers.get("ETag", None)
        logger.info(f"PUT {resp.status_code} `{url}`")
        if etag:
            logger.info(f"ETag: {etag}")
        else:
            logger.error(f"Failed to fetch ETag")

        return etag

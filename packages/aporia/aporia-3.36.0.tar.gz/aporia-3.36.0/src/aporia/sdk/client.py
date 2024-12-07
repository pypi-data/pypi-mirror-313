from http import HTTPStatus
from typing import Dict, Optional, Tuple, Union

import requests


class EntityNotFoundException(Exception):
    pass


class BackendRuntimeError(Exception):
    status_code: int
    body: Union[str, dict]

    def __init__(self, message: str, status_code: int, body: Union[str, dict]):
        super().__init__(message)
        self.status_code = status_code
        self.body = body


class Client:
    def __init__(
        self,
        base_url: str,
        token: str,
        debug: bool = False,
        requests_session: Optional[requests.Session] = None,
    ):
        self.base_url = base_url
        self.token = token
        self.debug = debug
        if requests_session is None:
            self._session = requests.Session()
        else:
            self._session = requests_session
        # Not setting Authorization header in session in case it's shared between multiple clients

    def send_request(
        self,
        url: str,
        method: str,
        data: Optional[Dict] = None,
        params: Optional[Dict[str, str]] = None,
        url_override: Optional[str] = None,
        url_search_replace: Optional[Tuple[str, str]] = None,
    ):
        if url_override is not None:
            target_url = url_override
        else:
            target_url = self.base_url + url

        if url_search_replace is not None:
            target_url = target_url.replace(url_search_replace[0], url_search_replace[1])

        if self.debug:
            print(f"{method} {target_url}, ({data})", end=" -> ")

        response = self._session.request(
            method=method,
            url=target_url,
            json=data,
            params=params,  # TODO: Start using this all over
            headers={"Authorization": f"Bearer {self.token}"},
        )

        if self.debug:
            print(f"{response.status_code}")

        return response

    def assert_response(self, response: requests.Response):
        if response.status_code == HTTPStatus.NOT_FOUND.value:
            raise EntityNotFoundException()
        if not response.ok:
            try:
                body = response.json()
            except Exception:
                body = response.content
            if self.debug:
                print(f"Request failed with status {response.status_code}, body: {body}")
            raise BackendRuntimeError(
                f"Request failed with status {response.status_code}, body: {body}",
                status_code=response.status_code,
                body=body,
            )

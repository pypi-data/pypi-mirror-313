import enum
import logging
import os
import time
from asyncio import Lock
from typing import Callable, Optional

from keycloak import KeycloakOpenID
from urllib3.util.retry import log

from tp_interfaces.logging.time import TimeMeasurer
from ._abstract import AsyncAbstractGQLClient

logger = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class AuthEnvs(enum.Enum):
    AUTH_URL = "KEYCLOAK_AUTH_URL"
    REALM = "KEYCLOAK_REALM"
    CLIENT_ID = "KEYCLOAK_CLIENT_ID"
    CLIENT_KEY = "KEYCLOAK_CLIENT_KEY"
    USER = "KEYCLOAK_USER"
    PWD = "KEYCLOAK_PWD"

    @property
    def env(self) -> str:
        return os.getenv(self.value)


class AsyncKeycloakAwareGQLClient(AsyncAbstractGQLClient):
    _TIME_OFFSET = 10  # in seconds

    def __init__(self, gql_uri: str, timeout: int = 60, concurrency_limit: int = 10, retry_execute: bool | Callable = True):
        super().__init__(gql_uri, timeout, concurrency_limit, retry_execute)

        self._auth: dict[AuthEnvs, str] = {env: env.env for env in AuthEnvs}

        not_set_envs = {env for env, val in self._auth.items() if val is None}
        if not_set_envs:
            raise ValueError(f"Authorization environment values are not set: {not_set_envs}")

        self._keycloak_openid: Optional[KeycloakOpenID] = None
        self._access_token: Optional[str] = None
        self._refresh_token: Optional[str] = None
        self._access_expiration_timestamp: float = 0
        self._refresh_expiration_timestamp: float = 0

        self._lock = Lock()

    async def _ensure_session_liveness(self):
        offsetted_time = time.time() + self._TIME_OFFSET
        if offsetted_time < self._access_expiration_timestamp:
            return

        time_before_req = time.time()
        if offsetted_time < self._refresh_expiration_timestamp and self._refresh_token is not None:
            with TimeMeasurer("refreshing access token with refresh token", logger=logger):
                token_info = self._keycloak_openid.refresh_token(self._refresh_token)
        else:
            with TimeMeasurer("refreshing access token with credentials", logger=logger):
                token_info = self._keycloak_openid.token(self._auth[AuthEnvs.USER], self._auth[AuthEnvs.PWD])

        self._access_token = token_info['access_token']
        self._access_expiration_timestamp = time_before_req + token_info['expires_in']
        self._refresh_token = token_info['refresh_token']
        self._refresh_expiration_timestamp = time_before_req + token_info['refresh_expires_in']

        headers = {"X-Auth-Token": self._access_token, "Authorization": f"Bearer {self._access_token}"}
        await self._configure_session(headers)

    async def __aenter__(self):
        self._keycloak_openid = KeycloakOpenID(
            self._auth[AuthEnvs.AUTH_URL], self._auth[AuthEnvs.REALM], self._auth[AuthEnvs.CLIENT_ID], self._auth[AuthEnvs.CLIENT_KEY]
        )
        return self

    async def __aexit__(self, exc_type=None, exc_val=None, exc_tb=None):
        async with self._lock:
            async with self._rw_lock.writer_lock:
                await self._close_session()

            self._access_token, self._refresh_token = None, None
            self._access_expiration_timestamp, self._refresh_expiration_timestamp = 0, 0
            self._keycloak_openid = None

    async def execute(self, document, variables=None, operation_name=None, extra_headers=None, timeout=None):
        async with self._lock:  # lock session configuration to avoid concurrent keycloack requests
            await self._ensure_session_liveness()
        return await super().execute(document, variables, operation_name, extra_headers, timeout)

from typing import NamedTuple

from ._abstract import AsyncAbstractGQLClient, build_retry_execute
from ._keycloak import AsyncKeycloakAwareGQLClient
from ._noauth import AsyncNoAuthGQLClient


class GQLClientConfig(NamedTuple):
    uri: str
    auth: bool = False
    timeout: int = 60
    concurrency_limit: int = 30
    retry_execute: bool | dict = True

    def configure(self) -> AsyncAbstractGQLClient:
        retry_execute = build_retry_execute(self.retry_execute)
        if self.auth:
            return AsyncKeycloakAwareGQLClient(self.uri, self.timeout, self.concurrency_limit, retry_execute)
        return AsyncNoAuthGQLClient(self.uri, self.timeout, self.concurrency_limit, retry_execute)

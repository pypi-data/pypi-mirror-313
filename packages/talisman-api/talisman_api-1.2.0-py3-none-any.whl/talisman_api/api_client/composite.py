from enum import Enum
from typing import Iterator, Mapping

from .client import TalismanAPIClient
from .gql_clients import GQLClientConfig


class APISchema(str, Enum):
    PUBLIC = "public"
    KB_UTILS = "kbutils"


class CompositeTalismanAPIClient(Mapping[APISchema, TalismanAPIClient]):
    def __init__(self, config: dict[str | APISchema, GQLClientConfig]):
        self._api_clients: dict[APISchema, TalismanAPIClient] = {
            APISchema(key): TalismanAPIClient(value) for key, value in config.items()
        }

    def __contains__(self, item: object) -> bool:
        return item in self._api_clients

    def __getitem__(self, item: APISchema) -> TalismanAPIClient:
        return self._api_clients.get(item)

    def __iter__(self) -> Iterator[APISchema]:
        return iter(self._api_clients)

    def __len__(self) -> int:
        return len(self._api_clients)

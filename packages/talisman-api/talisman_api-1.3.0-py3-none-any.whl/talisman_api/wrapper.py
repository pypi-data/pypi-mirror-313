import logging
from contextlib import AbstractAsyncContextManager
from typing import AsyncIterator, Callable

from graphql import DocumentNode

from .api_client import TalismanAPIClient as BaseClient

_LOGGER = logging.getLogger(__name__)


class TalismanAPIClient(AbstractAsyncContextManager):
    def __init__(self, client: BaseClient, document: DocumentNode):
        self._client = client
        self._document = document

    async def __aenter__(self):
        await self._client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._client.__aexit__(exc_type, exc_val, exc_tb)

    async def execute(self, operation_name: str, variables: dict | None = None, raise_on_timeout: bool = True):
        result = await self._client.execute(self._document, operation_name, variables, raise_on_timeout)
        _LOGGER.debug(
            f'query has been executed',
            extra={'operation': operation_name, 'variables': str(variables), 'result': str(result)}
        )
        return result

    async def paginate_items(
            self,
            operation_name: str,
            variables: dict = None,
            *,
            page_size: int = 20,
            extract_page: Callable[[dict], dict] = lambda d: d
    ) -> AsyncIterator[dict]:
        async for i in self._client.paginate_items(
                self._document,
                operation_name,
                variables,
                page_size=page_size,
                extract_page=extract_page
        ):
            yield i

    async def get_all_items(
            self,
            operation_name: str,
            variables: dict = None,
            *,
            extract_page: Callable[[dict], dict] = lambda d: d
    ):
        async for i in self._client.get_all_items(
                self._document,
                operation_name,
                variables,
                extract_page=extract_page
        ):
            yield i

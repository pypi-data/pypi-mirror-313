import asyncio
import logging
from contextlib import AbstractAsyncContextManager
from typing import AsyncIterator, Callable

from graphql import DocumentNode
from requests import Timeout

from .gql_clients import AsyncAbstractGQLClient, GQLClientConfig

logger = logging.getLogger(__name__)


class TalismanAPIClient(AbstractAsyncContextManager):

    def __init__(self, config: GQLClientConfig):
        self._config = config
        self._gql_client: AsyncAbstractGQLClient | None = None

        self._lock = asyncio.Lock()
        self._opened: int = 0
        self._close_task = None

    async def __aenter__(self):
        async with self._lock:
            self._opened += 1
            if self._gql_client is None:
                self._gql_client = self._config.configure()
                await self._gql_client.__aenter__()
            if self._close_task is not None:
                self._close_task.cancel()
                self._close_task = None
        return self

    async def __aexit__(self, exc_type=None, exc_val=None, exc_tb=None):
        async with self._lock:
            self._opened -= 1
            if self._opened == 0 and self._close_task is None:
                self._close_task = asyncio.create_task(self._delayed_close())

    async def _delayed_close(self, delay: int = 10):
        try:
            await asyncio.sleep(delay)
            async with self._lock:
                if self._opened == 0 and self._gql_client is not None:
                    await self._gql_client.__aexit__(None, None, None)
                    self._gql_client = None
        except asyncio.CancelledError:
            pass

    def validate(self, document: DocumentNode) -> bool:
        return self._gql_client.validate(document)

    async def execute(self, document: DocumentNode, operation_name: str, variables: dict | None = None, raise_on_timeout: bool = True):
        try:
            async with self:
                return await self._gql_client.execute(document, operation_name=operation_name, variables=variables)

        except Timeout as e:
            logger.error('Timeout while query processing', exc_info=e,
                         extra={'variables': str(variables), 'operation_name': operation_name})
            if raise_on_timeout:
                raise e
        except Exception as e:
            logger.error('Some exception was occured during query processing.', exc_info=e,
                         extra={'variables': str(variables), 'operation_name': operation_name})

            raise

    async def paginate_items(
            self,
            document: DocumentNode,
            operation_name: str,
            variables: dict = None,
            *,
            page_size: int = 50,
            extract_page: Callable[[dict], dict] = lambda d: d
    ) -> AsyncIterator[dict]:
        if variables is None:
            variables = {}
        total = 1  # some value greater than 0
        offset = 0
        while offset < total:
            query_variables = {**variables, "offset": offset, "limit": page_size}
            page = extract_page(await self.execute(document, operation_name, query_variables))
            total = page['pagination']['total']
            items = page['pagination'].get('list', tuple())
            for item in items:
                yield item
            offset += len(items)

    async def get_all_items(
            self,
            document: DocumentNode,
            operation_name: str,
            variables: dict = None,
            *,
            extract_page: Callable[[dict], dict] = lambda d: d
    ):
        if variables is None:
            variables = {}
        # get total only
        query_variables = {**variables, "offset": 0, "limit": 0}
        page = extract_page(await self.execute(document, operation_name, query_variables))
        total = page['pagination']['total']

        # get all items
        query_variables = {**variables, "offset": 0, "limit": total}
        page = extract_page(await self.execute(document, operation_name, query_variables))
        items = page['pagination'].get('list', tuple())
        for item in items:
            yield item

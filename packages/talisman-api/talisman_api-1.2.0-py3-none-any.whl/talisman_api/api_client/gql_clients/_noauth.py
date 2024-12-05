from ._abstract import AsyncAbstractGQLClient


class AsyncNoAuthGQLClient(AsyncAbstractGQLClient):

    async def __aenter__(self):
        await self._configure_session()
        return self

    async def __aexit__(self, exc_type=None, exc_val=None, exc_tb=None):
        async with self._rw_lock.writer_lock:
            await self._close_session()

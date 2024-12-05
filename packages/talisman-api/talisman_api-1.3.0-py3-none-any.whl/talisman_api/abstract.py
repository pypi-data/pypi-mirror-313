import inspect
import logging
from abc import ABCMeta, abstractmethod
from importlib import import_module, resources
from typing import Iterable

from gql import gql
from graphql import DocumentNode, GraphQLError
from typing_extensions import Self

from .api_client import CompositeTalismanAPIClient
from .api_client.composite import APISchema
from .wrapper import TalismanAPIClient

_LOGGER = logging.getLogger(__name__)


class AbstractTalismanAPI(metaclass=ABCMeta):
    _VERSION: dict[APISchema, str]

    def __init__(self, client: CompositeTalismanAPIClient, documents: dict[APISchema, DocumentNode]):
        if set(client) != set(documents):
            raise ValueError
        self._composite_client: CompositeTalismanAPIClient = client
        self._documents: dict[APISchema, DocumentNode] = documents

    def _client(self, schema: APISchema) -> TalismanAPIClient:
        return TalismanAPIClient(self._composite_client[schema], self._documents[schema])

    @classmethod
    @abstractmethod
    def _required_apis(cls) -> Iterable[APISchema]:
        pass

    @classmethod
    async def create(cls, client: CompositeTalismanAPIClient, *, logger: logging.Logger = _LOGGER) -> Self:
        documents: dict[APISchema, DocumentNode] = {}
        for api_schema in cls._required_apis():
            if api_schema not in client:
                logger.error(f'{cls} initialization: Client is not configured to use {api_schema} API')
                raise ValueError(f'Client is not configured to use {api_schema} API')

            package, _ = cls.__module__.rsplit('.', maxsplit=1)
            resource_name = f'graphql/{cls._VERSION[api_schema]}/{api_schema.value}.graphql'
            try:
                with (resources.files(package) / resource_name).open('r', encoding='utf-8') as f:
                    document: str = f.read()
            except Exception as e:
                logger.error(f'{cls} initialization: Package {package} contains no required {resource_name} file', exc_info=e)
                raise ValueError(f'Package {package} contains no required {resource_name} file') from e
            try:
                document: DocumentNode = gql(document)
            except GraphQLError as e:
                logger.error(f'{cls} initialization: GraphQL syntax error if {resource_name} (package {package})', exc_info=e)
                raise ValueError(f'GraphQL syntax error if {resource_name} (package {package})') from e

            api_client = client[api_schema]
            async with api_client:
                try:
                    await api_client.validate(document)
                    logger.info(f'{cls} initialization: {resource_name} (package {package}) match runtime server {api_schema} API')
                except Exception as e:
                    logger.error(
                        f'{cls} initialization: {resource_name} (package {package}) do not match runtime server {api_schema} API',
                        exc_info=e
                    )
                    raise ValueError(f'{resource_name} (package {package}) do not match runtime server {api_schema} API') from e
            documents[api_schema] = document
        return cls(client, documents)

    @classmethod
    async def get_compatible_api(
            cls,
            client: CompositeTalismanAPIClient,
            *,
            logger: logging.Logger = _LOGGER,
            impl_package: str = '_impl'
    ) -> Self:
        package, _ = cls.__module__.rsplit('.', 1)
        package_name = f'{package}.{impl_package}'
        package = import_module(package_name)
        if not hasattr(package, '__all__'):
            raise ValueError(
                f'{package_name}.__init__ should define __all__ attribute with ordered API implementation classes'
            )
        for impl_name in package.__all__:
            impl_cls = getattr(package, impl_name, None)
            if not inspect.isclass(impl_cls):
                logger.error(f'{package_name}.__all__ should contains only API implementation classes')
                continue
            if not issubclass(impl_cls, cls):
                logger.error(f'{package_name}.{impl_name} should inherit {cls}')
                continue
            try:
                return await impl_cls.create(client)
            except ValueError as e:
                logger.info(
                    f'{package_name}.{impl_name} (version: "{impl_cls._VERSION}") is not compatible with actual API: {e}',
                    exc_info=e
                )
        raise NotImplementedError('API version is not supported')

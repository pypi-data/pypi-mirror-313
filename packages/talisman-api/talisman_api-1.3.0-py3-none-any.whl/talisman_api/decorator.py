from functools import singledispatch

from . import APISchema
from .abstract import AbstractTalismanAPI


@singledispatch
def version(v: str | dict[APISchema, str]):
    ...


@version.register
def _(v: str):
    def decorate(cls: type[AbstractTalismanAPI]):
        cls._VERSION = dict.fromkeys(cls._required_apis(), v)
        return cls

    return decorate


@version.register
def _(v: dict):
    def decorate(cls: type[AbstractTalismanAPI]):
        cls._VERSION = dict(v)
        return cls

    return decorate

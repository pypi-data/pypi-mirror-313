from abc import ABCMeta, abstractmethod
from contextlib import AbstractAsyncContextManager
from typing import Generic, Optional, Type, TypeVar

from tdm import TalismanDocument
from typing_extensions import Self

from tp_interfaces.abstract import ImmutableBaseModel

_LoaderConfig = TypeVar('_LoaderConfig', bound=ImmutableBaseModel)


class Loader(AbstractAsyncContextManager, Generic[_LoaderConfig], metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def from_config(cls, config: dict) -> Self:
        pass

    @property
    @abstractmethod
    def config_type(self) -> Type[_LoaderConfig]:
        pass

    @abstractmethod
    async def load_doc_and_bind_facts(self, doc: TalismanDocument, config: _LoaderConfig) -> Optional[str]:
        pass

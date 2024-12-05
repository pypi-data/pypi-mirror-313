from abc import ABCMeta, abstractmethod
from typing import Iterator, TypeVar

from tdm import TalismanDocument


class AbstractReader(metaclass=ABCMeta):
    @abstractmethod
    def read(self) -> Iterator[TalismanDocument]:
        pass


_AbstractConfigurableReader = TypeVar('_AbstractConfigurableReader', bound='AbstractConfigurableReader')


class AbstractConfigurableReader(AbstractReader, metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def from_config(cls: _AbstractConfigurableReader, config) -> _AbstractConfigurableReader:
        pass

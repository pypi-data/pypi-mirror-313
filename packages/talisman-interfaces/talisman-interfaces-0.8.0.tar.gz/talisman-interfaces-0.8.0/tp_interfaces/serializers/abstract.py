from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import Iterable, TextIO

from tdm import TalismanDocument


class AbstractSerializer(metaclass=ABCMeta):
    @abstractmethod
    def serialize(self, doc: TalismanDocument, stream: TextIO):
        pass

    @staticmethod
    def _check_stream(stream: TextIO):
        if stream.closed or not stream.writable():
            raise Exception("stream  is closed or not writeable")


class AbstractPathSerializer(metaclass=ABCMeta):
    @abstractmethod
    def serialize(self, docs: Iterable[TalismanDocument], path: Path):
        pass

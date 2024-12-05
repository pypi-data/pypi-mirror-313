import asyncio
from abc import ABCMeta
from functools import partial
from itertools import chain
from typing import Iterator, Protocol, Sequence, Tuple, Type, TypeVar, runtime_checkable

from more_itertools import ichunked
from tdm import TalismanDocument

from tp_interfaces.abstract.model import AsyncModel
from tp_interfaces.abstract.schema import ImmutableBaseModel
from tp_interfaces.logging.context import with_log_extras
from tp_interfaces.serializable import Serializable

_Config = TypeVar('_Config', bound=ImmutableBaseModel)


@runtime_checkable
class AbstractDocumentProcessor(AsyncModel, Protocol[_Config]):

    async def process_doc(self, document: TalismanDocument, config: _Config) -> TalismanDocument:
        pass

    async def process_docs(self, documents: Sequence[TalismanDocument], config: _Config) -> Tuple[TalismanDocument, ...]:
        log_extras = with_log_extras(doc_id=lambda kwargs: kwargs['document'].id)
        return tuple(await asyncio.gather(*map(partial(log_extras(self.process_doc), config=config), documents)))

    def process_stream(self, documents: Iterator[TalismanDocument], config: _Config, batch_size: int) \
            -> Iterator[TalismanDocument]:
        return chain.from_iterable(map(partial(self.process_docs, config=config), map(tuple, ichunked(documents, batch_size))))

    @property
    def config_type(self) -> Type[_Config]:
        raise NotImplementedError


class AbstractSerializableDocumentProcessor(AbstractDocumentProcessor, Serializable, metaclass=ABCMeta):
    pass

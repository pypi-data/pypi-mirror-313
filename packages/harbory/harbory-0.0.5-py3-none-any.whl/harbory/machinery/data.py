import itertools
from typing import Generic, Iterable, Iterator, Sequence, Union

from colt import Registrable

from harbory.types import T_DataContainer

from .types import T_Example
from .utils import load_datasource


class DataSource(Generic[T_Example], Registrable):
    def load(self) -> Iterator[T_Example]:
        raise NotImplementedError


@DataSource.register("chain")
class ChainDataSource(DataSource[T_Example]):
    def __init__(self, sources: Sequence[Union[DataSource[T_Example], Iterable[T_Example]]]) -> None:
        self.sources = sources

    def load(self) -> Iterator[T_Example]:
        return itertools.chain.from_iterable(load_datasource(source) for source in self.sources)


class DataSink(Generic[T_DataContainer], Registrable):
    def save(self, data: Iterator[T_DataContainer]) -> None:
        raise NotImplementedError

from typing import TYPE_CHECKING, Iterable, Optional, Union, overload

from harbory.types import T_DataContainer

if TYPE_CHECKING:
    from .data import DataSource


@overload
def load_datasource(
    datasource: Union["DataSource[T_DataContainer]", Iterable[T_DataContainer]]
) -> Iterable[T_DataContainer]: ...


@overload
def load_datasource(datasource: None) -> None: ...


def load_datasource(
    datasource: Optional[Union["DataSource[T_DataContainer]", Iterable[T_DataContainer]]]
) -> Optional[Iterable[T_DataContainer]]:
    from .data import DataSource

    if isinstance(datasource, DataSource):
        return datasource.load()
    return datasource

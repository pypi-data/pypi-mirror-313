from typing import TypeVar

from harbory.types import DataContainer

T_Example = TypeVar("T_Example", bound=DataContainer)
T_Prediction = TypeVar("T_Prediction", bound=DataContainer)

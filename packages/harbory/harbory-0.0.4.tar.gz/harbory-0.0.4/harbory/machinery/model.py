from collections.abc import Iterable, Iterator
from logging import Logger
from os import PathLike
from typing import Generic, Optional, TypeVar, Union

import dill

from .processor import Processor
from .types import T_Example, T_Prediction

T_Fixtures = TypeVar("T_Fixtures")
T_SetupParams = TypeVar("T_SetupParams")
T_PredictionParams = TypeVar("T_PredictionParams")
T_EvaluationParams = TypeVar("T_EvaluationParams")
T_Model = TypeVar("T_Model", bound="Model")


class Model(
    Generic[
        T_Example,
        T_Prediction,
        T_Fixtures,
        T_SetupParams,
        T_PredictionParams,
        T_EvaluationParams,
    ],
    Processor[
        T_Example,
        T_Prediction,
        T_Fixtures,
        T_PredictionParams,
    ],
):
    Input: type[T_Example]
    Output: type[T_Prediction]
    SetupParams: type[T_SetupParams]
    PredictionParams: type[T_PredictionParams]
    EvaluationParams: type[T_EvaluationParams]

    @property
    def logger(self) -> Logger:
        from harbory.workflow import use_step_logger

        return use_step_logger(default=f"{self.__class__.__module__}.{self.__class__.__name__}")

    def setup(self, params: Optional[T_SetupParams] = None) -> None:
        pass

    def train(
        self,
        train_dataset: Iterable[T_Example],
        valid_dataset: Optional[Iterable[T_Example]],
    ) -> None:
        pass

    def predict(
        self,
        dataset: Iterable[T_Example],
        params: Optional[T_PredictionParams] = None,
        *,
        batch_size: Optional[int] = None,
        max_workers: Optional[int] = None,
    ) -> Iterator[T_Prediction]:
        yield from self(
            dataset,
            params,
            batch_size=batch_size,
            max_workers=max_workers,
        )

    def evaluate(
        self,
        dataset: Iterable[T_Example],
        params: Optional[T_EvaluationParams] = None,
    ) -> dict[str, float]:
        raise NotImplementedError

    def save(self, path: Union[str, PathLike]) -> None:
        with open(path, "wb") as f:
            dill.dump(self, f)

    @classmethod
    def load(cls: type[T_Model], path: Union[str, PathLike]) -> T_Model:
        with open(path, "rb") as f:
            model = dill.load(f)
            assert isinstance(model, cls)
            return model

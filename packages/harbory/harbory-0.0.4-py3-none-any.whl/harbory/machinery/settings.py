import dataclasses
from os import PathLike
from typing import Any, ClassVar, Generic, Optional, TypeVar

from harbory.common.jsonnet import FromJsonnet

from .archive import MachineryArchive
from .colt import COLT_BUILDER
from .data import DataSink, DataSource
from .model import Model, T_EvaluationParams, T_PredictionParams, T_SetupParams
from .processor import Processor
from .types import T_Example, T_Prediction

_T_MachinerySettings = TypeVar("_T_MachinerySettings", bound="MachinerySettings")


@dataclasses.dataclass
class MachinerySettings(FromJsonnet):
    __COLT_BUILDER__: ClassVar = COLT_BUILDER


@dataclasses.dataclass
class MachineryTraningSettings(
    Generic[T_Example, T_Prediction, T_SetupParams, T_EvaluationParams],
    MachinerySettings,
):
    model: Model[T_Example, T_Prediction, Any, T_SetupParams, Any, T_EvaluationParams]
    train_dataset: DataSource[T_Example]
    valid_dataset: Optional[DataSource[T_Example]] = None
    test_dataset: Optional[DataSource[T_Example]] = None
    setup: Optional[T_SetupParams] = None
    evaluation: Optional[T_EvaluationParams] = None
    preprocessor: Optional[Processor[T_Example, T_Example, Any, Any]] = None
    postprocessor: Optional[Processor[T_Prediction, T_Prediction, Any, Any]] = None

    def __post_init__(self) -> None:
        if self.setup is not None:
            self.setup = self.__COLT_BUILDER__(self.setup, self.model.SetupParams)
        if self.evaluation is not None:
            self.evaluation = self.__COLT_BUILDER__(self.evaluation, self.model.EvaluationParams)


@dataclasses.dataclass
class MachineryPredictionSettings(
    Generic[T_Example, T_Prediction, T_SetupParams, T_PredictionParams],
    MachinerySettings,
):
    archive: MachineryArchive[Model[T_Example, T_Prediction, Any, T_SetupParams, T_PredictionParams, Any]]
    dataset: DataSource[T_Example]
    output: DataSink[T_Prediction]
    setup: Optional[T_SetupParams] = None
    params: Optional[T_PredictionParams] = None
    preprocessor: Optional[Processor[T_Example, T_Example, Any, Any]] = None
    postprocessor: Optional[Processor[T_Prediction, T_Prediction, Any, Any]] = None
    batch_size: Optional[int] = None
    max_workers: Optional[int] = None

    @property
    def model(self) -> Model[T_Example, T_Prediction, Any, T_SetupParams, Any, Any]:
        return self.archive.model

    @classmethod
    def __pre_init__(self, config: Any) -> Any:
        if isinstance(config.get("archive"), (str, PathLike)):
            config["archive"] = MachineryArchive.load(config["archive"])
        return config

    def __post_init__(self) -> None:
        if self.setup is not None:
            self.setup = self.__COLT_BUILDER__(self.setup, self.model.SetupParams)
        if self.params is not None:
            self.params = self.__COLT_BUILDER__(self.params, self.model.PredictionParams)


@dataclasses.dataclass
class MachineryEvaluationSettings(
    Generic[T_Example, T_Prediction, T_SetupParams, T_EvaluationParams],
    MachinerySettings,
):
    archive: MachineryArchive[Model[T_Example, T_Prediction, Any, T_SetupParams, Any, T_EvaluationParams]]
    dataset: DataSource[T_Example]
    setup: Optional[T_SetupParams] = None
    params: Optional[T_EvaluationParams] = None
    preprocessor: Optional[Processor[T_Example, T_Example, Any, Any]] = None
    batch_size: Optional[int] = None
    max_workers: Optional[int] = None

    @property
    def model(self) -> Model[T_Example, T_Prediction, Any, T_SetupParams, Any, T_EvaluationParams]:
        return self.archive.model

    @classmethod
    def __pre_init__(self, config: Any) -> Any:
        if isinstance(config.get("archive"), (str, PathLike)):
            config["archive"] = MachineryArchive.load(config["archive"])
        return config

    def __post_init__(self) -> None:
        if self.setup is not None:
            self.setup = self.__COLT_BUILDER__(self.setup, self.model.SetupParams)
        if self.params is not None:
            self.params = self.__COLT_BUILDER__(self.params, self.model.EvaluationParams)

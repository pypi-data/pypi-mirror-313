import dataclasses
import tarfile
import tempfile
from os import PathLike
from pathlib import Path
from typing import ClassVar, Generic, TypeVar, Union, cast

from .model import Model, T_Model

T_MachineryArchive = TypeVar("T_MachineryArchive", bound="MachineryArchive")


@dataclasses.dataclass
class MachineryArchive(Generic[T_Model]):
    model: T_Model

    _MODEL_FILENAME: ClassVar[str] = "model"

    def save(self, path: Union[str, PathLike]) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            working_dir = Path(tmpdir)

            model_path = working_dir / self._MODEL_FILENAME
            self.model.save(model_path)

            with tarfile.open(path, "w:gz") as tar:
                tar.add(model_path, arcname=self._MODEL_FILENAME)

    @classmethod
    def load(cls: type[T_MachineryArchive], path: Union[str, PathLike]) -> T_MachineryArchive:
        with tempfile.TemporaryDirectory() as tmpdir:
            working_dir = Path(tmpdir)

            with tarfile.open(path, "r:gz") as tar:
                tar.extractall(working_dir)

            model_path = working_dir / cls._MODEL_FILENAME
            model = cast(T_Model, Model.load(model_path))

        return cls(model)

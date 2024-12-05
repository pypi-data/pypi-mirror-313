from pathlib import Path
from typing import Any, ClassVar, Generic, cast

from harbory.workflow import Format

from .archive import MachineryArchive, T_MachineryArchive


@Format.register("harbory.machinery.archive")
class MachineryArchiveFormat(Format[T_MachineryArchive], Generic[T_MachineryArchive]):
    _ARTIFACT_FILENAME: ClassVar[str] = "artifact.tar.gz"

    def write(self, artifact: T_MachineryArchive, directory: Path) -> None:
        artifact.save(directory / self._ARTIFACT_FILENAME)

    def read(self, directory: Path) -> T_MachineryArchive:
        return cast(T_MachineryArchive, MachineryArchive.load(directory / self._ARTIFACT_FILENAME))

    @classmethod
    def is_default_of(cls, obj: Any) -> bool:
        return isinstance(obj, MachineryArchive)

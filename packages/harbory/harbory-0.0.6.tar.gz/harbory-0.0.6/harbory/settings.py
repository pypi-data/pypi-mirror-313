import dataclasses
import os
from logging import getLogger
from os import PathLike
from typing import ClassVar, Mapping, Optional, Sequence, TypeVar, Union

import yaml
from colt import ColtBuilder, import_modules

from harbory.constants import DEFAULT_HARBORY_SETTINGS_PATH
from harbory.workflow import WorkflowSettings

from .constants import COLT_ARGSKEY, COLT_TYPEKEY

logger = getLogger(__name__)

T_HarborySettings = TypeVar("T_HarborySettings", bound="HarborySettings")


@dataclasses.dataclass(frozen=True)
class HarborySettings:
    __COLT_BUILDER__: ClassVar[ColtBuilder] = ColtBuilder(typekey=COLT_TYPEKEY, argskey=COLT_ARGSKEY)

    workflow: WorkflowSettings = dataclasses.field(default_factory=WorkflowSettings)

    environment: Mapping[str, str] = dataclasses.field(default_factory=dict)
    required_modules: Sequence[str] = dataclasses.field(default_factory=list)

    @classmethod
    def from_file(cls: type[T_HarborySettings], path: Union[str, PathLike]) -> T_HarborySettings:
        with open(path, "r") as f:
            settings = yaml.safe_load(f)
        # load required modules
        required_modules = cls.__COLT_BUILDER__(settings.pop("required_modules", []), Sequence[str])
        import_modules(required_modules)
        print("imported:", required_modules)
        # load environment variables
        environment = cls.__COLT_BUILDER__(settings.pop("environment", {}), Mapping[str, str])
        os.environ.update(environment)
        return cls.__COLT_BUILDER__(settings, cls)


def load_harbory_settings(path: Optional[Union[str, PathLike]] = None) -> HarborySettings:
    if path is not None or DEFAULT_HARBORY_SETTINGS_PATH.exists():
        path = path or DEFAULT_HARBORY_SETTINGS_PATH
        logger.info(f"Load harbory settings from {path}")
        return HarborySettings.from_file(path)
    return HarborySettings()

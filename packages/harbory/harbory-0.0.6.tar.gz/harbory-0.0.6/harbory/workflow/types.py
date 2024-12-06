from typing import Union

from harbory.types import JsonValue

StepConfig = dict[str, JsonValue]
StrictParamPath = tuple[Union[int, str], ...]

from typing import TypedDict, Union
from typing_extensions import NotRequired

SelectOptionValue = Union[str, int, bool]


class SelectOptionDict(TypedDict):
    value: SelectOptionValue
    label: str
    description: NotRequired[str]


SelectOptionPrimitive = SelectOptionValue

SelectOptions = Union[list[SelectOptionDict], list[SelectOptionPrimitive]]

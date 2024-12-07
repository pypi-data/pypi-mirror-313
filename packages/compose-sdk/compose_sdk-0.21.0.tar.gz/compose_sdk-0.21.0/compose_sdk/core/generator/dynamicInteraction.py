from typing import Union
from .displayInteraction import display_none
from ..ui import ComponentReturn


def dynamic_cond(
    condition: bool,
    *,
    true: Union[ComponentReturn, None] = None,
    false: Union[ComponentReturn, None] = None
) -> ComponentReturn:
    if condition is True:
        if true is None:
            return display_none()
        return true
    else:
        if false is None:
            return display_none()
        return false

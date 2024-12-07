from typing import Callable
from ..ui import (
    INTERACTION_TYPE,
    TYPE,
    ComponentReturn,
    CONFIRM_APPEARANCE,
    CONFIRM_APPEARANCE_DEFAULT,
)


def page_confirm(
    id: str,
    on_response: Callable[[bool], None],
    *,
    title: str = None,
    message: str = None,
    type_to_confirm_text: str = None,
    confirm_button_label: str = None,
    cancel_button_label: str = None,
    appearance: CONFIRM_APPEARANCE = CONFIRM_APPEARANCE_DEFAULT
) -> ComponentReturn:
    model_properties = {
        "hasOnResponseHook": on_response is not None,
    }

    optional_properties = {
        "title": title,
        "message": message,
        "typeToConfirmText": type_to_confirm_text,
        "confirmButtonLabel": confirm_button_label,
        "cancelButtonLabel": cancel_button_label,
        **(
            {"appearance": appearance}
            if appearance != CONFIRM_APPEARANCE_DEFAULT
            else {}
        ),
    }

    for key, value in optional_properties.items():
        if value is not None:
            model_properties[key] = value

    return {
        "model": {
            "id": id,
            "properties": model_properties,
        },
        "hooks": {
            "onResponse": on_response,
        },
        "type": TYPE.PAGE_CONFIRM,
        "interactionType": INTERACTION_TYPE.PAGE,
    }

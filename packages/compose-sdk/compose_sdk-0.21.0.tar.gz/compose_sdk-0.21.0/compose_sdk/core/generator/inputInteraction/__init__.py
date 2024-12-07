from typing import Union, Callable
from ...ui import (
    INTERACTION_TYPE,
    TYPE,
    SelectOptionValue,
    SelectOptions,
    Nullable,
    ComponentReturn,
    ValidatorResponse,
    VoidResponse,
)
from ...file import File
from ..base import MULTI_SELECTION_MIN_DEFAULT, MULTI_SELECTION_MAX_DEFAULT
from .tableComponent import table, dataframe


def input_text(
    id: str,
    *,
    label: str = None,
    required: bool = True,
    description: str = None,
    initial_value: Union[str, None] = None,
    validate: Callable[[Union[str, None]], ValidatorResponse] = None,
    on_enter: Callable[[Union[str, None]], VoidResponse] = None,
    style: Nullable.Style = None,
) -> ComponentReturn:
    return {
        "model": {
            "id": id,
            "label": label,
            "description": description,
            "required": required,
            "hasValidateHook": validate is not None,
            "style": style,
            "properties": {
                "initialValue": initial_value,
                "hasOnEnterHook": on_enter is not None,
            },
        },
        "hooks": {
            "validate": validate,
            "onEnter": on_enter,
        },
        "type": TYPE.INPUT_TEXT,
        "interactionType": INTERACTION_TYPE.INPUT,
    }


def input_email(
    id: str,
    *,
    label: str = None,
    required: bool = True,
    description: str = None,
    initial_value: Union[str, None] = None,
    validate: Callable[[Union[str, None]], ValidatorResponse] = None,
    on_enter: Callable[[Union[str, None]], VoidResponse] = None,
    style: Nullable.Style = None,
) -> ComponentReturn:
    return {
        "model": {
            "id": id,
            "label": label,
            "description": description,
            "required": required,
            "hasValidateHook": validate is not None,
            "style": style,
            "properties": {
                "initialValue": initial_value,
                "hasOnEnterHook": on_enter is not None,
            },
        },
        "hooks": {
            "validate": validate,
            "onEnter": on_enter,
        },
        "type": TYPE.INPUT_EMAIL,
        "interactionType": INTERACTION_TYPE.INPUT,
    }


def input_url(
    id: str,
    *,
    label: Nullable.Str = None,
    required: bool = True,
    description: Nullable.Str = None,
    initial_value: Nullable.Str = None,
    validate: Nullable.Callable = None,
    on_enter: Nullable.Callable = None,
    style: Nullable.Style = None,
) -> ComponentReturn:
    return {
        "model": {
            "id": id,
            "label": label,
            "description": description,
            "required": required,
            "hasValidateHook": validate is not None,
            "style": style,
            "properties": {
                "initialValue": initial_value,
                "hasOnEnterHook": on_enter is not None,
            },
        },
        "hooks": {
            "validate": validate,
            "onEnter": on_enter,
        },
        "type": TYPE.INPUT_URL,
        "interactionType": INTERACTION_TYPE.INPUT,
    }


def input_number(
    id: str,
    *,
    label: str = None,
    required: bool = True,
    description: str = None,
    initial_value: Union[int, float, None] = None,
    validate: Callable[[Union[int, float, None]], ValidatorResponse] = None,
    on_enter: Callable[[Union[int, float, None]], VoidResponse] = None,
    style: Nullable.Style = None,
) -> ComponentReturn:
    return {
        "model": {
            "id": id,
            "label": label,
            "description": description,
            "required": required,
            "hasValidateHook": validate is not None,
            "style": style,
            "properties": {
                "hasOnEnterHook": on_enter is not None,
                "initialValue": initial_value,
            },
        },
        "hooks": {
            "validate": validate,
            "onEnter": on_enter,
        },
        "type": TYPE.INPUT_NUMBER,
        "interactionType": INTERACTION_TYPE.INPUT,
    }


def input_password(
    id: str,
    *,
    label: Nullable.Str = None,
    required: bool = True,
    description: Nullable.Str = None,
    initial_value: Nullable.Str = None,
    validate: Nullable.Callable = None,
    on_enter: Nullable.Callable = None,
    style: Nullable.Style = None,
) -> ComponentReturn:
    return {
        "model": {
            "id": id,
            "label": label,
            "description": description,
            "required": required,
            "hasValidateHook": validate is not None,
            "style": style,
            "properties": {
                "hasOnEnterHook": on_enter is not None,
                "initialValue": initial_value,
            },
        },
        "hooks": {
            "validate": validate,
            "onEnter": on_enter,
        },
        "type": TYPE.INPUT_PASSWORD,
        "interactionType": INTERACTION_TYPE.INPUT,
    }


def _convert_date(date):
    if date is not None:
        return {"day": date.day, "month": date.month, "year": date.year}
    return None


def input_date(
    id: str,
    *,
    label: Nullable.Str = None,
    required: bool = True,
    description: Nullable.Str = None,
    initial_value: Nullable.Date = None,
    min: Nullable.Date = None,
    max: Nullable.Date = None,
    validate: Nullable.Callable = None,
    on_enter: Nullable.Callable = None,
    style: Nullable.Style = None,
) -> ComponentReturn:

    return {
        "model": {
            "id": id,
            "label": label,
            "description": description,
            "required": required,
            "hasValidateHook": validate is not None,
            "style": style,
            "properties": {
                "min": _convert_date(min),
                "max": _convert_date(max),
                "hasOnEnterHook": on_enter is not None,
                "initialValue": _convert_date(initial_value),
            },
        },
        "hooks": {
            "validate": validate,
            "onEnter": on_enter,
        },
        "type": TYPE.INPUT_DATE,
        "interactionType": INTERACTION_TYPE.INPUT,
    }


def radio_group(
    id: str,
    options: SelectOptions,
    *,
    label: Nullable.Str = None,
    required: bool = True,
    description: Nullable.Str = None,
    initial_value: Nullable.SelectOptionValue = None,
    validate: Nullable.Callable = None,
    on_change: Nullable.Callable = None,
    style: Nullable.Style = None,
) -> ComponentReturn:
    return {
        "model": {
            "id": id,
            "label": label,
            "description": description,
            "required": required,
            "hasValidateHook": validate is not None,
            "style": style,
            "properties": {
                "initialValue": initial_value,
                "hasOnSelectHook": on_change is not None,
                "options": options,
            },
        },
        "hooks": {
            "validate": validate,
            "onSelect": on_change,
        },
        "type": TYPE.INPUT_RADIO_GROUP,
        "interactionType": INTERACTION_TYPE.INPUT,
    }


def select_dropdown_single(
    id: str,
    options: SelectOptions,
    *,
    label: Nullable.Str = None,
    required: bool = True,
    description: Nullable.Str = None,
    initial_value: Nullable.SelectOptionValue = None,
    validate: Nullable.Callable = None,
    on_change: Nullable.Callable = None,
    style: Nullable.Style = None,
) -> ComponentReturn:
    return {
        "model": {
            "id": id,
            "label": label,
            "description": description,
            "required": required,
            "hasValidateHook": validate is not None,
            "style": style,
            "properties": {
                "hasOnSelectHook": on_change is not None,
                "options": options,
                "initialValue": initial_value,
            },
        },
        "hooks": {
            "validate": validate,
            "onSelect": on_change,
        },
        "type": TYPE.INPUT_SELECT_DROPDOWN_SINGLE,
        "interactionType": INTERACTION_TYPE.INPUT,
    }


def select_dropdown_multi(
    id: str,
    options: SelectOptions,
    *,
    label: Nullable.Str = None,
    required: bool = True,
    description: Nullable.Str = None,
    initial_value: list[SelectOptionValue] = [],
    validate: Nullable.Callable = None,
    on_change: Nullable.Callable = None,
    style: Nullable.Style = None,
    min_selections: int = MULTI_SELECTION_MIN_DEFAULT,
    max_selections: int = MULTI_SELECTION_MAX_DEFAULT,
) -> ComponentReturn:

    if not isinstance(initial_value, list):
        raise TypeError(
            f"initial_value must be a list for multiselect box, got {type(initial_value).__name__}"
        )

    return {
        "model": {
            "id": id,
            "label": label,
            "description": description,
            "required": required,
            "hasValidateHook": validate is not None,
            "style": style,
            "properties": {
                "initialValue": initial_value,
                "hasOnSelectHook": on_change is not None,
                "options": options,
                "minSelections": min_selections,
                "maxSelections": max_selections,
            },
        },
        "hooks": {
            "validate": validate,
            "onSelect": on_change,
        },
        "type": TYPE.INPUT_SELECT_DROPDOWN_MULTI,
        "interactionType": INTERACTION_TYPE.INPUT,
    }


def input_file_drop(
    id: str,
    *,
    label: str = None,
    required: bool = True,
    description: str = None,
    validate: Callable[[list[File]], ValidatorResponse] = None,
    style: Nullable.Style = None,
    on_change: Callable[[list[File]], VoidResponse] = None,
    accepted_file_types: list[str] = None,
    min_count: int = MULTI_SELECTION_MIN_DEFAULT,
    max_count: int = MULTI_SELECTION_MAX_DEFAULT,
) -> ComponentReturn:
    return {
        "model": {
            "id": id,
            "label": label,
            "description": description,
            "required": required,
            "hasValidateHook": validate is not None,
            "style": style,
            "properties": {
                "hasOnFileChangeHook": on_change is not None,
                "acceptedFileTypes": accepted_file_types,
                "minCount": min_count,
                "maxCount": max_count,
            },
        },
        "hooks": {
            "validate": validate,
            "onFileChange": on_change,
        },
        "type": TYPE.INPUT_FILE_DROP,
        "interactionType": INTERACTION_TYPE.INPUT,
    }


def input_text_area(
    id: str,
    *,
    label: Nullable.Str = None,
    required: bool = True,
    description: Nullable.Str = None,
    initial_value: Nullable.Str = None,
    validate: Nullable.Callable = None,
    on_enter: Nullable.Callable = None,
    style: Nullable.Style = None,
) -> ComponentReturn:
    return {
        "model": {
            "id": id,
            "label": label,
            "description": description,
            "required": required,
            "hasValidateHook": validate is not None,
            "style": style,
            "properties": {
                "initialValue": initial_value,
                "hasOnEnterHook": on_enter is not None,
            },
        },
        "hooks": {
            "validate": validate,
            "onEnter": on_enter,
        },
        "type": TYPE.INPUT_TEXT_AREA,
        "interactionType": INTERACTION_TYPE.INPUT,
    }

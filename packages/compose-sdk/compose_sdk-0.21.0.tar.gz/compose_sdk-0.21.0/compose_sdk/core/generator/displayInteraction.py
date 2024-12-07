import base64
from typing import Union, List, Literal
import io

from ..ui import (
    INTERACTION_TYPE,
    TYPE,
    Nullable,
    DISPLAY_UTILS,
    ComponentReturn,
    LanguageName,
    HeaderSize,
    TextColor,
    TextSize,
)
from ..utils import Utils


class TextComponentReturn(ComponentReturn):
    type: TYPE.DISPLAY_TEXT


def display_text(
    text: Union[
        str,
        int,
        float,
        TextComponentReturn,
        List[Union[str, int, float, TextComponentReturn]],
    ],
    *,
    color: TextColor = None,
    size: TextSize = None,
    style: Nullable.Style = None,
) -> TextComponentReturn:
    id = Utils.generate_id()

    model_properties = {
        "text": text,
    }

    optional_properties = {
        "color": color,
        "size": size,
    }

    for key, value in optional_properties.items():
        if value is not None:
            model_properties[key] = value

    return {
        "model": {"id": id, "style": style, "properties": model_properties},
        "hooks": None,
        "type": TYPE.DISPLAY_TEXT,
        "interactionType": INTERACTION_TYPE.DISPLAY,
    }


def display_header(
    text: str,
    *,
    color: TextColor = None,
    size: HeaderSize = None,
    style: Nullable.Style = None,
) -> ComponentReturn:
    id = Utils.generate_id()

    model_properties = {
        "text": text,
    }

    optional_properties = {
        "color": color,
        "size": size,
    }

    for key, value in optional_properties.items():
        if value is not None:
            model_properties[key] = value

    return {
        "model": {"id": id, "style": style, "properties": model_properties},
        "hooks": None,
        "type": TYPE.DISPLAY_HEADER,
        "interactionType": INTERACTION_TYPE.DISPLAY,
    }


def display_json(
    json: DISPLAY_UTILS.Json,
    *,
    label: Nullable.Str = None,
    description: Nullable.Str = None,
    style: Nullable.Style = None,
) -> ComponentReturn:
    id = Utils.generate_id()

    return {
        "model": {
            "id": id,
            "style": style,
            "properties": {
                "label": label,
                "description": description,
                "json": json,
            },
        },
        "hooks": None,
        "type": TYPE.DISPLAY_JSON,
        "interactionType": INTERACTION_TYPE.DISPLAY,
    }


def display_spinner(
    *, text: Nullable.Str = None, style: Nullable.Style = None
) -> ComponentReturn:
    id = Utils.generate_id()

    return {
        "model": {
            "id": id,
            "style": style,
            "properties": {
                "text": text,
            },
        },
        "hooks": None,
        "type": TYPE.DISPLAY_SPINNER,
        "interactionType": INTERACTION_TYPE.DISPLAY,
    }


def display_code(
    code: str,
    *,
    label: str = None,
    description: str = None,
    lang: LanguageName = None,
    style: Nullable.Style = None,
) -> ComponentReturn:
    id = Utils.generate_id()

    model_properties = {
        "code": code,
    }

    optional_properties = {
        "label": label,
        "description": description,
        "lang": lang,
    }

    for key, value in optional_properties.items():
        if value is not None:
            model_properties[key] = value

    return {
        "model": {
            "id": id,
            "style": style,
            "properties": model_properties,
        },
        "hooks": None,
        "type": TYPE.DISPLAY_CODE,
        "interactionType": INTERACTION_TYPE.DISPLAY,
    }


def display_image(src: str, *, style: Nullable.Style = None) -> ComponentReturn:
    id = Utils.generate_id()

    return {
        "model": {
            "id": id,
            "style": style,
            "properties": {
                "src": src,
            },
        },
        "hooks": None,
        "type": TYPE.DISPLAY_IMAGE,
        "interactionType": INTERACTION_TYPE.DISPLAY,
    }


def display_markdown(markdown: str, *, style: Nullable.Style = None) -> ComponentReturn:
    id = Utils.generate_id()

    return {
        "model": {
            "id": id,
            "style": style,
            "properties": {
                "markdown": markdown,
            },
        },
        "hooks": None,
        "type": TYPE.DISPLAY_MARKDOWN,
        "interactionType": INTERACTION_TYPE.DISPLAY,
    }


def display_pdf(
    file: Union[bytes, io.BufferedIOBase],
    *,
    label: Nullable.Str = None,
    description: Nullable.Str = None,
    annotations: Nullable.Annotations = None,
    scroll: Literal["vertical", "horizontal"] = None,
    style: Nullable.Style = None,
) -> ComponentReturn:
    id = Utils.generate_id()

    if isinstance(file, io.BufferedIOBase):
        file.seek(0)
        file_content = file.read()
    elif isinstance(file, bytes):
        file_content = file
    else:
        raise TypeError(
            "The 'file' argument must be of type 'bytes' or a bytes-like object that supports the read() method (e.g., BytesIO). "
            "Please provide the PDF content as bytes or a bytes-like object."
        )

    # Convert bytes to base64
    base64_pdf = base64.b64encode(file_content).decode("utf-8")
    base64_pdf_with_prefix = f"data:application/pdf;base64,{base64_pdf}"

    model_properties = {
        "base64": base64_pdf_with_prefix,
    }

    optional_properties = {
        "label": label,
        "description": description,
        "annotations": annotations,
        "scroll": scroll,
    }

    for key, value in optional_properties.items():
        if value is not None:
            model_properties[key] = value

    return {
        "model": {
            "id": id,
            "style": style,
            "properties": model_properties,
        },
        "hooks": None,
        "type": TYPE.DISPLAY_PDF,
        "interactionType": INTERACTION_TYPE.DISPLAY,
    }


def display_none() -> ComponentReturn:
    id = Utils.generate_id()

    return {
        "model": {
            "id": id,
            "style": None,
            "properties": {},
        },
        "hooks": None,
        "type": TYPE.DISPLAY_NONE,
        "interactionType": INTERACTION_TYPE.DISPLAY,
    }

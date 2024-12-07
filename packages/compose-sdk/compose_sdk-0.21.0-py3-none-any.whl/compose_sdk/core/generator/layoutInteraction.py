from typing import Union, Callable
from ..ui import (
    INTERACTION_TYPE,
    TYPE,
    Nullable,
    LAYOUT_ALIGN,
    LAYOUT_DIRECTION,
    LAYOUT_JUSTIFY,
    LAYOUT_ALIGN_DEFAULT,
    LAYOUT_DIRECTION_DEFAULT,
    LAYOUT_JUSTIFY_DEFAULT,
    LAYOUT_SPACING,
    LAYOUT_SPACING_DEFAULT,
    ComponentReturn,
    ValidatorResponse,
    VoidResponse,
)
from ..utils import Utils

Children = Union[ComponentReturn, list[ComponentReturn]]


def layout_stack(
    children: Children,
    *,
    direction: LAYOUT_DIRECTION = LAYOUT_DIRECTION_DEFAULT,
    justify: LAYOUT_JUSTIFY = LAYOUT_JUSTIFY_DEFAULT,
    align: LAYOUT_ALIGN = LAYOUT_ALIGN_DEFAULT,
    spacing: LAYOUT_SPACING = LAYOUT_SPACING_DEFAULT,
    style: Nullable.Style = None
) -> ComponentReturn:
    """
    A flexible container for arranging and styling its children. By default, it
    arranges its children in a vertical stack.
    """
    id = Utils.generate_id()

    return {
        "model": {
            "id": id,
            "children": children,
            "direction": direction,
            "justify": justify,
            "align": align,
            "spacing": spacing,
            "style": style,
            "properties": {},
        },
        "hooks": None,
        "type": TYPE.LAYOUT_STACK,
        "interactionType": INTERACTION_TYPE.LAYOUT,
    }


def layout_row(
    children: Children,
    *,
    justify: LAYOUT_JUSTIFY = LAYOUT_JUSTIFY_DEFAULT,
    align: LAYOUT_ALIGN = LAYOUT_ALIGN_DEFAULT,
    spacing: LAYOUT_SPACING = LAYOUT_SPACING_DEFAULT,
    style: Nullable.Style = None
) -> ComponentReturn:
    """
    A flexible container for arranging and styling its children. By default, it
    arranges its children in a horizontal row.
    """
    return layout_stack(
        children,
        direction="horizontal",
        justify=justify,
        align=align,
        spacing=spacing,
        style=style,
    )


def layout_distributed_row(
    children: Children,
    *,
    align: LAYOUT_ALIGN = "center",
    spacing: LAYOUT_SPACING = LAYOUT_SPACING_DEFAULT,
    style: Nullable.Style = None
) -> ComponentReturn:
    """
    A flexible container for arranging and styling its children. By default, it
    distributes its children in a row and maximizes the space between them.

    A common use case is for headers where you have text on the left and buttons
    on the right.
    """
    return layout_stack(
        children,
        direction="horizontal",
        justify="between",
        align=align,
        spacing=spacing,
        style=style,
    )


def layout_card(
    children: Children,
    *,
    direction: LAYOUT_DIRECTION = LAYOUT_DIRECTION_DEFAULT,
    justify: LAYOUT_JUSTIFY = LAYOUT_JUSTIFY_DEFAULT,
    align: LAYOUT_ALIGN = LAYOUT_ALIGN_DEFAULT,
    spacing: LAYOUT_SPACING = LAYOUT_SPACING_DEFAULT,
    style: Nullable.Style = None
) -> ComponentReturn:
    """
    A flexible container for arranging and styling its children. By default, it
    renders its children inside a card UI.
    """

    stack = layout_stack(
        children,
        direction=direction,
        justify=justify,
        align=align,
        spacing=spacing,
        style=style,
    )

    return {
        **stack,
        "model": {
            **stack["model"],
            "appearance": "card",
        },
    }


def layout_form(
    id: str,
    children: Children,
    *,
    direction: LAYOUT_DIRECTION = LAYOUT_DIRECTION_DEFAULT,
    justify: LAYOUT_JUSTIFY = LAYOUT_JUSTIFY_DEFAULT,
    align: LAYOUT_ALIGN = LAYOUT_ALIGN_DEFAULT,
    spacing: LAYOUT_SPACING = LAYOUT_SPACING_DEFAULT,
    style: Nullable.Style = None,
    clear_on_submit: bool = False,
    validate: Callable[[dict], ValidatorResponse] = None,
    on_submit: Callable[[dict], VoidResponse] = None
) -> ComponentReturn:
    """
    A flexible container for managing forms. The form manages input states, offers hooks
    to handle validation and submission, and groups input values into a single sanitized
    output object.

    The form can also be arranged and styled using the same options available to normal
    `ui.stack` components.

    The form can include non-input components such as text, sub-containers, etc. The form
    will automatically find the input components within its children and manage their
    states.
    """
    return {
        "model": {
            "id": id,
            "children": children,
            "direction": direction,
            "justify": justify,
            "align": align,
            "spacing": spacing,
            "style": style,
            "properties": {
                "hasOnSubmitHook": on_submit is not None,
                "hasValidateHook": validate is not None,
                "clearOnSubmit": clear_on_submit,
            },
        },
        "hooks": {
            "validate": validate,
            "onSubmit": on_submit,
        },
        "type": TYPE.LAYOUT_FORM,
        "interactionType": INTERACTION_TYPE.LAYOUT,
    }

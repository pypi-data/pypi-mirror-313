import pandas
from ...ui import (
    INTERACTION_TYPE,
    TYPE,
    TableColumns,
    Nullable,
    ComponentReturn,
    TableData,
)
from ..base import MULTI_SELECTION_MIN_DEFAULT, MULTI_SELECTION_MAX_DEFAULT


def get_model_actions(
    actions: Nullable.TableActions,
) -> Nullable.TableActionsWithoutOnClick:
    if actions is None:
        return None

    return [
        {key: value for key, value in action.items() if key != "on_click"}
        for action in actions
    ]


def get_hook_actions(actions: Nullable.TableActions) -> Nullable.TableActionsOnClick:
    if actions is None:
        return None

    return [action["on_click"] for action in actions]


def _table(
    id: str,
    data: TableData,
    *,
    label: Nullable.Str = None,
    required: bool = True,
    description: Nullable.Str = None,
    initial_selected_rows: list[int] = [],
    validate: Nullable.Callable = None,
    on_change: Nullable.Callable = None,
    columns: Nullable.TableColumns = None,
    actions: Nullable.TableActions = None,
    style: Nullable.Style = None,
    min_selections: int = MULTI_SELECTION_MIN_DEFAULT,
    max_selections: int = MULTI_SELECTION_MAX_DEFAULT,
    allow_select: bool = True,
) -> ComponentReturn:

    if not isinstance(initial_selected_rows, list):
        raise TypeError(
            f"initial_selected_rows must be a list for table component, got {type(initial_selected_rows).__name__}"
        )

    if not all(isinstance(row, int) for row in initial_selected_rows):
        raise ValueError("All elements in initial_selected_rows must be integers")

    return {
        "model": {
            "id": id,
            "label": label,
            "description": description,
            "required": required,
            "hasValidateHook": validate is not None,
            "style": style,
            "properties": {
                "initialSelectedRows": initial_selected_rows,
                "hasOnSelectHook": on_change is not None,
                "data": data,
                "columns": columns,
                "actions": get_model_actions(actions),
                "minSelections": min_selections,
                "maxSelections": max_selections,
                "allowSelect": allow_select,
            },
        },
        "hooks": {
            "validate": validate,
            "onSelect": on_change,
            "onRowActions": get_hook_actions(actions),
        },
        "type": TYPE.INPUT_TABLE,
        "interactionType": INTERACTION_TYPE.INPUT,
    }


def table(
    id: str,
    data: TableData,
    *,
    label: Nullable.Str = None,
    required: bool = True,
    description: Nullable.Str = None,
    initial_selected_rows: list[int] = [],
    validate: Nullable.Callable = None,
    on_change: Nullable.Callable = None,
    columns: Nullable.TableColumns = None,
    actions: Nullable.TableActions = None,
    style: Nullable.Style = None,
    min_selections: int = MULTI_SELECTION_MIN_DEFAULT,
    max_selections: int = MULTI_SELECTION_MAX_DEFAULT,
    allow_select: bool = True,
) -> ComponentReturn:
    return _table(
        id,
        data,
        label=label,
        required=required,
        description=description,
        initial_selected_rows=initial_selected_rows,
        validate=validate,
        on_change=on_change,
        style=style,
        columns=columns,
        actions=actions,
        min_selections=min_selections,
        max_selections=max_selections,
        allow_select=allow_select,
    )


def dataframe(
    id: str,
    df: pandas.DataFrame,
    *,
    label: Nullable.Str = None,
    required: bool = True,
    description: Nullable.Str = None,
    initial_selected_rows: list[int] = [],
    validate: Nullable.Callable = None,
    on_change: Nullable.Callable = None,
    actions: Nullable.TableActions = None,
    style: Nullable.Style = None,
    min_selections: int = MULTI_SELECTION_MIN_DEFAULT,
    max_selections: int = MULTI_SELECTION_MAX_DEFAULT,
    allow_select: bool = True,
) -> ComponentReturn:

    # Replace empty values in the dataframe with None
    df = df.replace({None: "", pandas.NA: "", float("nan"): ""})

    # Create the "columns" array
    columns: TableColumns = [{"key": col, "label": col} for col in df.columns]

    # Create the "table" array
    table: TableData = df.to_dict(orient="records")  # type: ignore

    return _table(
        id,
        table,
        label=label,
        required=required,
        description=description,
        initial_selected_rows=initial_selected_rows,
        validate=validate,
        on_change=on_change,
        style=style,
        columns=columns,
        actions=actions,
        min_selections=min_selections,
        max_selections=max_selections,
        allow_select=allow_select,
    )

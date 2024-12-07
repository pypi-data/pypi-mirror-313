from typing import Callable, Dict, Literal, Union, TypedDict
from typing_extensions import NotRequired
from datetime import datetime
from .validator_response import VoidResponse

TABLE_COLUMN_FORMAT = Literal[
    # Oct 14, 1983
    "date",
    # Oct 14, 1983, 10:14 AM
    "datetime",
    # 1,023,456
    "number",
    # $1,023,456.00
    "currency",
    # ✅ or ❌
    "boolean",
    # Stringify the value and render as is
    "string",
]


class AdvancedTableColumn(TypedDict):
    key: str
    label: NotRequired[str]
    format: NotRequired[TABLE_COLUMN_FORMAT]
    width: NotRequired[str]


TableColumn = Union[str, AdvancedTableColumn]

TableColumns = list[TableColumn]

TableDataRow = Dict[str, Union[str, int, float, bool, datetime, None]]
TableData = list[TableDataRow]


class TableActionWithoutOnClick(TypedDict):
    label: str
    surface: NotRequired[bool]


class TableAction(TableActionWithoutOnClick):
    on_click: Callable[[TableDataRow], VoidResponse]


TableActionOnClick = TableAction["on_click"]

TableActions = list[TableAction]
TableActionsWithoutOnClick = list[TableActionWithoutOnClick]
TableActionsOnClick = list[TableActionOnClick]

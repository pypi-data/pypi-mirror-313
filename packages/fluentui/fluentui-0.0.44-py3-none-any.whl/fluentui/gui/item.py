from typing import Any, Callable

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QStandardItem, QColor, QFont
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined


class StandardItem(QStandardItem):
    def __init__(self, text=None,
                 children: list[QStandardItem] = None, *,
                 rows: int = None,
                 columns=1,
                 flags: Qt.ItemFlag = None,
                 enabled=True,
                 text_align: Qt.AlignmentFlag = None,
                 size_hint: int = None,
                 background='',
                 foreground='',
                 font: QFont = None,
                 ):
        if rows is None:
            super().__init__(rows)
        else:
            super().__init__(rows, columns=columns)

        if font: self.setFont(font)
        if not enabled: self.setEnabled(enabled)
        if flags is not None: self.setFlags(flags)
        if text: self.setData(text, Qt.ItemDataRole.DisplayRole)
        if background: self.setBackground(QColor(background))
        if foreground: self.setBackground(QColor(foreground))
        if text_align is not None: self.setTextAlignment(text_align)
        if size_hint is not None: self.setSizeHint(QSize(0, size_hint))

        for x in children or []:
            self.appendRow(x)


class TreeItem:
    def __init__(self, data: list = None,
                 children: list['TreeItem'] = None, *,
                 flags=Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable,
                 union_flags: Qt.ItemFlag = None,
                 check_state: dict[int, Qt.CheckState] = None,
                 parent: 'TreeItem' = None,
                 ):
        self.d = data or []
        self.flags = flags if union_flags is None else flags | union_flags
        self.check_state = check_state or {}
        self.parent = parent
        self.children: list[TreeItem] = []

        if Qt.ItemFlag.ItemIsUserCheckable in self.flags:
            state = self.check_state.get(0, Qt.CheckState.Unchecked)
            self.check_state[0] = state
        self.append(children or [])

    def set_check_state(self, column: int, state: Qt.CheckState):
        self.check_state[column] = state
        self.set_children_check_state(column, state)
        self.set_parent_check_stata(column)

    def set_children_check_state(self, column: int, state: Qt.CheckState) -> None:
        for x in self.children:
            x.check_state[column] = state
            x.set_children_check_state(column, state)

    def set_parent_check_stata(self, column: int) -> None:
        parent = self.parent
        if not parent or parent.parent is None or not parent.children:
            return

        children = parent.children
        if all(x.check_state[column] == Qt.CheckState.Checked for x in children):
            parent.check_state[column] = Qt.CheckState.Checked
        elif any(x.check_state[column] in (Qt.CheckState.Checked, Qt.CheckState.PartiallyChecked) for x in children):
            parent.check_state[column] = Qt.CheckState.PartiallyChecked
        else:
            parent.check_state[column] = Qt.CheckState.Unchecked

        self.parent.set_parent_check_stata(column)

    def append(self, children: 'list[TreeItem] | TreeItem') -> None:
        if isinstance(children, TreeItem): children = [children]
        for x in children:
            x.parent = self
            self.children.append(x)

    def child(self, row: int) -> 'TreeItem':
        return self.children[row] if 0 <= row < self.child_count() else None

    def child_count(self) -> int:
        return len(self.children)

    def row(self) -> int:
        return self.parent.children.index(self) if self.parent else 0

    def column_count(self) -> int:
        return len(self.d)

    def data(self, column: int) -> Any:
        return self.d[column]


class ColumnField(FieldInfo):
    def __init__(self, default=PydanticUndefined, *,
                 default_factory: Callable[[], Any] = None,
                 title='',
                 alias='',
                 visible=False
                 ):
        self.visible = visible
        super().__init__(
            default=default,
            default_factory=default_factory,
            title=title,
            alias=alias
        )

    def __set_name__(self, owner, name):
        self.title = name

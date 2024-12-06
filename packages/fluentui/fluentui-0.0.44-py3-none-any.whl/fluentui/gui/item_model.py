from typing import Any, Callable, Iterable

from PySide6.QtCore import QAbstractTableModel, QObject, QModelIndex, QPersistentModelIndex, Qt
from PySide6.QtGui import QStandardItem, QStandardItemModel
from polars import DataFrame, concat

from .item import TreeItem, ColumnField
from ..core import ItemModel, AbsItemModelMix


class StandardModel(AbsItemModelMix, QStandardItemModel):
    def __init__(self,
                 parent: QObject = None,
                 rows: int = None,
                 columns: int = None,
                 items: Iterable[QStandardItem] = None
                 ):
        if rows is not None and columns is not None:
            super().__init__(rows, columns, parent)
        else:
            super().__init__(parent)
        self.appendRow(items or [])

    def appendRow(self, items: QStandardItem | Iterable[QStandardItem]) -> None:
        for x in items if isinstance(items, Iterable) else [items]:
            super().appendRow(x)


class ColumnModel(AbsItemModelMix, QAbstractTableModel):
    def __init__(self,
                 parent: QObject = None, *,
                 table: list[ColumnField] = None,
                 data: list[dict] = None
                 ):
        super().__init__(parent)
        self.table = table or []
        self.fields = [x.title for x in self.table]

        self.df = DataFrame(schema={x.title: x.annotation for x in self.table})
        if data is not None:
            self.append(data)

    def rowCount(self, parent=QModelIndex()) -> int:
        """ 行数 """
        return self.df.height

    def columnCount(self, parent=QModelIndex()) -> int:
        """ 列数 """
        return self.df.width

    def headerData(self, section: int, orientation=Qt.Orientation.Horizontal, role=Qt.ItemDataRole.DisplayRole) -> Any:
        """ 头数据 """
        if orientation == Qt.Orientation.Horizontal:
            if role == Qt.ItemDataRole.DisplayRole and self.table:
                return self.table[section].alias
            if role == Qt.ItemDataRole.TextAlignmentRole:
                return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        return super().headerData(section, orientation, role)

    def removeRows(self, row: int, count: int, parent=QModelIndex()) -> None:
        """ 移除行 """
        self.beginRemoveRows(parent, row, row + count - 1)
        self.df = self.df[:row].extend(self.df[row + count:])
        self.endRemoveRows()
        return True

    def data(self, index: QModelIndex, role=Qt.ItemDataRole.DisplayRole) -> Any:
        """ 项目数据 """
        if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            return self.df[index.row(), index.column()]
        return None

    def setData(self, index: QModelIndex, value: object, role=Qt.ItemDataRole.EditRole) -> bool:
        """ 设置数据 """
        if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            self.df[index.row(), index.column()] = value
            self.dataChanged.emit(index, index, [role])
            return True
        return False

    def append(self, data: dict | list[dict] = None, row=-1, remove_rows=False) -> None:
        """ 添加行 """
        if remove_rows:
            self.removeRows(0, self.rowCount())

        if isinstance(data, list) and not data:
            return

        fields = {x.title: x.default for x in self.table}
        data = data or [fields]
        data = data if isinstance(data, list) else [data]

        first = row if row >= 0 else self.rowCount()
        last = first + len(data) - 1
        data = [fields | x for x in data]  # 确保模型排序

        self.beginInsertRows(QModelIndex(), first, last)

        df = DataFrame(data)
        empty = self.df.is_empty()
        self.df = df if empty else concat([self.df[:first], df, self.df[first:]])

        self.endInsertRows()

    def update(self, data: dict, row: int | QModelIndex, roles: list = None):
        row = row if isinstance(row, int) else row.row()
        roles = roles or [Qt.ItemDataRole.DisplayRole]

        for column, name in enumerate(self.fields):
            if name not in data:
                continue
            index = self.index(row, column)
            self.df[row, column] = data[name]
            self.dataChanged.emit(index, index, roles)

    def __getitem__(self, index: int | tuple | QModelIndex | QPersistentModelIndex) -> dict | object:
        if isinstance(index, tuple):
            if isinstance((row := index[0]), QModelIndex):
                row = row.row()
            return self.df[row, index[1]]
        elif isinstance(index, QModelIndex | QPersistentModelIndex):
            return self.df[index.row(), index.column()]
        return self.df[index].to_dicts()[0]  # int


class RowModel(ColumnModel):
    def columnCount(self, parent=QModelIndex()) -> int:
        return 1

    def data(self, index: QModelIndex, role=Qt.ItemDataRole.DisplayRole) -> object | Callable:
        """ 项目数据 """
        if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            return self.__data(index.row())
        return super().data(index, role)

    def setData(self, index: QModelIndex, value: object, role=Qt.ItemDataRole.EditRole) -> bool:
        """ 设置数据 """
        succeed = role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole)
        if succeed:
            self.df[index.row(), index.column()] = value
            self.dataChanged.emit(index, index, [role])
        return succeed

    def update(self, data: dict, row: int | QModelIndex, roles: list = None):
        row = row if isinstance(row, int) else row.row()
        roles = roles or [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole]
        updated = False

        for column, name in enumerate(self.fields):
            if name in data:  # 仅更新存在字段
                updated = True
                self.df[row, column] = data[name]

        if updated:
            index = self.index(row, 0)
            self.dataChanged.emit(index, index, roles)

    def __getitem__(self, index: int | tuple | QModelIndex | QPersistentModelIndex) -> dict | object:
        if self.df.is_empty():
            return None
        if isinstance(index, tuple):
            if isinstance((row := index[0]), QModelIndex):
                row = row.row()
            return self.df[row, index[1]]
        row = index if isinstance(index, int) else index.row()
        return self.df[row].to_dicts()[0]

    def __data(self, row: int):
        return lambda key: self.df[row, key]


class TreeModel(ItemModel):
    def __init__(self, headers: list[str] = None,
                 items: TreeItem | list[TreeItem] = None,
                 parent: QObject = None
                 ):
        super().__init__(parent)
        if not headers and items:
            first = items[0] if isinstance(items, list) else items
            headers = [''] * first.column_count()
        self.root = TreeItem(headers, items)

    def index(self, row: int, column=0, parent=QModelIndex()) -> QModelIndex:
        if self.hasIndex(row, column, parent):
            item = parent.internalPointer() if parent.isValid() else self.root
            if child := item.child(row):
                return self.createIndex(row, column, child)
        return QModelIndex()

    def parent(self, index: QModelIndex) -> QModelIndex:
        if index.isValid():
            parent: TreeItem = index.internalPointer().parent
            if parent != self.root:
                return self.createIndex(parent.row(), 0, parent)
        return QModelIndex()

    def rowCount(self, parent=QModelIndex()) -> int:
        item = parent.internalPointer() if parent.isValid() else self.root
        return item.child_count()

    def columnCount(self, parent=QModelIndex()) -> int:
        item = self.item(parent) if parent.isValid() else self.root
        return item.column_count()

    def data(self, index: QModelIndex, role=Qt.ItemDataRole.DisplayRole) -> Any:
        if role == Qt.ItemDataRole.DisplayRole:
            return self.item(index).data(index.column())
        if role == Qt.ItemDataRole.CheckStateRole:
            item = self.item(index)
            if item.flags & Qt.ItemFlag.ItemIsUserCheckable:
                return item.check_state.get(index.column(), None)
        return None

    def setData(self, index: QModelIndex, value: Any, role=Qt.ItemDataRole.EditRole) -> bool:
        if role == Qt.ItemDataRole.CheckStateRole:
            item = self.item(index)
            state = Qt.CheckState(value)
            if (item.flags & Qt.ItemFlag.ItemIsUserTristate) and state == Qt.CheckState.PartiallyChecked:
                state = Qt.CheckState.Checked
            item.set_check_state(index.column(), state)
            self.dataChanged.emit(index, index, [role])
            self.layoutChanged.emit()
        return False

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        return self.item(index).flags

    def headerData(self, section: int, orien: Qt.Orientation, role=Qt.ItemDataRole.DisplayRole) -> Any:
        if orien == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.root.data(section)
        return None

    def item(self, row: int | QModelIndex, column: int = None) -> TreeItem:
        """ item(row: int | QModelIndex, column=0) """
        if isinstance(row, int):
            return self.index(row, column or 0).internalPointer()
        index = row if column is None else row.siblingAtColumn(column)
        return index.internalPointer()

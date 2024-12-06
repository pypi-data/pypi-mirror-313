from PySide6.QtCore import QAbstractItemModel, QModelIndex, QPersistentModelIndex, QAbstractProxyModel, \
    QAbstractTableModel, QSortFilterProxyModel, QObject

ModelIndex: type[QModelIndex | QPersistentModelIndex] = QModelIndex | QPersistentModelIndex


class AbsItemModelMix:
    def index(self, row: int | ModelIndex, column: int = None, parent=QModelIndex()) -> QModelIndex:
        if isinstance(row, QModelIndex):
            column = row.column() if column is None else column
            row = row.row()
        return super().index(row, column or 0, parent)

    def hasIndex(self, row: int, column=0, parent=QModelIndex()) -> bool:
        return super().hasIndex(row, column, parent)


class ItemModel(AbsItemModelMix, QAbstractItemModel):
    ...


class AbsProxyModelMix(AbsItemModelMix):
    ...


class AbsProxyModel(AbsProxyModelMix, QAbstractProxyModel):
    ...


class AbsTableModel(AbsItemModelMix, QAbstractTableModel):
    ...


class SortFilterProxyModelMix(AbsProxyModelMix):
    def __init__(self, source: ItemModel = None, parent: QObject = None):
        super().__init__(parent)
        if source is not None:
            self.setSourceModel(source)


class SortFilterProxyModel(SortFilterProxyModelMix, QSortFilterProxyModel):
    ...

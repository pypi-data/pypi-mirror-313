from typing import Callable, Iterable

from PySide6.QtCore import Qt, QModelIndex, QAbstractItemModel, QItemSelectionModel, QPoint
from PySide6.QtWidgets import QAbstractItemView, QTableWidget, QAbstractItemDelegate, QListView, QTreeView, QTableView, \
    QWidget, QTreeWidget, QTreeWidgetItem, QFrame

from .container import AbsScrollAreaMix
from .item_delete import TableItemDelegate
from ..gui import TreeModel


class AbsItemViewMix(AbsScrollAreaMix):
    def __init__(self, *,
                 frame_shape=QFrame.Shape.NoFrame,
                 model: QAbstractItemModel = None,
                 auto_scroll=False,
                 auto_scroll_margin=0,
                 edit_triggers=QAbstractItemView.EditTrigger.NoEditTriggers,
                 selection_behavior=QAbstractItemView.SelectionBehavior.SelectRows,
                 selection_mode=QAbstractItemView.SelectionMode.SingleSelection,
                 hor_scroll_mode=QAbstractItemView.ScrollMode.ScrollPerPixel,
                 ver_scroll_mode=QAbstractItemView.ScrollMode.ScrollPerPixel,
                 hor_single_step: int = None,  # 滚动速度，通常对应于用户按下 [箭头键]
                 ver_single_step: int = None,
                 delegate: QAbstractItemDelegate = None,
                 cell_clicked: Callable[[QModelIndex], None] = None,
                 double_clicked: Callable[[QModelIndex], None] = None,
                 row_changed: Callable[[QModelIndex, QModelIndex], None] = None,
                 **kwargs
                 ):
        super().__init__(frame_shape=frame_shape, **kwargs)

        if double_clicked: self.doubleClicked.connect(double_clicked)
        if cell_clicked:
            clicked = self.cellClicked if isinstance(self, QTableWidget) else self.clicked
            clicked.connect(cell_clicked)

        self.setEditTriggers(edit_triggers)
        self.setAutoScroll(auto_scroll)
        self.setAutoScrollMargin(auto_scroll_margin)
        self.setHorizontalScrollMode(hor_scroll_mode)
        self.setVerticalScrollMode(ver_scroll_mode)
        self.setSelectionMode(selection_mode)
        self.setSelectionBehavior(selection_behavior)

        if hor_single_step is not None: self.horizontalScrollBar().setSingleStep(hor_single_step)
        if ver_single_step is not None: self.verticalScrollBar().setSingleStep(ver_single_step)

        if model: self.setModel(model)
        if delegate: self.setItemDelegate(delegate)
        if row_changed: self.selectionMode().currentRowChanged.connect(row_changed)

    def currentChanged(self, current: QModelIndex, previous: QModelIndex) -> None:
        super().currentChanged(current, previous)
        if current.parent() != previous.parent() or current.row() != previous.row():
            ...  # currentRowChanged

    def setCurrentIndex(self, index: QModelIndex | int) -> None:
        if not (m := self.model()):
            return
        index = m.index(index, 0) if isinstance(index, int) else index
        super().setCurrentIndex(index)

    def selectionMode(self) -> QItemSelectionModel:
        return super().selectionMode()


class ListView(AbsItemViewMix, QListView):
    def __init__(self, *, uniform_item_sizes=False, spacing=0, **kwargs):
        super().__init__(**kwargs)
        self.setSpacing(spacing)
        self.setUniformItemSizes(uniform_item_sizes)


class TableViewMix(AbsItemViewMix):
    def __init__(self, *args,
                 default_row_height=32,  # 默认行高
                 default_col_width: int = None,  # 默认列宽
                 word_wrap=True,
                 sorting_enabled=False,
                 auto_scroll=False,
                 hor_header_visible=True,
                 ver_header_visible=True,
                 stretch_last_section=False,
                 **kwargs
                 ):
        super().__init__(*args, **kwargs)
        hor_header = self.horizontalHeader()
        ver_header = self.verticalHeader()

        if default_col_width:
            hor_header.setDefaultSectionSize(default_col_width)  # 默认列宽
        hor_header.setVisible(hor_header_visible)

        ver_header.setDefaultSectionSize(default_row_height)  # 默认行高
        ver_header.setVisible(ver_header_visible)

        self.setShowGrid(False)
        self.setWordWrap(word_wrap)
        self.setAutoScroll(auto_scroll)
        self.setSortingEnabled(sorting_enabled)
        self.horizontalHeader().setStretchLastSection(stretch_last_section)


class TableView(TableViewMix, QTableView):
    def __init__(self, **kwargs):
        kwargs.setdefault('delegate', TableItemDelegate())
        super().__init__(**kwargs)

    def indexAt(self, pos: QPoint | QWidget) -> QModelIndex:
        if isinstance(pos, QWidget):
            global_pos = pos.mapToGlobal(pos.pos())
            pos = self.viewport().mapFromGlobal(global_pos)
        return super().indexAt(pos)

    def rowAt(self, y: int | QWidget) -> int:
        if isinstance(y, QWidget):
            global_pos = y.mapToGlobal(y.pos())
            y = self.viewport().mapFromGlobal(global_pos).y()
        return super().rowAt(y)


class TableWidget(TableViewMix, QTableWidget):
    def __init__(self, rows=0, columns=0, **kwargs):
        super().__init__(**kwargs)
        self.setRowCount(rows)
        self.setColumnCount(columns)


class TreeWidgetItem(QTreeWidgetItem):
    def __init__(self, parent: QTreeWidgetItem | QTreeWidget = None,
                 strings: Iterable[str] = None,
                 typ=QTreeWidgetItem.ItemType.Type, *,
                 flags: Qt.ItemFlag = None,
                 union_flags: Qt.ItemFlag = None,
                 check_state: tuple[int, Qt.CheckState] = None,
                 children: list[QTreeWidgetItem] = None
                 ):
        super().__init__(parent, strings, typ)
        if flags is not None: self.setFlags(flags)
        if union_flags is not None: self.setFlags(self.flags() | union_flags)
        if check_state: self.setCheckState(*check_state)
        self.addChildren(children or [])


class TreeViewMix(AbsItemViewMix):
    def __init__(self,
                 indentation=20,
                 header_hidden=False,
                 expand_all=False,
                 root_is_decorated=True,
                 items_expandable=True,
                 expands_on_double_click=False,
                 **kwargs
                 ):
        super().__init__(**kwargs)
        self.setIndentation(indentation)
        self.setHeaderHidden(header_hidden)
        self.setItemsExpandable(items_expandable)
        self.setRootIsDecorated(root_is_decorated)
        self.setExpandsOnDoubleClick(expands_on_double_click)
        if kwargs.get('model', None) and expand_all: self.expandAll()


class TreeView(TreeViewMix, QTreeView):
    def model(self) -> TreeModel:
        return super().model()


class TreeWidget(TreeViewMix, QTreeWidget):
    def __init__(self,
                 items: list[QTreeWidgetItem] | QTreeWidgetItem = None,
                 **kwargs
                 ):
        expand_all = kwargs.pop('expand_all', False)
        super().__init__(**kwargs)

        items = [items] if isinstance(items, QTreeWidgetItem) else items
        self.addTopLevelItems(items or [])
        if expand_all: self.expandAll()

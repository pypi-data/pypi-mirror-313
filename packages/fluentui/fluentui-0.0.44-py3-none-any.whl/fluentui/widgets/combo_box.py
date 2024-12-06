from typing import Callable, Any

from PySide6.QtGui import QStandardItemModel, QWheelEvent, Qt
from PySide6.QtWidgets import QComboBox, QAbstractItemView, QListView

from .container import WidgetMix


class ComboBox(WidgetMix, QComboBox):
    def __init__(self, *,
                 max_visible=20,
                 items: list[str | dict | tuple] = None,
                 editable=False,
                 index: int | str = None,
                 on_index_changed: Callable[[int], None] = None,
                 **kwargs):
        super().__init__(**kwargs)

        self.setEditable(editable)
        self.setMaxVisibleItems(max_visible)
        self.view().setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)

        if items:
            if isinstance(items[0], str):
                self.addItems(items)
            else:
                for x in items:
                    if not isinstance(x, tuple):  # dict
                        x = tuple(x.items())[0]
                    self.addItem(x[1], x[0])

        if isinstance(index, int):
            self.setCurrentIndex(index)
        elif isinstance(index, str):
            self.setCurrentText(index)

        if on_index_changed: self.currentIndexChanged.connect(on_index_changed)

    def setItems(self, items: list[dict], block_clear_signal=False) -> None:
        if block_clear_signal:
            self.blockSignals(True)
        self.clear()
        if block_clear_signal:
            self.blockSignals(False)

        if not items: return

        if isinstance(items[0], str):
            self.addItems(items)
            return

        for x in items:
            if not isinstance(x, tuple):  # dict
                x = tuple(x.items())[0]
            self.addItem(x[1], x[0])

    def selectText(self, text: str, edit=False) -> int:
        if edit:
            self.setEditText(text)
        else:
            self.setCurrentText(text)
        return self.currentIndex()

    def currentData(self, default: object = None, role=Qt.ItemDataRole.UserRole) -> Any:
        value = super().currentData(role)
        return default if value is None else value

    def current_edit_data(self, default: object = None, role=Qt.ItemDataRole.UserRole) -> Any:
        text = self.currentText()
        value = super().itemData(self.findText(text), role)
        return default if value is None else value

    def selectData(self, data: object) -> int:
        if (index := self.findData(data)) >= 0:
            return self.setCurrentIndex(index)
        return index

    def view(self) -> QListView:
        return super().view()

    def model(self) -> QStandardItemModel:
        return super().model()

    def wheelEvent(self, e: QWheelEvent):
        e.ignore()

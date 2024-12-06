import inspect
from typing import Callable

from PySide6.QtCore import QModelIndex, QObject, QSize
from PySide6.QtGui import QColor, QPainter, QPalette, QBrush
from PySide6.QtWidgets import QStyleOptionViewItem, QStyledItemDelegate, QStyle, QItemDelegate, QWidget

from ..assets import Light
from ..core import ModelIndex, Qt


class ItemDelegateMix(QItemDelegate):
    def __init__(self, parent: QObject = None,
                 size_hint: Callable[[QStyleOptionViewItem, ModelIndex, Callable], QSize] = None,
                 create_editor: Callable[[QWidget, QStyleOptionViewItem, ModelIndex, Callable], QWidget] = None,
                 update_editor_geometry: Callable[[QWidget, QStyleOptionViewItem, ModelIndex, Callable], None] = None,
                 ):
        super().__init__(parent)
        self._size_hint_fn = size_hint
        self._create_editor_fn = create_editor
        self._update_editor_geometry_fn = update_editor_geometry

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: ModelIndex) -> QWidget:
        return self.__call(self._create_editor_fn, super().createEditor, parent, option, index)

    def updateEditorGeometry(self, parent: QWidget, option: QStyleOptionViewItem, index: ModelIndex) -> None:
        self.__call(self._update_editor_geometry_fn, super().updateEditorGeometry, parent, option, index)

    def sizeHint(self, option: QStyleOptionViewItem, index: ModelIndex) -> QSize:
        return self.__call(self._size_hint_fn, super().sizeHint, option, index)

    @staticmethod
    def __call(fn: Callable, super_fn: Callable, *args):
        if not fn: return super_fn(*args)
        if len(inspect.signature(fn).parameters) == len(args) + 1:
            return fn(*args, super_fn)
        return fn(*args)

class TableItemDelegate(ItemDelegateMix, QStyledItemDelegate):
    def __init__(self, parent: QObject = None, **kwargs):
        super().__init__(parent, **kwargs)
        self.bg_high = QColor('#ebf3fc')  # 高亮背景颜色
        self.line_color = QColor(Light.Stroke)  # 线条颜色
        self.fg = QColor(Light.Text)

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        fg = index.data(Qt.DataRole.Foreground) or self.fg
        bg = index.data(Qt.DataRole.Background) or self.bg_high

        p: QPalette = option.palette
        p.setColor(QPalette.ColorRole.Highlight, bg)
        p.setColor(QPalette.ColorRole.HighlightedText, fg)

        if option.state & QStyle.StateFlag.State_HasFocus:
            option.state ^= QStyle.StateFlag.State_HasFocus

        super().paint(painter, option, index)

        if self.line_color:
            rect = option.rect
            painter.setPen(self.line_color)
            painter.drawLine(rect.bottomLeft(), rect.bottomRight())


class ListItemDelegate(ItemDelegateMix, QItemDelegate):
    def __init__(self, parent: QObject = None, **kwargs):
        super().__init__(parent, **kwargs)
        self.bg_high = QColor('#ebf3fc')  # 高亮背景颜色
        self.fg = QColor(Light.Text)

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        bg: QBrush | QColor = index.data(Qt.DataRole.Background)
        if isinstance(bg, QBrush): bg = bg.color()
        bg = self.bg_high if not bg or bg.alpha() == 0 else QColor(bg)

        fg = index.data(Qt.DataRole.Foreground)
        fg = QColor(fg) if fg else self.fg

        p: QPalette = option.palette
        p.setColor(QPalette.ColorRole.Highlight, bg)
        p.setColor(QPalette.ColorRole.HighlightedText, fg)

        if (state := option.state) & QStyle.StateFlag.State_HasFocus:
            option.state ^= QStyle.StateFlag.State_HasFocus
        elif state & QStyle.StateFlag.State_MouseOver and bg.alpha() > 0:
            painter.fillRect(option.rect, bg)

        super().paint(painter, option, index)

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QBoxLayout, QLayout, QWidget, QGridLayout

from .container import WidgetMix
from ..core import Margin


class Spacing(int): ...


class Stretch(int): ...


class Layout:
    def __init__(self, *args,
                 parent=None,
                 spacing=0,
                 margin='0',
                 row_span=1,
                 column_span=1,
                 align=Qt.AlignmentFlag(0),
                 **kwargs):
        self.row_span = row_span
        self.column_span = column_span

        super().__init__(parent=parent, *args, **kwargs)
        self.setAlignment(align)
        self.setSpacing(spacing)
        self.setContentsMargins(Margin(margin))


class BoxLayout(Layout, QBoxLayout):
    def __init__(self, *children: QLayout | QWidget | Stretch | Spacing,
                 dir_: QBoxLayout.Direction,
                 **kwargs):
        super().__init__(dir_, **kwargs)
        if children and isinstance(first := children[0], list):
            children = first

        for x in children or ():
            self.addWidget(x)

    def addWidget(self, w: QLayout | QWidget | Stretch | Spacing, align=Qt.AlignmentFlag(0)) -> None:
        if isinstance(w, QLayout):
            return self.addLayout(w)
        if isinstance(w, Stretch):
            return self.addStretch(w)
        if isinstance(w, Spacing):
            return self.addSpacing(w)

        if isinstance(w, WidgetMix):
            align = w.align_self
        super().addWidget(w, alignment=align)


class Row(BoxLayout):
    def __init__(self, *children, **kwargs):
        super().__init__(*children, dir_=QBoxLayout.Direction.LeftToRight, **kwargs)


class Column(BoxLayout):
    def __init__(self, *children, **kwargs):
        super().__init__(*children, dir_=QBoxLayout.Direction.TopToBottom, **kwargs)


class Grid(Layout, QGridLayout):
    def __init__(self, *children: QWidget | QLayout | list, **kwargs):
        super().__init__(**kwargs)
        for row, x in enumerate(children):
            if isinstance(x, list):
                for column, y in enumerate(x):
                    self.addWidget(y, row, column)
                continue
            self.addWidget(x, row, 0)

    def addWidget(self, w: QWidget | QLayout,
                  row: int, column=0,
                  row_span=1, column_span=1,
                  alignment=Qt.AlignmentFlag(0)):
        if isinstance(w, Layout | WidgetMix):
            row_span, column_span = w.row_span, w.column_span

        if isinstance(w, QWidget):
            super().addWidget(w, row, column, row_span, column_span, alignment)
            return
        self.addLayout(w, row, column, row_span, column_span, alignment)

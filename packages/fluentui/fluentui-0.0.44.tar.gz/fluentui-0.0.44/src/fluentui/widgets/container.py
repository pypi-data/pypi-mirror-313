from typing import Callable

from PySide6.QtCore import Signal, QEvent
from PySide6.QtGui import QAction
from PySide6.QtGui import QMouseEvent, QCloseEvent, QKeyEvent, QColor
from PySide6.QtWidgets import QWidget, QSizePolicy, QLayout, QGraphicsDropShadowEffect, QToolBox, QTabWidget, \
    QStackedWidget, QFrame, QScrollArea, QSplitter, QColorDialog, QFileDialog, QDialog

from ..assets import QssSheet, Qss
from ..core import Qt, ObjectMix, Margin

WidgetSizeMax = 16777215


class WidgetMix(ObjectMix):
    on_close = Signal()
    on_key_enter_pressed = Signal(QWidget)
    on_clicked = Signal(QWidget)

    def __init__(
            # a、b、c、d、e、f、g、h、i、j、k、l、m、n、o、p、q、r、s、t、u、v、w、x、y、z
            self, *args,
            attrs: Qt.WidgetAttribute | list[Qt.WidgetAttribute | list[Qt.WidgetAttribute]] = None,
            color_scheme='auto',  # light, dark, auto
            shadow_effect: QGraphicsDropShadowEffect = None,
            enabled=True,
            hidden=False,
            menu_policy=Qt.ContextMenuPolicy.Default,
            layout_dir: Qt.LayoutDirection = None,
            margin='0',
            mouse_tracking=False,
            parent: QWidget = None,
            propes: dict = None,
            qss: dict = None,
            tooltip='',
            win_title='',
            win_flags: Qt.WindowType = None,

            # 大小参数
            width: int = None, height: int = None, size: str | int | tuple = None,
            min_w: int = None, min_h: int = None,
            max_w: int = None, max_h: int = None,
            hor_stretch=0, ver_stretch=0,

            # 布局参数
            row_span=1,
            column_span=1,
            align_self=Qt.AlignmentFlag(0),

            closed: Callable = None,
            destroyed: Callable[[], None] = None,
            clicked: Callable[[QWidget], None] = None,
            key_enter_pressed: Callable[[QWidget], None] = None,
            **kwargs
    ):
        if not (layout := None) and args:
            first = args[0]
            if first is None or first == () or isinstance(first, QLayout):
                args, layout = args[1:], first
        super().__init__(*args, parent=parent, **kwargs)

        self.row_span = row_span
        self.column_span = column_span
        self.align_self = align_self
        self.qss = Qss()

        # # 设置属性
        self.__init_properties(attrs, propes, qss, color_scheme)
        self.__init_size(width, height, size, min_w, min_h, max_w, max_h, hor_stretch, ver_stretch)

        # 订阅信号
        if closed: self.on_close.connect(closed)
        if clicked: self.on_clicked.connect(clicked)
        if destroyed: self.destroyed.connect(destroyed)
        if key_enter_pressed: self.on_key_enter_pressed.connect(key_enter_pressed)

        # 对象属性
        if hidden: self.setHidden(hidden)
        if win_flags is not None: self.setWindowFlags(win_flags)
        if shadow_effect:
            if not shadow_effect.parent(): shadow_effect.setParent(self)
            self.setGraphicsEffect(shadow_effect)
        self.setContentsMargins(Margin(margin))
        self.setEnabled(enabled)
        self.setToolTip(tooltip)
        self.setWindowTitle(win_title)
        self.setMouseTracking(mouse_tracking)
        self.setContextMenuPolicy(menu_policy)

        if layout:
            if layout_dir is not None:
                self.setLayoutDirection(layout_dir)
            self.setLayout(layout)

    def setStyleSheet(self, qss: dict | Qss) -> None:
        self.qss = Qss(qss) if isinstance(qss, dict) else qss
        super().setStyleSheet(f'{self.__class__.__name__} {self.qss.build()}')

    def mergeStyleSheet(self, qss: dict | Qss) -> None:
        self.qss |= qss
        super().setStyleSheet(f'{self.__class__.__name__} {self.qss.build()}')

    def event(self, e: QEvent) -> bool:
        accepted = super().event(e)
        if e.type() == QEvent.Type.Polish:
            QssSheet.apply_theme(self)
            self.polishEvent(e)
        return accepted

    def polishEvent(self, _: QEvent):
        ...

    def addActions(self, *actions: QAction):
        if actions and isinstance(actions[0], list):
            actions = actions[0]
        for x in actions:
            if not x.parent():
                x.setParent(self)
            super().addAction(x)

    def closeEvent(self, e: QCloseEvent) -> None:
        super().closeEvent(e)
        if self.isSignalConnected(self.on_close):
            self.on_close.emit()

    def keyPressEvent(self, e: QKeyEvent) -> None:
        super().keyPressEvent(e)
        if e.key() in (Qt.Key.Enter, Qt.Key.Return):
            if self.isSignalConnected(self.on_key_enter_pressed):
                self.on_key_enter_pressed.emit(self)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        super().mousePressEvent(e)
        self.setProperty('mousePressed', True)

    def mouseReleaseEvent(self, e: QMouseEvent):
        super().mouseReleaseEvent(e)
        if self.property('mousePressed'):
            self.setProperty('mousePressed', False)
            if self.isSignalConnected(self.on_clicked):
                self.on_clicked.emit(self)

    def __init_properties(self,
                          attrs: Qt.WidgetAttribute | set[Qt.WidgetAttribute | set[Qt.WidgetAttribute]] = None,
                          propes: dict = None,
                          qss: dict = None,
                          color_scheme='auto',
                          ):
        propes = propes or {}
        setattr(self, '_init_color_scheme', color_scheme)
        if isinstance(self, QDialog):
            self.setAttribute(Qt.WidgetAttribute.DeleteOnClose)

        if isinstance(attrs, set):
            for x in attrs:
                self.setAttribute(x, False)
        elif attrs is not None:
            for x in attrs if isinstance(attrs, list) else [attrs]:
                if isinstance(x, set):
                    for a in x: self.setAttribute(a, False)
                    continue
                self.setAttribute(x)

        propes |= {'custom-qss': qss, 'mousePressed': False}
        for k, v in propes.items():
            self.setProperty(k, v)

    def __init_size(self, w: int | str = None, h: int | str = None,
                    size: str | int | tuple = None,
                    min_w: int = None, min_h: int = None,
                    max_w: int = None, max_h: int = None,
                    hor_stretch=0, ver_stretch=0
                    ):

        if min_w is not None or min_h is not None:
            self.setMinimumSize(min_w or WidgetSizeMax, min_h or WidgetSizeMax)
        if max_w is not None or max_h is not None:
            self.setMaximumSize(max_w or WidgetSizeMax, max_h or WidgetSizeMax)

        if isinstance(w, str) or isinstance(h, str) or hor_stretch > 0 or ver_stretch > 0:
            policy = self.sizePolicy()
            if isinstance(w, str): policy.setHorizontalPolicy(QSizePolicy.Policy.Expanding)
            if isinstance(h, str): policy.setVerticalPolicy(QSizePolicy.Policy.Expanding)
            if hor_stretch > 0: policy.setHorizontalStretch(hor_stretch)
            if ver_stretch > 0: policy.setVerticalStretch(ver_stretch)
            self.setSizePolicy(policy)

        if size is not None:
            if isinstance(size, str):
                if size[-1] == ',':  # 仅指定宽。如: '800,'
                    self.resize(int(size[:-1]), self.height())
                elif size[0] == ',':  # 仅指定高。如: ',800'
                    self.resize(self.width(), int(size[1:]))
                else:
                    size = [int(x) for x in size.split(',')]
                    size = size * 2 if len(size) == 1 else size
                    self.resize(*size)
            else:
                if isinstance(size, int): size = (size, size)
                self.setFixedSize(*size)
        if isinstance(w, int) and isinstance(h, int):
            self.setFixedSize(w, h)
        elif isinstance(w, int):
            self.setFixedWidth(w)
        elif isinstance(h, int):
            self.setFixedHeight(h)


class Widget(WidgetMix, QWidget):
    def __init__(self, layout: QLayout = None, **kwargs):
        super().__init__(layout, **kwargs)
        self.setAttribute(Qt.WidgetAttribute.StyledBackground)


class InvisWidget(Widget):
    ...


class FrameMix(WidgetMix):
    def __init__(self,
                 frame_shape: QFrame.Shape = None,
                 line_width: int = None,
                 **kwargs
                 ):
        super().__init__(**kwargs)
        if frame_shape is not None: self.setFrameShape(frame_shape)
        if line_width is not None: self.setLineWidth(line_width)


class Frame(FrameMix, QFrame):
    ...


class AbsScrollAreaMix(FrameMix):
    def __init__(self,
                 hor_scroll_bar_policy: Qt.ScrollBarPolicy = None,
                 ver_scroll_bar_policy: Qt.ScrollBarPolicy = None,
                 **kwargs):
        super().__init__(**kwargs)
        if hor_scroll_bar_policy is not None:
            self.setHorizontalScrollBarPolicy(hor_scroll_bar_policy)
        if ver_scroll_bar_policy is not None:
            self.setVerticalScrollBarPolicy(ver_scroll_bar_policy)


class ScrollArea(AbsScrollAreaMix, QScrollArea):
    ...


class ToolBox(FrameMix, QToolBox):
    def __init__(self, *children: dict, **kwargs):
        super().__init__(**kwargs)
        for x in children:
            if icon := x.get('icon'):
                self.addItem(x['widget'], icon, x['text'])
                continue
            self.addItem(x['widget'], x['text'])


class Splitter(FrameMix, QSplitter):
    def __init__(self, *split: QWidget,
                 sizes: list[int] = None,
                 handle_width=5,
                 children_collapsible=True,
                 orient=Qt.Orientation.Hor,
                 **kwargs
                 ):
        super().__init__(**kwargs)
        self.setOrientation(orient)
        self.setHandleWidth(handle_width)
        self.setChildrenCollapsible(children_collapsible)

        if sizes: self.setSizes(sizes or [])
        for x in split or []: self.addWidget(x)


class StackedView(FrameMix, QStackedWidget):
    def __init__(self, *stack: QWidget, **kwargs):
        super().__init__(**kwargs)
        for x in stack or ():
            self.addWidget(x)


class TabWidget(WidgetMix, QTabWidget):
    def __init__(self,
                 *children: dict,
                 position=QTabWidget.TabPosition.North,
                 current_changed: Callable[[int], None] = None,
                 **kwargs
                 ):
        super().__init__(**kwargs)
        if current_changed: self.currentChanged.connect(current_changed)

        self.setTabPosition(position)
        for x in children:
            if icon := x.get('icon', None):
                self.addTab(x['widget'], icon, x['label'])
                continue
            self.addTab(x['widget'], x['label'])


class DialogMix(WidgetMix):
    def __init__(self,
                 layout: QLayout = None, *,
                 accepted: Callable = None,
                 rejected: Callable = None,
                 finished: Callable[[int], None] = None,
                 **kwargs
                 ):
        super().__init__(layout, **kwargs)
        if accepted: self.accepted.connect(accepted)
        if rejected: self.rejected.connect(rejected)
        if finished: self.finished.connect(finished)


class Dialog(DialogMix, QDialog):
    ...


class FileDialog(DialogMix, QFileDialog):
    def __init__(self, caption='', directory='', filter_='', **kwargs):
        super().__init__(caption=caption, directory=directory, filter=filter_, **kwargs)


class ColorDialog(DialogMix, QColorDialog):
    def __init__(self, color: QColor | str = '#fff',
                 color_selected: Callable[[QColor], None] = None,
                 **kwargs
                 ):
        super().__init__(color, **kwargs)
        if color_selected: self.colorSelected.connect(color_selected)

    @staticmethod
    def getColor(initial='#fff',
                 parent=None,
                 title='',
                 options=QColorDialog.ColorDialogOption.ShowAlphaChannel
                 ) -> QColor:
        return super().getColor(QColor(initial), parent, title, options)

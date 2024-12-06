from typing import Callable

from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QPushButton, QCheckBox, QRadioButton, QAbstractButton

from .container import WidgetMix
from ..core import Qt


class AbsButtonMix(WidgetMix):
    def __init__(self,
                 text: str = '', *,
                 icon: str | QPixmap | QIcon = None,
                 icon_size: int | tuple[int, int] = None,
                 checked=False,
                 checkable: bool = None,
                 auto_exclusive: bool = None,
                 on_toggled: Callable[[bool], None] = None,
                 **kwargs
                 ):
        if isinstance(icon_size, int):
            icon_size = (icon_size, icon_size)

        super().__init__(**kwargs)
        self.on_key_enter_pressed.connect(self.on_clicked.emit)

        if on_toggled: self.toggled.connect(on_toggled)
        if icon_size is not None: self.setIconSize(QSize(*icon_size))
        if icon: self.setIcon(QIcon(icon) if isinstance(icon, str) else icon)
        if checkable is not None: self.setCheckable(checkable)
        if auto_exclusive is not None: self.setAutoExclusive(auto_exclusive)
        self.setText(text)
        self.setChecked(checked)


class AbsButton(AbsButtonMix, QAbstractButton):
    ...


class Button(AbsButtonMix, QPushButton):
    def __init__(self, text='', *,
                 default: bool = None,
                 auto_default: bool = None,
                 **kwargs
                 ):
        super().__init__(text, **kwargs)
        self.setFlat(True)
        if default is not None: self.setDefault(default)
        if auto_default is not None: self.setAutoDefault(auto_default)


class PrimaryButton(Button):
    ...


class DangerButton(Button):
    ...


class SubtleButton(Button):
    ...


class InvisButton(Button):
    ...


class CheckBox(AbsButtonMix, QCheckBox):
    def __init__(self, text='', *,
                 tristate=False,
                 state=Qt.CheckState.Unchecked,
                 state_changed: Callable[[Qt.CheckState], ...] = None,
                 **kwargs
                 ):
        super().__init__(text, **kwargs)
        if state_changed: self.stateChanged.connect(state_changed)
        self.setTristate(tristate)
        self.setCheckState(state)


class RadioButton(AbsButtonMix, QRadioButton):
    ...

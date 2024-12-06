from typing import Callable, Any

from PySide6.QtGui import QAction, QIcon, QPixmap


class Action(QAction):
    def __init__(self, text='', *,
                 icon: str | QIcon | QPixmap = None,
                 icon_text='',
                 data: Any = None,
                 enabled=True,
                 checked=False,
                 checkable=False,
                 separator=False,
                 toggled: Callable[[bool], ...] = None,
                 triggered: Callable[[bool], ...] | Callable = None):
        if icon:
            flag = not isinstance(icon, QIcon)
            super().__init__(QIcon(icon) if flag else icon, text)
        else:
            super().__init__(text)

        self.setEnabled(enabled)
        self.setChecked(checked)
        self.setCheckable(checkable)
        self.setIconText(icon_text)
        self.setSeparator(separator)

        if data is not None: self.setData(data)
        if toggled: self.toggled.connect(toggled)
        if triggered: self.triggered.connect(triggered)

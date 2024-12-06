from typing import Callable

from PySide6.QtGui import QColor, QIcon, QPixmap
from PySide6.QtWidgets import QSystemTrayIcon, QGraphicsDropShadowEffect, QMenu


class ShadowEffect(QGraphicsDropShadowEffect):
    def __init__(self, blur_radius=1.0,
                 offset=(8.0, 8.0),
                 color=QColor.fromRgbF(0.247059, 0.247059, 0.247059, 0.705882),
                 parent=None
                 ):
        super().__init__(parent)
        self.setBlurRadius(blur_radius)
        self.setOffset(*offset)
        self.setColor(color)


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self,
                 menu: QMenu = None,
                 icon: str | QIcon | QPixmap = None,
                 tooltip='',
                 activated: Callable[[QSystemTrayIcon.ActivationReason], None] = None,
                 show=False,
                 **kwargs
                 ):
        if isinstance(icon, str): icon = QIcon(icon)
        super().__init__(**kwargs)
        if activated: self.activated.connect(activated)

        self.setToolTip(tooltip)
        if icon: self.setIcon(icon)
        if menu: self.setContextMenu(menu)
        if show: self.show()

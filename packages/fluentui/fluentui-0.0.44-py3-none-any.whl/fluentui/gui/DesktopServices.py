from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices


class DesktopServices(QDesktopServices):
    @classmethod
    def openUrl(cls, url: QUrl | str) -> bool:
        super().openUrl(url if isinstance(url, QUrl) else QUrl(url))

from typing import Any

from PySide6.QtCore import Qt, QSize, QByteArray
from PySide6.QtGui import QColor, QFontDatabase, QFont, QIcon, QIconEngine, QImage
from PySide6.QtGui import QPixmap

from ..core import Size


class FontDatabase(QFontDatabase):
    @classmethod
    def applicationFontFamilies(cls, fileNames: list[str]) -> list[str]:
        return [super().applicationFontFamilies(y) for
                y in [cls.addApplicationFont(x) for x in fileNames]]


class Font(QFont):
    def __init__(self,
                 families='Segoe UI, Microsoft YaHei UI, PingFang SC', *,
                 pixel=0,
                 point=0,
                 weight=QFont.Weight.Normal,
                 italic=False,
                 ):
        super().__init__([x.strip() for x in families.split(',')], -1, weight, italic)
        if pixel > 0: self.setPixelSize(pixel)
        if point > 0: self.setPointSize(point)


class Color(QColor):
    def __init__(self, name='', alpha: float = 1):
        super().__init__(name)
        self.setAlphaF(alpha)


class Pixmap(QPixmap):
    def __init__(self,
                 size: int | tuple[int, int] | Size = None,
                 filename='', format_: str = None, flags=Qt.ImageConversionFlag.AutoColor,
                 xpm: list[str] = None,
                 other: QPixmap = None,
                 variant: Any = None,
                 ):
        """
        QPixmap()
        QPixmap(size)
        QPixmap(fileName, format: str = None, flags=Qt.AutoColor)
        QPixmap(xpm: list[str])
        QPixmap(other: QPixmap)
        QPixmap(variant: Any)
        """
        if size is not None:
            super().__init__(size if isinstance(size, QSize) else Size(size))
        elif filename:
            super().__init__(filename, format_, flags)
        elif xpm:
            super().__init__(xpm)
        elif other is not None:
            super().__init__(other)
        elif variant is not None:
            super().__init__(variant)
        else:
            super().__init__()

    @staticmethod
    def from_data(data: bytes | bytearray | QByteArray,
                  format_: str = None,
                  flags=Qt.ImageConversionFlag.AutoColor
                  ) -> 'Pixmap':
        pixmap = Pixmap()
        pixmap.loadFromData(data, format_, flags)
        return pixmap


class Icon(QIcon):
    def __init__(self, icon: str | QPixmap | QIconEngine | QIcon | QImage = None):
        if icon is None:
            super().__init__()
        else:
            super().__init__(icon)

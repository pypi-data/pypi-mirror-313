from hashlib import md5
from pathlib import Path
from typing import Callable

from PySide6.QtCore import QBuffer, QIODevice, Signal, QByteArray
from PySide6.QtGui import QPixmap, QResizeEvent
from PySide6.QtNetwork import QNetworkReply

from .widget import Label
from ..core import Qt
from ..gui import Pixmap
from ..network import Request


class ImageLabel(Label):
    completed = Signal(QPixmap)
    CACHE_PATH = Path.home() / f'AppData/Local/images_cache'
    CACHE_PATH.mkdir(parents=True, exist_ok=True)

    def __init__(self,
                 src='',
                 completed: Callable[[QPixmap], None] = None,
                 **kwargs
                 ):
        super().__init__(align=Qt.Alignment.Center, **kwargs)

        self.origin_pixmap = QPixmap()
        self.source: str | Path | bytes | QPixmap = None
        if completed: self.completed.connect(completed)

        self.__reply: QNetworkReply = None
        self.destroyed.connect(lambda: self.__reply and self.__reply.abort())

        self.setPixmap(QPixmap(':/fluentui/icons/image-256.svg'))
        self.request(src)

    def request(self, src: str | Path | bytes | QPixmap) -> None:
        if not src or src == self.source: return
        self.source = src

        if isinstance(src, QPixmap):
            if not src.isNull():
                self.__completed(src)
            return
        elif isinstance(src, Path | bytes):
            data = src.read_bytes() if isinstance(src, Path) else src
            self.__completed(Pixmap.from_data(data))
            return

        # srcType => str
        ext = Path(src).suffix.split('?')[0]  # 图片扩展名
        if not (path := self.CACHE_PATH / (md5(src.encode()).hexdigest() + ext)).exists():
            if (p := Path(src)).exists():  # 如果缓存路径不存在，则判断系统路径
                path = p

        if path.exists():
            self.request(path)
            return

        self.__reply = Request(src).send(
            lambda r:
            self.__downloaded(path, r.readAll().data())
        )

    def setPixmap(self, pixmap: QPixmap) -> None:
        super().setPixmap(pixmap.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.Smooth
        ))

    def isNull(self) -> bool:
        return self.origin_pixmap.isNull()

    def thumbnail(self, fmt='JPG', quality=-1) -> bytes:
        """ 缩略图数据。质量因子必须在 [0,100] 或 -1 的范围内 """
        if self.origin_pixmap.isNull():
            return b''

        buffer = QBuffer(data := QByteArray())
        buffer.open(QIODevice.OpenModeFlag.WriteOnly)
        self.origin_pixmap.save(buffer, fmt, quality)

        buffer.close()
        return data.data()

    def origin(self, format_='JPG') -> bytes:
        """ 原图数据 """
        return self.thumbnail(format_, 100)

    def resizeEvent(self, e: QResizeEvent) -> None:
        super().resizeEvent(e)
        if self.origin_pixmap and not self.origin_pixmap.isNull():
            self.setPixmap(self.origin_pixmap)

    def __completed(self, pixmap: QPixmap):
        if pixmap.isNull(): return

        self.origin_pixmap = pixmap
        self.setPixmap(pixmap)

        if self.isSignalConnected(self.completed):
            self.completed.emit(pixmap)

    def __downloaded(self, path: Path, data: bytes) -> None:
        """ 下载完成 """
        if not data: return

        p = Pixmap.from_data(data)
        if p.isNull() or path.write_bytes(data) <= 0:  return

        self.data = data
        self.__completed(p)

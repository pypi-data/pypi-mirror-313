from PySide6.QtCore import QFile, QIODevice


class File(QFile):
    def __init__(self, name: str, *,
                 mode: QIODevice.OpenModeFlag = None,
                 open_=False,
                 parent=None
                 ):
        super().__init__(name, parent)
        if mode is not None and open_:
            self.open(mode)

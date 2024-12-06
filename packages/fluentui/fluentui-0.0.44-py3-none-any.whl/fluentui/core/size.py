from PySide6.QtCore import QSize


class Size(QSize):
    def __init__(self, *size: int | tuple[int, int] | QSize):
        if len(size) == 1:
            if isinstance(first := size[0], int):
                size = (first, first)
            elif isinstance(first, tuple):
                size = (first[0], first[1])
        super().__init__(*size)

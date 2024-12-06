from PySide6.QtCore import QMargins


class Margin(QMargins):
    def __init__(self, *margin: str | QMargins):
        if margin and isinstance(margin[0], str):
            n = len(m := [int(x) for x in margin[0].split(' ')])
            if n == 1:  # top
                margin = (m[0], m[0], m[0], m[0])
            elif n == 2:  # top, right
                margin = (m[1], m[0], m[1], m[0])
            elif n == 3:  # top, right, bottom
                margin = (m[1], m[0], m[1], m[2])
            else:  # top, right, bottom, left
                margin = (m[3], m[0], m[1], m[2])
        super().__init__(*margin)

    def merge(self, top: int = None,
              right: int = None,
              bottom: int = None,
              left: int = None
              ) -> 'Margin':
        if top is not None: self.setTop(top)
        if right is not None: self.setRight(right)
        if bottom is not None: self.setBottom(bottom)
        if left is not None: self.setLeft(left)
        return self

    def __str__(self) -> str:
        return (f'Margins{{top: {self.top()}, right: {self.right()}, '
                f'bottom: {self.bottom()}, left: {self.left()}}}')

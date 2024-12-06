import sys
from typing import Callable, Any

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication

from ..core import Qt
from ..gui import FontDatabase


class App(QApplication):
    def __init__(self, font: QFont = None,
                 font_families: list[str] = None,
                 quit_on_last_window_closed=True,
                 about_to_quit: Callable[[], None] = None,
                 color_scheme=Qt.ColorScheme.Light,
                 ):
        self.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)
        super().__init__(sys.argv)

        if font_families: FontDatabase.applicationFontFamilies(font_families)
        if font: self.setFont(font)
        if about_to_quit: self.aboutToQuit.connect(about_to_quit)
        if color_scheme is not None: self.styleHints().setColorScheme(color_scheme)

        self.setQuitOnLastWindowClosed(quit_on_last_window_closed)

    def exec(self) -> Any:
        return sys.exit(super().exec())

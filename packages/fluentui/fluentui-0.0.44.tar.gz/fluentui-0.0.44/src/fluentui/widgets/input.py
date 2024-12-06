from operator import setitem
from typing import Callable

from PySide6.QtGui import QImage, QColor, QValidator, QIntValidator, QTextDocument
from PySide6.QtNetwork import QNetworkReply
from PySide6.QtWidgets import QTextEdit, QLineEdit
from bs4 import BeautifulSoup
from selectolax.parser import HTMLParser

from .container import WidgetMix, AbsScrollAreaMix
from ..core import Qt, Url
from ..network import Request


class Input(WidgetMix, QLineEdit):
    def __init__(self, text: object = '', *,
                 placeholder='',
                 read_only=False,
                 text_changed: Callable[[str], None] = None,
                 validator: QValidator = None,
                 **kwargs
                 ):
        super().__init__(f'{text}', **kwargs)
        if text_changed: self.textChanged.connect(text_changed)
        if validator is not None: self.setValidator(validator)

        self.setReadOnly(read_only)
        self.setPlaceholderText(placeholder)

    def setText(self, text: object, block_signals=False):
        super().setText(f'{text}')
        if block_signals: self.blockSignals(True)
        self.setCursorPosition(0)
        if block_signals: self.blockSignals(False)


class IntInput(Input):
    def __init__(self, text='', **kwargs):
        super().__init__(text, **kwargs)
        self.setValidator(QIntValidator())


class Textarea(AbsScrollAreaMix, QTextEdit):
    def __init__(self,
                 text='', *,
                 placeholder='',
                 text_color='',
                 read_only=False,
                 undo_redo_enabled=True,
                 accept_rich_text=True,
                 text_change: Callable[[], None] = None,
                 align: Qt.AlignmentFlag = None,
                 selection_changed: Callable = None,
                 cursor_position_changed: Callable = None,
                 **kwargs
                 ):
        super().__init__(**kwargs)
        self.requests: list[QNetworkReply] = []
        self.destroyed.connect(
            lambda:
            next((None for x in self.requests if x.abort()), None)
        )

        if text_change: self.textChanged.connect(text_change)
        if selection_changed: self.selectionChanged.connect(selection_changed)
        if cursor_position_changed: self.cursorPositionChanged.connect(cursor_position_changed)

        if align is not None: self.setAlignment(align)
        if text_color: self.setTextColor(QColor(text_color))
        self.document().setDefaultStyleSheet('img { max-width: 100%; }')
        self.setText(text)
        self.setReadOnly(read_only)
        self.setAcceptRichText(accept_rich_text)
        self.setUndoRedoEnabled(undo_redo_enabled)
        self.setPlaceholderText(placeholder)

    def setText(self, text: str):
        super().setText(text)

        doc = self.document()
        html = HTMLParser(text)

        for img in html.css('img[src^="http://"], img[src^="https://"]'):
            url = Url(src := img.attributes['src'])
            if url.isEmpty() or not url.isValid():
                continue

            name = url.toString()
            if doc.resource(QTextDocument.ResourceType.ImageResource, name):
                continue

            # 占位图片源，防止请求重复的图片
            doc.addResource(QTextDocument.ResourceType.ImageResource, name, True)
            reply = Request.get(src, finished=self.__downloaded)
            self.requests.append(reply)

    def setDocument(self, document: QTextDocument):
        document.setDefaultStyleSheet('img { max-width: 100%; }')
        document.resource(QTextDocument.ResourceType.ImageResource, "name")
        super().setDocument(document)

    def content(self) -> str:
        if self.document().isEmpty():
            return ''

        contents = []
        for p in BeautifulSoup(self.toHtml(), 'lxml').find_all('p'):
            del p['style']
            for span in p.find_all('span'):
                style: str = span['style']
                if setitem(span, 'style', style) or style == "":
                    span.unwrap()
            text = f'{p}'.rstrip()
            contents.append(f'<p>{'\u200B'}</p>' if text == '<p><br/></p>' else text)
        return '\n'.join(x for x in contents)

    def __downloaded(self, reply: QNetworkReply):
        self.requests.remove(reply)
        name = reply.url().toString()

        image = QImage()
        if not image.loadFromData(reply.readAll()):
            return

        try:
            doc = self.document()
            doc.addResource(QTextDocument.ResourceType.ImageResource, name, image)
            doc.setPageSize(doc.pageSize())  # 刷新内容
        except (RuntimeError, ValueError) as _:
            ...

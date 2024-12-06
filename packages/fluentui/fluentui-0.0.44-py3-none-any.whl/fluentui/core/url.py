from PySide6.QtCore import QUrl


class Url(QUrl):
    def toString(self, options=QUrl.ComponentFormattingOption.PrettyDecoded):
        if not isinstance(options, QUrl.ComponentFormattingOption):
            options = QUrl.ComponentFormattingOption(options)
        return super().toString(options)

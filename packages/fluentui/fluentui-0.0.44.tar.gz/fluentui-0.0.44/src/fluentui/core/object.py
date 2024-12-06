from PySide6.QtCore import Signal, QMetaMethod, SIGNAL, QRegularExpression, QObject

from .namespace import Qt


class ObjectMix:
    def __init__(self,
                 *args,
                 key='',
                 parent=None,
                 props: dict = None,
                 ):
        super().__init__(parent=parent, *args)
        self.setObjectName(key)
        for name, value in (props or {}).items():
            self.setProperty(name, value)

    def findChildren(self, typ: type,
                     name='',
                     options=Qt.FindChildOption.Recursively,
                     pattern: QRegularExpression | str = None
                     ) -> list[QObject]:
        """
        (type, name='', options=Qt.FindChildOption.Recursively) -> list[QObject]\n
        (type, pattern: QRegularExpression | str, options=Qt.FindChildOption.Recursively) -> list[QObject]
        """
        if pattern is None:
            return super().findChildren(typ, name, options)
        return super().findChildren(typ, pattern, options)

    def isSignalConnected(self, signal: Signal):
        return super().isSignalConnected(QMetaMethod.fromSignal(signal))

    def receivers(self, signal: Signal | str) -> int:
        if isinstance(signal, Signal):
            signal = QMetaMethod.fromSignal(signal).methodSignature()
            signal = signal.toStdString()
        elif isinstance(signal, Signal):
            signal = f'{signal}'
        else:
            signal = f'{getattr(self.__class__, signal)}'
        return super().receivers(SIGNAL(signal))

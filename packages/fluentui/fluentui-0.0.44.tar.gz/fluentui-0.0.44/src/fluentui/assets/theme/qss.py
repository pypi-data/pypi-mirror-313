from dataclasses import dataclass, field
from enum import Enum
from typing import Self
from weakref import WeakKeyDictionary

from PySide6.QtWidgets import QWidget, QApplication

from .color import Light, Dark

_styled_widgets = WeakKeyDictionary[QWidget, str]()


@dataclass
class Qss:
    d: dict = field(default_factory=dict)

    def merge(self, a: 'dict | Qss') -> Self:
        self.d = self.join(a if isinstance(a, dict) else a.d, self.d)
        return self

    @classmethod
    def join(cls, dst: dict, src: dict) -> dict:
        for name, elem in dst.items():
            if isinstance(elem, dict):
                elem = cls.join(elem, src.get(name, {}).copy())
            src[name] = elem
        return src

    def build(self, d: dict = None) -> str:
        if not (d := d or self.d):
            return ''

        base, elems = [], {}
        for k, v in d.items():
            if isinstance(v, dict):
                elems[k] = v
                continue
            base.append(f"    {k}: {v};")

        result = "{\n" + "\n".join(base) + "\n}"
        return result + ''.join(f"\n{k} {self.build(v)}" for k, v in elems.items())

    def __or__(self, other: 'dict | Qss') -> Self:
        return self.merge(other)


class QssSheet(Enum):
    Widget = 'Widget'
    InvisWidget = 'InvisWidget'
    Dialog = 'Dialog'

    Slider = 'Slider'

    Input = 'Input'
    SpinBox = 'SpinBox'

    Button = 'Button'
    PrimaryButton = 'PrimaryButton'
    SubtleButton = 'SubtleButton'
    DangerButton = 'DangerButton'
    InvisButton = 'InvisButton'
    RadioButton = 'RadioButton'

    Label = 'Label'
    Line = 'Line'

    Textarea = 'Textarea'
    ComboBox = 'ComboBox'
    AbsItemViewMix = 'AbsItemViewMix'

    def __call__(self, theme='light') -> dict:
        """ 返回对应类名的主题样式 """
        d = LightQss if theme == 'light' else DarkQss
        return getattr(d, self.name, {}).copy()

    def apply(self, w: QWidget, theme='auto'):
        if notin := w not in _styled_widgets:
            theme = w.__dict__.pop('_init_color_scheme')

        if theme == 'auto':
            if parent := w.parent():
                theme = _styled_widgets.get(parent, 'light')  # 获取父主题
                if _styled_widgets.get(w, None) == 'auto':
                    _styled_widgets.pop(w)
            else:
                theme = QApplication.styleHints().colorScheme().name.lower()

        if notin or theme != 'auto':
            _styled_widgets[w] = theme  # 记录 widget 的主题
            if notin: w.destroyed.connect(lambda: _styled_widgets.pop(w, None))

        qss = Qss(self(theme)) | (w.property('custom-qss') or {})
        if not qss.d: return

        w.setStyleSheet(qss)

    @classmethod
    def toggle_theme(cls, w: QWidget, theme: str):
        for x in w.findChildren(QWidget):
            if _styled_widgets.get(x, '') == 'auto':
                cls.apply_theme(w, theme)

    @classmethod
    def apply_theme(cls, widget: QWidget, theme='auto', typ=None) -> None:
        if typ is QWidget: return

        c = typ or widget.__class__
        if (name := c.__name__) in cls:
            cls(name).apply(widget, theme)
            return

        for x in c.__bases__:
            cls.apply_theme(widget, theme, x)
            if x.__name__ in cls:
                return


class LightQss:
    Widget = {'background': Light.Background}
    Dialog = {'background': Light.Background}
    InvisWidget = {'background': Light.Transparent}

    Label = {'color': Light.Text}
    Line = {'background': Light.Stroke}

    Button = {
        'color': Light.Text,
        'background': Light.Background,
        'padding': '5 12',
        'border': f'1 solid {Light.Stroke}',
        'border-radius': Light.Rounded,
        'font-weight': 600,
        ':hover': {'background': Light.Hover, 'border-color': '#c7c7c7'},
        ':pressed': {'background': Light.Pressed, 'border-color': '#b3b3b3'},
        ':disabled': {'color': Light.TextDisabled, 'background': '#f0f0f0', 'border-color': '#e0e0e0'}
    }

    RadioButton = {
        'spacing': '11',
        'background': Light.Transparent,
        'padding': '6 8',
        '::indicator': {
            'width': '16',
            'height': '16',
            'image': 'url(:/fluentui/icons/radio-uncheck-16.svg)'
        },
        '::indicator:hover': {
            'image': 'url(:/fluentui/icons/radio-uncheck-hover-16.svg)'
        },
        '::indicator:pressed': {
            'image': 'url(:/fluentui/icons/radio-uncheck-pressed-16.svg)'
        },
        '::indicator:checked': {
            'image': 'url(:/fluentui/icons/radio-checked-16.svg)'
        },
        '::indicator:checked:hover': {
            'image': 'url(:/fluentui/icons/radio-checked-hover-16.svg)'
        },
        '::indicator:checked:pressed': {
            'image': 'url(:/fluentui/icons/radio-checked-pressed-16.svg)'
        }
    }

    PrimaryButton = Button | {
        'color': Light.Background,
        'background': Light.Primary,
        'border-color': Light.Transparent,
        ':hover': {'background': Light.PrimaryHover},
        ':pressed': {'background': Light.PrimaryPressed},
    }

    DangerButton = PrimaryButton | {
        'color': Light.Background,
        'background': Light.Danger,
        ':hover': {'background': Light.DangerHover},
        ':pressed': {'background': Light.DangerPressed},
    }

    SubtleButton = Button | {
        'background': Light.Transparent,
        'border-color': Light.Transparent,
        ':hover': {'background': Light.Hover},
        ':pressed': {'background': Light.Pressed},
    }

    InvisButton = SubtleButton | {
        ':hover': {'color': Light.Primary, 'background': Light.Transparent},
        ':pressed': {'color': Light.PrimaryHover, 'background': Light.Transparent},
    }

    Input = {
        'color': Light.Text,
        'padding': '4 10',
        'border': f'1 solid {Light.Stroke}',
        'border-bottom': f'1 solid {Light.StrokeAccessible}',
        'border-radius': Light.Rounded,
        ':read-only, :disabled': {
            'color': Light.TextDisabled,
            'background': Light.Background,
            'border-bottom-color': Light.Stroke,
        },
        ':focus': {'border-bottom': f'2 solid {Light.Primary}'}
    }

    SpinBox = {
        'color': Light.Text,
        'padding': '4 0 4 -1',
        'border': f'1 solid {Light.Stroke}',
        'border-bottom': f'1 solid {Light.StrokeAccessible}',
        'border-radius': Light.Rounded,
        '::up-arrow': {'image': f'url(:/fluentui/icons/chevron-up-16.svg)'},
        '::down-arrow': {'image': f'url(:/fluentui/icons/chevron-down-16.svg)'},
        '::up-button': {
            'width': 24,
            'padding-top': '2',
            'border-top-right-radius': Light.Rounded,
        },
        '::down-button': {
            'width': 24,
            'padding-bottom': '2',
            'border-bottom-right-radius': Light.Rounded,
        },
        '::up-button:hover, ::down-button:hover': {
            'background': Light.Hover
        },
        '::up-button:pressed, ::down-button:pressed': {
            'background': Light.Pressed
        },
        ':read-only, :disabled': {
            'color': Light.TextDisabled,
            'background': Light.Background,
            'border-bottom-color': Light.Stroke,
        }
    }

    Slider = {
        'padding': '0 10',
        'QSlider::groove:horizontal': {
            'height': 4,
            'background': '#616161',
            'border-radius': 2
        },
        'QSlider::handle:horizontal': {
            'width': '20;',
            'height': '20;',
            'margin': '-8 -10;',
            'image': 'url(:/fluentui/icons/slider-20.svg)'
        },
        'QSlider::handle:horizontal:hover': {
            'image': 'url(:/fluentui/icons/slider-hover-20.svg)'
        },
        'QSlider::sub-page:horizontal': {
            'background': '#0f6cbd'
        }
    }

    ComboBox = {
        'color': Light.Text,
        'padding': '4 10 4 11',
        'border': f'1 solid {Light.Stroke}',
        'border-radius': Light.Rounded,
        ':disabled': {
            'background': '#fafafa',
            'color': Light.TextDisabled,
            'border-color': Light.Stroke
        },
        'ComboBox:editable': {
            'padding': '4 10 4 9'
        },
        'QAbstractItemView::item': {'padding': '4 0', 'color': Light.Text},
        '::drop-down': {'border': 'none', 'width': '32'},
        '::down-arrow': {
            'right': 4,
            'image': f'url(:/fluentui/icons/chevron-down-20.svg)'
        }
    }

    Textarea = {
        'color': Light.Text,
        'padding': '6 8',
        'border': f'1 solid {Light.Stroke}',
        'border-radius': Light.Rounded,
    }

    AbsItemViewMix = {
        'border': 'none'
    }


class DarkQss(LightQss):
    Widget = {
        'background': Dark.Background
    }

    Button = {
        'color': Dark.Text,
        'background': Dark.Background,
        'padding': '5 12',
        'border': f'1 solid {Dark.Stroke}',
        'border-radius': Light.Rounded,
        'font-weight': 600,
        ':hover': {'background': Dark.Hover, 'border-color': '#757575'},
        ':pressed': {'background': Dark.Pressed, 'border-color': '#6b6b6b'},
        ':disabled': {'color': Dark.TextDisabled, 'background': '#141414', 'border-color': '#424242'},
    }

    SubtleButton = Button | {
        'background': Light.Transparent,
        'border-color': Light.Transparent,
        ':hover': {'background': Dark.Hover},
        ':pressed': {'background': Dark.Pressed},
    }

    PrimaryButton = Button | {
        'color': Dark.Text,
        'background': Dark.Primary,
        'border-color': Dark.Transparent,
        ':hover': {'background': '#0f6cbd'},
        ':pressed': {'background': '#0c3b5e'},
    }

class Light:
    Primary = '#0f6cbd'  # 主要颜色
    PrimaryHover = '#115ea3'  # 滑过、链接
    PrimaryPressed = '#0c3b5e'

    Background = '#fff'  # 背景
    Hover = '#f5f5f5'  # 滑过
    Pressed = '#e0e0e0'  # 按下
    Danger = '#c50f1f'
    DangerHover = '#b10e1c'
    DangerPressed = '#960b18'

    Stroke = "#d1d1d1"  # 描边
    StrokeAccessible = '#616161'
    Rounded = 4  # 边框圆角
    Transparent = 'transparent'  # 透明

    Text = "#242424"  # 文本
    TextDisabled = '#bdbdbd'  # 禁用文本
    TextPlaceholder = '#707070'  # 占位文本


class Dark(Light):
    Primary = '#115ea3'
    Background = '#292929'
    Hover = '#3d3d3d'
    Pressed = '#1f1f1f'  # 按下
    Stroke = "#666666"

    Text = "#fff"
    TextDisabled = '#5c5c5c'  # 禁用文本

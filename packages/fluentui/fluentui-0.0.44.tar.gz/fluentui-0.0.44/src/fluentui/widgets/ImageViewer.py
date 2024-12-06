from PySide6.QtCore import Qt, QPoint, QVariantAnimation, QEvent
from PySide6.QtGui import QPixmap, QWheelEvent, QPainter, QResizeEvent, QColor
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem

from .container import WidgetMix


class ImageViewer(WidgetMix, QGraphicsView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.zoom_total = 1.0  # 图片总缩放倍率
        self.zoom_origin = QPoint()  # 滚动开始时的视图锚点
        self.zoom_scene_origin = QPoint()  # 滚动开始时的场景锚点
        self.pixmap: QGraphicsPixmapItem = None  # 当前图片项目

        self.zoom_anim = QVariantAnimation()  # 缩放动画
        self.zoom_anim.valueChanged.connect(self.__on_zoom)  # 动画值改变信号

        self.setScene(QGraphicsScene())  # 设置场景
        self.setViewportMargins(-2, -2, -2, -2)  # 消除边缘间距
        self.setBackgroundBrush(QColor('#242424'))  # 设置背景
        self.setFrameShape(self.Shape.NoFrame)  # 移除边框
        self.setDragMode(self.DragMode.ScrollHandDrag)  # 启用拖拽模式
        self.setResizeAnchor(self.ViewportAnchor.NoAnchor)  # 清除视图锚点
        self.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)  # 平滑渲染
        self.setCacheMode(self.CacheModeFlag.CacheBackground)  # 缓存背景
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # 隐藏垂直滚动条
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # 隐藏水平滚动条
        self.setOptimizationFlags(self.OptimizationFlag.DontSavePainterState)  # 不保存绘制状态
        self.setViewportUpdateMode(self.ViewportUpdateMode.SmartViewportUpdate)  # 智能渲染视口内容

    def load(self, item: str | QGraphicsPixmapItem):
        """ load filename or QGraphicsPixmapItem  """
        if isinstance(item, str):
            item = QGraphicsPixmapItem(QPixmap(item))
        if item.pixmap().isNull():
            return

        self.zoom_total = 1.0  # 重置缩放倍率
        self.resetTransform()  # 重置变换
        self.scene().clear()  # 清除场景内容

        self.pixmap = item
        item.setTransformationMode(Qt.TransformationMode.SmoothTransformation)  # 平滑变换
        item.setShapeMode(QGraphicsPixmapItem.ShapeMode.BoundingRectShape)  # 边界矩形形状

        self.scene().addItem(self.pixmap)  # 添加场景内容
        if self.ratio() < 1:  # 原图的宽或高 > 当前窗口
            self.fitInView(self.pixmap, Qt.AspectRatioMode.KeepAspectRatio)

    def __on_zoom(self, value: float):
        if value == self.zoom_total:
            print('比例相等，无需缩放。')
            return

        factor = value / self.zoom_total
        self.zoom_total = value
        self.scale(factor, factor)

        delta = self.mapToScene(self.zoom_origin) - self.zoom_scene_origin
        self.translate(delta.x(), delta.y())

    def zoom(self, factor: float):
        running = self.zoom_anim.state() == QVariantAnimation.State.Running
        if not self.zoom_anim.stop() and running:
            factor *= factor  # 加速缩放
        self.zoom_anim.setStartValue(self.zoom_total)
        self.zoom_anim.setEndValue(max(1.0, self.zoom_total * factor))
        self.zoom_anim.start()

    def wheelEvent(self, e: QWheelEvent):
        angle = e.angleDelta().y()  # 正值表示向前滚动 (放大)
        if angle < 0 and self.zoom_total == 1:  # 限制缩小尺寸
            print('无法缩小')
            return

        self.zoom_origin = e.position().toPoint()
        self.zoom_scene_origin = self.mapToScene(self.zoom_origin)
        self.zoom(1.1 if angle > 0 else 0.9)

    def resizeEvent(self, e: QResizeEvent):
        super().resizeEvent(e)
        if not self.pixmap: return
        factor = self.ratio() * self.zoom_total / self.m11()
        self.scale(factor, factor)

    def enterEvent(self, e: QEvent):
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.NoAnchor)
        super().enterEvent(e)

    def leaveEvent(self, e: QEvent):
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        super().leaveEvent(e)

    def m11(self) -> float:
        """
        图片自己的水平缩放系数，该值为 1 时表示图片未缩放，为原图大小。\n
        注意，是原图的大小，与当前窗口大小无关。
        """
        return self.transform().m11()

    def ratio(self) -> float:
        """
        图片与当前窗口大小宽高比。\n
        缩放图片不影响该值，只有调整大小时才会影响。\n
        pw, ph 使用 self 而不用 viewport，是因为 viewport 已经调整过 margins，
        其大小会比 self 大 4，而 self 才是整个可视区域。
        """
        scene = self.sceneRect()
        pw = self.width() / scene.width()
        ph = self.height() / scene.height()
        return min(pw, ph)

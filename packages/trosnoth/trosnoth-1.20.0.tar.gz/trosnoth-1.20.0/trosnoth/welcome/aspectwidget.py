from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtWidgets import QWidget, QSizePolicy, QPushButton


class AspectWidget(QWidget):
    '''
    A widget that maintains its aspect ratio.
    '''
    def __init__(self, *args, ratio=4/3, **kwargs):
        super().__init__(*args, **kwargs)
        self.ratio = ratio
        self.adjusted_to_size = (-1, -1)
        self.adjusted_width = self.width()
        self.adjusted_height = self.height()
        self.h_margin = 0
        self.v_margin = 0
        self.initial_width = None
        self.setSizePolicy(QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored))
        self.bg_pixmap = None

    def set_background(self, filename):
        if filename is None:
            self.bg_pixmap = None
        else:
            self.bg_pixmap = QPixmap(str(filename))

    def resizeEvent(self, event):
        size = event.size()
        if size == self.adjusted_to_size:
            # Avoid infinite recursion. I suspect Qt does this for you,
            # but it's best to be safe.
            return
        self.adjusted_to_size = size

        full_width = size.width()
        full_height = size.height()
        width = min(full_width, full_height * self.ratio)
        height = min(full_height, full_width / self.ratio)
        self.adjusted_width = width
        self.adjusted_height = height
        if self.initial_width is None:
            self.initial_width = self.adjusted_width
        new_scale = width / self.initial_width

        self.h_margin = h_margin = round((full_width - width) / 2)
        self.v_margin = v_margin = round((full_height - height) / 2)

        self.setContentsMargins(h_margin, v_margin, h_margin, v_margin)

        for child in self.findChildren(ScalingPushButton):
            child.set_scale(new_scale)

    def paintEvent(self, evt):
        super().paintEvent(evt)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        painter.drawPixmap(
            self.h_margin, self.v_margin, self.adjusted_width,
            self.adjusted_height, self.bg_pixmap)


class ScalingPushButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_font_size = None

    def paintEvent(self, evt):
        super().paintEvent(evt)
        if self.init_font_size is None:
            self.init_font_size = self.font().pointSize()

    def set_scale(self, new_scale):
        if self.init_font_size is None:
            return
        self.setStyleSheet(f'font-size: {round(self.init_font_size * new_scale)}pt;')

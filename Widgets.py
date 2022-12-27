from PyQt6.QtWidgets import QGroupBox, QGridLayout, QFrame
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtCore import pyqtSignal
from numpy import lcm
from pyqtgraph import ImageView
import numpy as np


class ImageViewFrame(QFrame):
    signal_mouse_pressed = pyqtSignal(int, int)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._imv = ImageView(self)
        self._imv.ui.histogram.hide()
        self._imv.ui.roiBtn.hide()
        self._imv.ui.menuBtn.hide()
        self._x = [25, 0]
        self._y = [25, 0]

    def get_border(self):
        return self._x[0]

    def setImage(self, img: np.array):
        self._imv.setImage(img)

    def connect_mouse_pressed_to(self, slot):
        self.signal_mouse_pressed.connect(slot)
        
    

    def mousePressEvent(self, event: QMouseEvent) -> None:
        pos = event.pos()
        x, y = pos.x(), pos.y()
        if self._x[0] < x < self._x[1] and self._y[0] < y < self._y[1]:
            self.signal_mouse_pressed.emit(x - self._x[0], y - self._y[0])
        # # print(pos.x(), pos.y())
        # return super().mousePressEvent(event)

    def setGeometry(self, x, y, w, h):
        super().setGeometry(x, y, w, h)
        self._imv.setGeometry(x, y, w, h)
        self._x[1] = w - self._x[0]
        self._y[1] = h - self._y[0]


class GroupBoxLayout(QGroupBox):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._grid = QGridLayout(self)
        self._cur_row, self._cur_col = 0, 0
        self._widgets = []
        self._unique_cols = set()

    def addWidget(self, widget, colSpan=1, rowSpan=1, nextRow=False):
        self._grid.addWidget(widget, self._cur_row, self._cur_col, rowSpan, colSpan)
        self._cur_col += colSpan
        if nextRow:
            self._cur_row += rowSpan
            self._cur_col = 0

    def addRow(self, widgets: tuple, colSpans: tuple = None, rowSpans: tuple = None):
        if colSpans is None:
            colSpans = (1, ) * len(widgets)
        if rowSpans is None:
            rowSpans = (1, ) * len(widgets)
        self._unique_cols.add(sum(colSpans))
        self._widgets.append((widgets, colSpans, rowSpans))

    def apply_layout(self):
        col_total = lcm.reduce(tuple(self._unique_cols))
        self._cur_row, self._cur_col = 0, 0
        for widgets, colSpans, rowSpans in self._widgets:
            col_num = sum(colSpans)
            for i, widget in enumerate(widgets):
                real_colSpan = col_total // col_num * colSpans[i]
                self._grid.addWidget(widget, self._cur_row, self._cur_col, rowSpans[i], real_colSpan)
                self._cur_col += real_colSpan
            self._cur_row += max(rowSpans)
            self._cur_col = 0

    def nextRow(self, num=1):
        self._cur_row += num
        self._cur_col = 0

    def nextCol(self, num=1):
        self._cur_col += num

    def setSpacing(self, spacing=0, orientation=0) -> None:
        if orientation == 0:
            self._grid.setHorizontalSpacing(spacing)
        else:
            self._grid.setVerticalSpacing(spacing)
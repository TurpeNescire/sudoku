from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import Qt

from sudoku_settings import *


class CellFocusOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._visible = False

        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)


    def setFocused(self, focused: bool):
        self._visible = focused
        self.update()


# TODO: add hover events that don't take focus
    def paintEvent(self, event):
        if not self._visible:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        color = QColor(CELL_FOCUS_RECT_COLOR)
        color.setAlpha(CELL_FOCUS_RECT_ALPHA)
        pen = QPen(color)
        pen.setWidth(CELL_FOCUS_RECT_WIDTH)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        #rect = self.rect().adjusted(4, 4, -4, -4)
        rect = self.rect().adjusted(
                CELL_FOCUS_RECT_INSET,
                CELL_FOCUS_RECT_INSET,
                -CELL_FOCUS_RECT_INSET,
                -CELL_FOCUS_RECT_INSET
        )
        #painter.drawRoundedRect(rect, 4, 4)
        painter.drawRoundedRect(rect, CELL_FOCUS_RECT_RADIUS, CELL_FOCUS_RECT_RADIUS)


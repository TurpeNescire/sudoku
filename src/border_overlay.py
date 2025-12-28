from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import Qt, QTimer

from sudoku_settings import *


class BorderOverlay(QWidget):
    def __init__(self, gridSize=9, parent=None):
        super().__init__(parent)

        self._gridSize = gridSize
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        overlaySize = min(self.width(), self.height())
        cellSize = overlaySize / self._gridSize
        x_offset = (self.width() - overlaySize) / 2
        y_offset = (self.height() - overlaySize) / 2

        # Pens
        thinPen = QPen(QColor(BORDER_THIN_COLOR), 1)
        thinPen.setStyle(BORDER_THIN_STYLE)
        thickPen = QPen(QColor(BORDER_THICK_COLOR), 3)
        thickPen.setStyle(BORDER_THICK_STYLE)



        # Draw thin and thick boundary lines
        for rowOrColIndex in range(1, self._gridSize + 1):
            if rowOrColIndex % 3 == 0:          # thick boundary
                painter.setPen(thickPen)
            else:                               # thin boundary
                painter.setPen(thinPen)

            # vertical and horizontal pixel position
            pos = rowOrColIndex * cellSize

            # vertical
            painter.drawLine(
                x_offset + pos,
                y_offset,
                x_offset + pos,
                y_offset + overlaySize
            )

            # horizontal
            painter.drawLine(
                x_offset,
                y_offset + pos,
                x_offset + overlaySize,
                y_offset + pos
            )


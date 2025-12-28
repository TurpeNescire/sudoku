from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import Qt

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

        for row in range(self._gridSize + 1):
            for col in range(self._gridSize + 1):
                x = x_offset + col * cellSize
                y = y_offset + row * cellSize

                # Vertical lines
                if col < self._gridSize:
                    pen = QPen(QColor(BORDER_THICK_COLOR) if col % 3 == 0 else QColor(BORDER_THIN_COLOR),
                               3 if col % 3 == 0 else 1)
                    pen.setStyle(BORDER_THICK_STYLE if col % 3 == 0 else BORDER_THIN_STYLE)
                    painter.setPen(pen)
                    painter.drawLine(x, y_offset, x, y_offset + overlaySize)    # type: ignore

                # Horizontal lines
                if row < self._gridSize:
                    pen = QPen(QColor(BORDER_THICK_COLOR) if row % 3 == 0 else QColor(BORDER_THIN_COLOR),
                               3 if row % 3 == 0 else 1)
                    pen.setStyle(BORDER_THICK_STYLE if row % 3 == 0 else BORDER_THIN_STYLE)
                    painter.setPen(pen)
                    painter.drawLine(x_offset, y, x_offset + overlaySize, y)    # type: ignore


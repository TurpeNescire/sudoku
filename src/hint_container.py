from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QRectF, QRect
from PySide6.QtGui import QPainter, QColor, QFont 

from sudoku_settings import *


class HintContainer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Example hint values, you can replace with dynamic data
        #self._hints = [[str(r * 3 + c + 1) for c in range(3)] for r in range(3)]
        self._hints: list[int] = []
        for row in range(3):
            for col in range(3):
                hint = row * 3 + col + 1
                self._hints.append(hint)

        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, True)
        self.setAutoFillBackground(False)


    def setHints(self, hints):
        self._hints = hints
        self.update()


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Optional: fill background (transparent or white)
        #painter.fillRect(self.rect(), Qt.transparent)
        painter.fillRect(self.rect(), HINT_BACKGROUND_COLOR)

        availableWidth = self.width()
        availableHeight = self.height()
        cellSize = min(availableWidth, availableHeight)
        inset = cellSize * HINT_INSET_RATIO
        # sanity check inset amount, it should be in pixels now
        inset = max(HINT_INSET_MIN, inset)
        inset = min(HINT_INSET_MAX, inset)

        newCellSize = cellSize - inset * 2
        left = (self.width() - newCellSize) / 2
        top = (self.height() - newCellSize) / 2
        left = int(round(left))
        top = int(round(top))
        size = int(round(newCellSize))
        drawRect = QRect(left, top, size, size)
        hintSize = newCellSize / 3

        font = QFont("Arial", int(round(min(hintSize, hintSize) / HINT_FONT_SIZE_SCALE)))
        painter.setFont(font)
        painter.setPen(QColor(HINT_FONT_COLOR))

        for row in range(3):
            for col in range(3):
                index = row * 3 + col
                hint_text = str(self._hints[index])

                hintRect = QRectF(
                        drawRect.left() + col * hintSize,
                        drawRect.top() + row * hintSize,
                        hintSize,
                        hintSize
                )
                
                painter.drawText(
                    hintRect,
                    Qt.AlignmentFlag.AlignCenter,
                    hint_text
                )



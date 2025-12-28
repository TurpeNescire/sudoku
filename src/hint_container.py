from PySide6.QtWidgets import QWidget, QLabel, QFrame
from PySide6.QtCore import Qt, QRectF
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

        self.setAttribute(Qt.WA_OpaquePaintEvent, True)
        self.setAutoFillBackground(False)


    def setHints(self, hints):
        self._hints = hints
        self.update()


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Optional: fill background (transparent or white)
        #painter.fillRect(self.rect(), Qt.transparent)
        painter.fillRect(self.rect(), HINT_CONTAINER_BACKGROUND_COLOR)

        w = self.width()
        h = self.height()
        cell_width = w / 3
        cell_height = h / 3

        font = QFont("Arial", int(round(min(cell_width, cell_height) / HINT_CONTAINER_FONT_SIZE_SCALE)))
        painter.setFont(font)
        painter.setPen(QColor(HINT_CONTAINER_FONT_COLOR))

        for row in range(3):
            for col in range(3):
                index = row * 3 + col
                hint_text = str(self._hints[index])

                x = col * cell_width
                y = row * cell_height
                rect = QRectF(x, y, cell_width, cell_height)
                painter.drawText(
                    rect,
                    Qt.AlignmentFlag.AlignCenter,
                    hint_text
                )


#class Hint(QLabel):
#    def __init__(self, row, col, text="", parent=None):
#        super().__init__(text, parent)
#
#        self._row = row
#        self._col = col
#
#        #self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
#
#        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
#        self.setStyleSheet(f"""
#            Hint {{
#                background: yellow;
#                border: none;
#                outline: none;
#                color: black;
#            }}
#        """)
#
#
#class HintContainer(QWidget):
#    def __init__(self, parent=None):
#        super().__init__(parent)
#        
#        self._hints: list[Hint] = []
#
#        for row in range(3):
#            for col in range(3):
#                self._hints.append(Hint(row, col, f"{row * 3 + col + 1}", self))
#
#
#    def resizeEvent(self, event):
#        cellWidth = self.width() // 3
#        cellHeight = self.height() // 3
#
#        for row in range(3):
#            for col in range(3):
#                index = row * 3 + col
#                self._hints[index].setGeometry(
#                        col * cellWidth,
#                        row * cellHeight,
#                        cellWidth,
#                        cellHeight
#                )
#
#
#        super().resizeEvent(event)
#

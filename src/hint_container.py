from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCore import Qt


class Hint(QLabel):
    def __init__(self, row, col, text="", parent=None):
        super().__init__(text, parent)

        self._row = row
        self._col = col

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("background-color: lightgray; border: 1px solid gray;")


class HintContainer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self._hints: list[Hint] = []

        for row in range(3):
            for col in range(3):
                self._hints.append(Hint(row, col, f"{row * 3 + col + 1}", self))


    def resizeEvent(self, event):
        cellWidth = self.width() // 3
        cellHeight = self.height() // 3

        for row in range(3):
            for col in range(3):
                index = row * 3 + col
                self._hints[index].setGeometry(
                        col * cellWidth,
                        row * cellHeight,
                        cellWidth,
                        cellHeight
                )

        super().resizeEvent(event)


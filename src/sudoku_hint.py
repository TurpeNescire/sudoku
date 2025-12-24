from PySide6.QtWidgets import QWidget, QLineEdit, QGridLayout, QSizePolicy, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QSize, QEvent

from sudoku_settings import *

class Hint(QLabel):
    row: int
    col: int

    def __init__(self, parent, text: str, row: int, col: int):
        super().__init__(parent)

        self.row = row
        self.col = col
        self.setText(text)




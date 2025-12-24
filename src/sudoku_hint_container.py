from __future__ import annotations
from typing import TYPE_CHECKING

from PySide6.QtWidgets import QWidget, QLineEdit, QGridLayout, QSizePolicy, QVBoxLayout, QStackedWidget

if TYPE_CHECKING:
    from sudoku_cell import Cell
from sudoku_hint import Hint


class HintContainer(QWidget):
    def __init__(self, parent: Cell, row: int, col: int):
        super().__init__(parent)

        self.row = row
        self.col = col

        self.installEventFilter(parent)
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        for row_idx in range (3):
            for col_idx in range(3):
                digit = (row_idx + 1) * (col_idx + 1)
                hint = Hint(self, str(digit), row_idx, col_idx)
                #hint.setReadOnly(True)
                layout.addWidget(hint, row_idx, col_idx)

        self.setLayout(layout)


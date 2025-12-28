from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Qt

from sudoku_settings import *


class CellEdit(QLineEdit):
    def __init__(self, row: int, col: int, parent=None):
        super().__init__(parent)

        self._row = row
        self._col = col
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setFrame(False)
        self.setText(f"{self._row},{self._col}")
        self.setStyleSheet(f"""
            QLineEdit {{
                background-color: {CELL_EDIT_BACKGROUND_COLOR};   /* temporary visible color */
                color: {CELL_EDIT_FONT_COLOR};
                border: {CELL_EDIT_BORDER_SIZE};
                padding: {CELL_EDIT_PADDING_SIZE}px;
            }}
        """)


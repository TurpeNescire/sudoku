import random

from PySide6.QtWidgets import QLineEdit
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtCore import Qt, QRegularExpression

from sudoku_settings import *


class CellEdit(QLineEdit):
    def __init__(self, row: int, col: int, parent):
        super().__init__(parent)

        self.row = row
        self.col = col
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        # QIntValidator still allows stuff like 0, 001, 000004
        validator = QRegularExpressionValidator(QRegularExpression("^[1-9]$"))
        self.setValidator(validator)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        #self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        self.setFrame(True)
        #self.setText(f"{self.row},{self.col}")
        self.setText(f"{random.choice('          123456789')}")
        if self.text() == " ":
            self.setText("")
        self.setStyleSheet(f"""
            QLineEdit {{
                background-color: {CELL_EDIT_BACKGROUND_COLOR};
                font-family: {CELL_EDIT_FONT_FAMILY};
                color: {CELL_EDIT_FONT_COLOR};
                border: {CELL_EDIT_BORDER_SIZE};
                padding: {CELL_EDIT_PADDING_SIZE}px;
            }}
        """)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        font = self.font()
        newSize = int(max(10, self.width() * CELL_EDIT_FONT_SCALE))
        font.setPixelSize(newSize)
        self.setFont(font)


from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Qt

from sudoku_settings import *


class CellEdit(QLineEdit):
    def __init__(self, row: int, col: int, parent):
        super().__init__(parent)

        self.row = row
        self.col = col
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        #self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setFrame(False)
        self.setText(f"{self.row},{self.col}")
        self.setStyleSheet(f"""
            QLineEdit {{
                background-color: {CELL_EDIT_BACKGROUND_COLOR};
                color: {CELL_EDIT_FONT_COLOR};
                border: {CELL_EDIT_BORDER_SIZE};
                padding: {CELL_EDIT_PADDING_SIZE}px;
            }}
        """)

#    def setFocus(self, reason=Qt.FocusReason.OtherFocusReason):
#        print(f"{self}.setFocus called with reason {reason}")
#        super().setFocus(reason)
#
#    def focusInEvent(self, event):
#        self.parent().setFocused(True)
#        print(f"{self}.focusInEvent called with event {event}")
#        super().focusInEvent(event)
#
#
#    def focusOutEvent(self, event):
#        self.parent().setFocused(False)
#        print(f"{self}.focusOutEvent called with event {event}")
#        super().focusOutEvent(event)
#
#

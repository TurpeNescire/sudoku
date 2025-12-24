from PySide6.QtWidgets import QWidget, QLineEdit, QGridLayout, QSizePolicy, QVBoxLayout 
from PySide6.QtCore import Qt, QSize, QEvent

from sudoku_settings import *


class CellEdit(QLineEdit):
    row: int
    col: int
    myLayout: QVBoxLayout

    def __init__(self, parent, row: int, col: int):
        super().__init__(parent)

        self.row = row
        self.col = col

        self.setReadOnly(True)
        #self.setAttribute(Qt.WA_MacShowFocusRect, False)    # trying to get rid of focus rect
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setMaxLength(1)         # only one digit
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.myLayout = QVBoxLayout()
        self.setLayout(self.myLayout)


        self.resetStyleSheet()
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        font = self.font()
        new_size = max(10, int(event.size().height() * 0.7))
        font.setPointSize(new_size)
        self.setFont(font)

    # for some reason on mac, the focus rectangle for qlineedit's with active
    # edit mode have a blue highlight rectangle that can't be gotten rid of
    # except by resetting the style sheet, so this is the best place to do it without
    # resetting the stylesheet too often?  hacky but they need to fix
    # self.setAttribute(Qt.WA_MacShowFocusRect, False) which is supposed to do this
    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.style().unpolish(self)
        self.resetStyleSheet()
        self.style().polish(self)

    def resetStyleSheet(self):
        side_border_width = ""
        if self.row == 2 or self.row == 5:
            side_border_width += f"border-bottom-width: {CELL_BORDER_SIDE_WIDTH}px;\n"
        elif self.row == 3 or self.row == 6:
            side_border_width += f"border-top-width: {CELL_BORDER_SIDE_WIDTH}px;\n"
        
        if self.col == 2 or self.col == 5:
            side_border_width += f"\t\tborder-right-width: {CELL_BORDER_SIDE_WIDTH}px;\n"
        elif self.col == 3 or self.col == 6:
            side_border_width += f"\t\tborder-left-width: {CELL_BORDER_SIDE_WIDTH}px;\n"

        side_border_width = side_border_width[:-1]

        self.setStyleSheet(f"""
            QLineEdit {{
                background-color: {CELL_BACKGROUND_COLOR};
                border: {CELL_BORDER_WIDTH}px {CELL_BORDER_STYLE} {CELL_BORDER_COLOR};
                {side_border_width}
                border-radius: {CELL_BORDER_RADIUS};
                padding: {CELL_PADDING}px;
                margin: {CELL_MARGIN}px;
                outline: none;
                outline-color: {CELL_OUTLINE_COLOR};
                color: red
            }}
            QLineEdit:focus {{
                background-color: {CELL_FOCUS_BACKGROUND_COLOR};
                border: {CELL_BORDER_WIDTH}px {CELL_BORDER_STYLE} {CELL_FOCUS_BORDER_COLOR};
                {side_border_width}
                border-radius: {CELL_BORDER_RADIUS};
                padding: {CELL_FOCUS_PADDING}px;
                margin: {CELL_FOCUS_MARGIN}px;
                outline: 0;
                outline-color: {CELL_FOCUS_OUTLINE_COLOR};
                outline-color: orange;
                color: blue
            }}
        """)

        #if self.row == 2 and self.col == 2:
        #    print(self.property("styleSheet"))


from PySide6.QtWidgets import QWidget, QLineEdit, QGridLayout, QSizePolicy, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QSize, QEvent

from sudoku_settings import *

class Hint(QLabel):
    row: int
    col: int
    pRow: int
    pCol: int

    def __init__(self, parent, text: str, row: int, col: int):
        super().__init__(parent)

        self.row = row
        self.col = col
        self.pRow = parent.row
        self.pCol = parent.col
        self.setText(text)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.resetStyleSheet()

       
    def resetStyleSheet(self):
        fontSize = max(9, int(self.height() * 0.6))
        side_border_width = []
        
        if self.row == 2:
            if self.pRow == 2 or self.pRow == 5:
                #side_border_width.append(f"border-bottom-width: 2px;")
                side_border_width.append(f"border-bottom: {HINT_BORDER_SIDE_WIDTH}px {HINT_BORDER_SIDE_STYLE} {HINT_BORDER_SIDE_COLOR};")
            else:
                #side_border_width.append(f"border-bottom-width: 1px;")
                side_border_width.append(f"border-bottom: {CELL_BORDER_WIDTH}px {CELL_BORDER_STYLE} {CELL_BORDER_COLOR};")

            if self.col == 2:
                side_border_width.append(f"\t\tborder-bottom-right-radius: 4px;")
        elif self.row == 0:
            if self.pRow == 3 or self.pRow == 6:
                #side_border_width.append(f"border-top-width: 2px;")
                side_border_width.append(f"border-top: {HINT_BORDER_SIDE_WIDTH}px {HINT_BORDER_SIDE_STYLE} {HINT_BORDER_SIDE_COLOR};")
            else:
                #side_border_width.append(f"border-top-width: 1px;")
                side_border_width.append(f"border-top: {CELL_BORDER_WIDTH}px {CELL_BORDER_STYLE} {CELL_BORDER_COLOR};")

            if self.col == 0:
                side_border_width.append(f"\t\tborder-top-left-radius: 4px;")

        if self.col == 2:
            if self.pCol == 2 or self.pCol == 5:
                #side_border_width.append(f"\t\tborder-right-width: 2px;")
                side_border_width.append(f"border-right: {HINT_BORDER_SIDE_WIDTH}px {HINT_BORDER_SIDE_STYLE} {HINT_BORDER_SIDE_COLOR};")
            else:
                #side_border_width.append(f"\t\tborder-right-width: 1px;")
                side_border_width.append(f"border-right: {CELL_BORDER_WIDTH}px {CELL_BORDER_STYLE} {CELL_BORDER_COLOR};")

            if self.row == 0:
                side_border_width.append(f"\t\tborder-top-right-radius: 4px;")
        elif self.col == 0:
            if self.pCol == 3 or self.pCol == 6:
                #side_border_width.append(f"\t\tborder-left-width: 2px;")
                side_border_width.append(f"border-left: {HINT_BORDER_SIDE_WIDTH}px {HINT_BORDER_SIDE_STYLE} {HINT_BORDER_SIDE_COLOR};")
            else:
                #side_border_width.append(f"\t\tborder-left-width: 1px;")
                side_border_width.append(f"border-left: {CELL_BORDER_WIDTH}px {CELL_BORDER_STYLE} {CELL_BORDER_COLOR};")

            if self.row == 2:
                side_border_width.append(f"\t\tborder-bottom-left-radius: 4px;")

        # clean up tabs and newlines for style sheet
        if len(side_border_width) > 0 and side_border_width[0][0] == "\t":
            side_border_width[0] = side_border_width[0][2:]
        if side_border_width != "":
            side_border_width = "\n".join(side_border_width)

        self.setStyleSheet(f"""
            QLabel:focus {{
                border: 0px solid black;
                {side_border_width}
                background-color: #dcdcdc;
                color: red;
                font-size: {fontSize}px;
            }}
            QLabel {{
                border: 0px solid black;
                {side_border_width}
                background-color: white;
                color: blue;
                font-size: {fontSize}px;
            }}
        """)


    def focusInEvent(self, event):
        super().focusInEvent(event)
        #print(self.property("styleSheet"))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resetStyleSheet()


from PySide6.QtWidgets import QWidget, QLineEdit, QGridLayout, QSizePolicy, QVBoxLayout, QStackedWidget


from sudoku_cell import Cell


class HintContainer(QWidget):
    def __init__(self, parent: Cell, row: int, col: int):
        super().__init__(parent)

        self.row = row
        self.col = col

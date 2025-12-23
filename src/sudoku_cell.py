from PySide6.QtWidgets import QWidget, QLineEdit, QGridLayout, QSizePolicy, QVBoxLayout, QStackedWidget
from PySide6.QtCore import Qt, QSize, QEvent

from sudoku_settings import *
from sudoku_cell_line_edit import CellLineEdit

class Cell(QWidget):
    row: int
    col: int
    myLayout: QVBoxLayout
    stacked_widget: QStackedWidget
    solution: CellLineEdit
    solution_layout: QVBoxLayout
    hint_container: QWidget
    hint_layout: QGridLayout

    def __init__(self, parent, row: int, col: int):
        super().__init__(parent)
        
        self.row = row
        self.col = col
        
        # stacked_widget allows Cell to swap between visible child widgets
        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.installEventFilter(parent)

        # solution is the line edit subclass that shows single digit answers
        self.solution = CellLineEdit(self, row, col)
        self.solution.installEventFilter(parent)

        self.stacked_widget.addWidget(self.solution)
        
        # hint container contains 3x3 QLineEdits for displaying hints 
        self.hint_container = QWidget(self)
        self.hint_container.installEventFilter(parent)
        self.hint_layout = QGridLayout()
        self.hint_container.setLayout(self.hint_layout)
        self.stacked_widget.addWidget(self.hint_container)

        # set solution as the visible widget
        self.stacked_widget.setCurrentIndex(0);
        
        self.myLayout = QVBoxLayout()
        self.myLayout.addWidget(self.stacked_widget)
        self.myLayout.setContentsMargins(0, 0, 0, 0)
        #self.myLayout.setSpacing(0)
        self.setLayout(self.myLayout)



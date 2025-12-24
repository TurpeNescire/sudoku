from enum import Enum

from PySide6.QtWidgets import QWidget, QLineEdit, QGridLayout, QSizePolicy, QVBoxLayout, QStackedWidget
from PySide6.QtCore import Qt, QSize, QEvent, QEnum, QObject

from sudoku_settings import *
from sudoku_cell_line_edit import CellLineEdit


class CellViewMode(Enum):
    SOLUTION = 0
    HINT_GRID = 1
    HINT_COMPACT = 2


class CellViewObject(QObject):
    CellViewMode = QEnum(CellViewMode)

    def __init__(self):
        super().__init__()


class Cell(QWidget):
    row: int
    col: int
    display_as_hint: int
    myLayout: QVBoxLayout
    stacked_widget: QStackedWidget
    solution: CellLineEdit
    solution_layout: QVBoxLayout
    hint_container: QWidget
    hint_layout: QGridLayout
    mode: CellViewMode

    def __init__(self, parent, row: int, col: int):
        super().__init__(parent)
        
        self.row = row
        self.col = col
        self.display_as_hint = False
        
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
        self.hint_layout.setContentsMargins(0, 0, 0, 0)
        for row_idx in range (3):
            for col_idx in range(3):
                digit = (row_idx + 1) * (col_idx + 1)
                hint_edit = QLineEdit(str(digit))
                hint_edit.setReadOnly(True)
                self.hint_layout.addWidget(hint_edit, row_idx, col_idx)

        self.hint_container.setLayout(self.hint_layout)
        self.stacked_widget.addWidget(self.hint_container)

        # set solution as the visible widget
        self.show_solution()
        
        self.myLayout = QVBoxLayout()
        self.myLayout.addWidget(self.stacked_widget)
        self.myLayout.setContentsMargins(0, 0, 0, 0)
        #self.myLayout.setSpacing(0)
        self.setLayout(self.myLayout)

    def show_solution(self):
        self.mode = CellViewMode.SOLUTION
        self.stacked_widget.setCurrentIndex(CellViewMode.SOLUTION.value)

    def show_hint_grid(self):
        self.mode = CellViewMode.HINT_GRID
        self.stacked_widget.setCurrentIndex(CellViewMode.HINT_GRID.value)

    def show_compact_hints(self):
        self.mode = CellViewMode.HINT_COMPACT
        self.stacked_widget.setCurrentIndex(CellViewMode.HINT_COMPACT.value)

    def get_mode(self) -> CellViewMode:
        return self.mode

    def set_mode(self, mode: CellViewMode):
        if mode == CellViewMode.SOLUTION:
            self.show_solution()
        elif mode == CellViewMode.HINT_GRID:
            self.show_hint_grid()
        elif mode == CellViewMode.HINT_COMPACT:
            self.show_compact_hints()

    def cycle_mode(self):
        if self.mode == CellViewMode.SOLUTION:
            self.show_hint_grid()
        elif self.mode == CellViewMode.HINT_GRID:
            self.show_compact_hints()
        elif self.mode == CellViewMode.HINT_COMPACT:
            self.show_solution()


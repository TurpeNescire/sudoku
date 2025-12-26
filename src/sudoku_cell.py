from enum import Enum

from PySide6.QtWidgets import QWidget, QLineEdit, QGridLayout, QSizePolicy, QVBoxLayout, QStackedWidget
from PySide6.QtCore import Qt, QSize, QEvent, QEnum, QObject

from sudoku_settings import *
from sudoku_cell_edit import CellEdit
from sudoku_hint_container import HintContainer


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
    solution: CellEdit
    solution_layout: QVBoxLayout
    hint_container: QWidget
    hint_layout: QGridLayout
    mode: CellViewMode

    def __init__(self, parent, row: int, col: int):
        super().__init__(parent)
        
        self.row = row
        self.col = col
        self.display_as_hint = False

        policy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        policy.setHeightForWidth(True)
        self.setSizePolicy(policy)

        # stacked_widget allows Cell to swap between visible child widgets
        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.installEventFilter(parent)

        # solution is the line edit subclass that shows single digit answers
        self.solution = CellEdit(self, row, col)
        self.solution.installEventFilter(parent)

        self.stacked_widget.addWidget(self.solution)
        
        # hint container contains 3x3 QLineEdits for displaying hints 
        self.hint_container = HintContainer(self, self.row, self.col)
        self.stacked_widget.addWidget(self.hint_container)

        # set solution as the visible widget
        self.show_solution()
        
        self.myLayout = QVBoxLayout()
        self.myLayout.addWidget(self.stacked_widget)
        self.myLayout.setContentsMargins(0, 0, 0, 0)
        #self.myLayout.setSpacing(0)
        self.setLayout(self.myLayout)

    def get_cell_widget(self):
        return self.stacked_widget.currentWidget()

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
            self.show_solution()
            #self.show_compact_hints()
#        elif self.mode == CellViewMode.HINT_COMPACT:
#            self.show_solution()


#    def resizeEvent(self, event):
#        super().resizeEvent(event)

# does this do anything to keep square cells?
    def heightForWidth(self, width):
        return width  # Always return same as width for square

    def sizeHint(self):
        parent = self.parentWidget()
        if parent:
            side = min(parent.width(), parent.height()) // 9
            return QSize(side, side)
        return QSize(30, 30)
    


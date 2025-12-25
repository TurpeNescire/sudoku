from __future__ import annotations
from typing import TYPE_CHECKING

from PySide6.QtWidgets import QFrame, QGridLayout, QStackedWidget, QWidgetItem, QHBoxLayout, QVBoxLayout, QSizePolicy, QLayout, QWidget
from PySide6.QtCore import Qt, QEvent, QRect, QObject

if TYPE_CHECKING:
    from sudoku_main_window import SudokuMainWindow 
from sudoku_cell import Cell
from sudoku_cell_edit import CellEdit
from sudoku_settings import *
#from sudoku_hint import Hint


class SudokuGridView(QFrame):
    in_edit_mode = True
    mainWindow: SudokuMainWindow

    def __init__(self, parent: SudokuMainWindow):
        super().__init__(parent)

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus) 
        self.mainWindow = parent

        layout = QGridLayout()
        layout.setSpacing(0)
        for row in range(9):
            for col in range(9):
                cell = Cell(self, row, col)
                cell.installEventFilter(self)
                layout.addWidget(cell, row, col)

        self.setLayout(layout)

    def eventFilter(self, obj, event):
        # intercept key press events from interior cell widgets
        # after calling cell.installEventFilter(self) in the constructor
        # we need to do this becasue QLineEdit was eating arrow keys and escape, etc.
        if event.type() == QEvent.Type.KeyPress and isinstance(obj, CellEdit):
            return self.handleKeyPress(event.key()) 

        return super().eventFilter(obj, event)

    def keyPressEvent(self, event):
        if self.handleKeyPress(event.key()) is False:
            super().keyPressEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        side = min(self.width(), self.height())
        self.resize(side, side)
        parent = self.parent()
        assert isinstance(parent, QWidget) 
        self.move(parent.rect().center() - self.rect().center())

    def handleKeyPress(self, key):
        # move the current focus highlight to the next cell
        if (
            key == Qt.Key.Key_Return or key == Qt.Key.Key_Up or
            key == Qt.Key.Key_Down or key == Qt.Key.Key_Left or
            key == Qt.Key.Key_Right
        ):
            currentFocus = self.focusWidget()

            # runs at startup to set the current focus to the CellLineEdit
            # at position (0,0) in the grid layout
            if isinstance(currentFocus, SudokuGridView):
                currentFocusLayout = currentFocus.layout()
                assert isinstance(currentFocusLayout, QGridLayout)
                currentFocusItem = currentFocusLayout.itemAtPosition(0,0)
                assert isinstance(currentFocusItem, QWidgetItem)
                currentFocus = currentFocusItem.widget()
                assert isinstance(currentFocus, Cell)
                currentFocus = currentFocus.findChild(QStackedWidget)
                assert isinstance(currentFocus, QStackedWidget)
                currentFocus = currentFocus.widget(0)
                assert isinstance(currentFocus, CellEdit)
                currentFocus.setFocus()
                return True

            currentFocus = self.mainWindow.get_current_cell()
            assert isinstance(currentFocus, Cell)
            row, col = currentFocus.row, currentFocus.col

            # after getting the current row/col, handle finding the next
            # cells row/col, wrapping the row or column 
            if SCROLL_MODE == "no v wrap":    # don't wrap at the vertical limits
                index = row * 9 + col
                if key == Qt.Key.Key_Return or key == Qt.Key.Key_Down:
                    index = (index + 9) % 81
                elif key == Qt.Key.Key_Up:
                    index = (index - 9) % 81
                elif key == Qt.Key.Key_Left:
                    index = (index - 1) % 81
                elif key == Qt.Key.Key_Right:
                    index = (index + 1) % 81
                row, col = divmod(index, 9)
            elif SCROLL_MODE == "v wrap":      # wrap at the vertical limits
                if key == Qt.Key.Key_Return or key == Qt.Key.Key_Down:
                    row, col = (row + 1) % 9, col
                    if row == 0:
                        col = (col + 1) % 9
                elif key == Qt.Key.Key_Up:
                    row, col = (row - 1) % 9, col
                    if row == 8:
                        col = (col - 1) % 9
                elif key == Qt.Key.Key_Left:
                    col, row = (col - 1) % 9, row
                    if col == 8:
                        row = (row - 1) % 9
                elif key == Qt.Key.Key_Right:
                    col, row = (col + 1) % 9, row
                    if col == 0:
                        row = (row + 1) % 9

            # get the widget of the next focus item using new row/col values
            layout = self.layout()
            assert isinstance(layout, QGridLayout)
            nextFocusLayoutItem = layout.itemAtPosition(row, col)
            nextFocusCell = nextFocusLayoutItem.widget() if nextFocusLayoutItem else None
            assert isinstance(nextFocusCell, Cell)
            nextFocusWidget = nextFocusCell.get_cell_widget()
            nextFocusWidget.setFocus()

            return True
        elif key == Qt.Key.Key_Tab:         # either Qt or MacOS seems to coopt Key_Tab events, this never runs
            return False
        elif key == Qt.Key.Key_Space:
            self.edit_mode()
            return True
        elif key == Qt.Key.Key_Escape: 
            self.in_edit_mode = False
            self.edit_mode()
            return True
       
        return False

    def edit_mode(self):
        # toggle read only mode on cells inside the central layout
        self.in_edit_mode = False if self.in_edit_mode else True

        layout = self.layout()
        assert isinstance(layout, QGridLayout)
        for i in range(layout.count()):
            item = layout.itemAt(i)
            assert isinstance(item, QWidgetItem)
            cell = item.widget()
            assert isinstance(cell, Cell)
            cellStackedWidget = cell.findChild(QStackedWidget)
            assert isinstance(cellStackedWidget, QStackedWidget)
            cellEdit = cellStackedWidget.widget(0)
            assert isinstance(cellEdit, CellEdit)
            cellEdit.setReadOnly(self.in_edit_mode)                       


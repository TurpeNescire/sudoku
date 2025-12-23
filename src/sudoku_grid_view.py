from PySide6.QtWidgets import QFrame, QGridLayout, QStackedWidget, QWidgetItem, QHBoxLayout, QVBoxLayout, QSizePolicy, QLayout, QWidget
from PySide6.QtCore import Qt, QEvent, QRect, QObject

from sudoku_cell import Cell
from sudoku_cell_line_edit import CellLineEdit
from sudoku_settings import *


class SudokuGridView(QFrame):
    in_edit_mode = True

    def __init__(self):
        super().__init__()

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus) 

        layout = QGridLayout()
        layout.setSpacing(0)
        for row in range(9):
            for col in range(9):
                cell = Cell(self, row, col)
                cell.installEventFilter(self)
                layout.addWidget(cell, row, col)

        self.setLayout(layout)


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
                assert isinstance(currentFocus, CellLineEdit)
                currentFocus.setFocus()
                return True

            # hierarchy is Cell->QStackedWidget->CellLineEdit, need to get the
            # current focus CellLineEdit's parent Cell so we can find the next
            # Cell in the 9x9 grid
            assert isinstance(currentFocus, CellLineEdit)
            currentFocus = currentFocus.parent().parent()
            assert isinstance(currentFocus, Cell)

            # TODO: fix after installing QGridLayout in containing layout
            layout = self.layout()
            assert isinstance(layout, QGridLayout)
            index = layout.indexOf(currentFocus)
            assert index != -1

            pos = layout.getItemPosition(index)
            assert pos is not None
            row, col, _rowSpan, _colSpan = pos # type: ignore
                    # known limitation in PySide6 type stubs
                    # getItemPosition() always returns a 4-tuple at runtime
            
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
            nextFocusLayoutItem = layout.itemAtPosition(row, col)
            nextFocusCell = nextFocusLayoutItem.widget() if nextFocusLayoutItem else None
            assert isinstance(nextFocusCell, Cell)
            nextFocusStackedWidget = nextFocusCell.findChild(QStackedWidget)
            assert isinstance(nextFocusStackedWidget, QStackedWidget)
            nextFocusWidget = nextFocusStackedWidget.widget(0)
            assert isinstance(nextFocusWidget, CellLineEdit)

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
            if item is not None:
                widget = item.widget()
                if isinstance(widget, CellLineEdit):
                    widget.setReadOnly(self.in_edit_mode)

    def eventFilter(self, obj, event):
        # intercept key presses from interior cell widgets
        if event.type() == QEvent.Type.KeyPress and isinstance(obj, CellLineEdit):
            return self.handleKeyPress(event.key()) 

        return super().eventFilter(obj, event)
                        


'''
    def setCellStyleSheet(self):
        for i in range(self.gridLayout.count()):
            item = self.gridLayout.itemAt(i)
            if item is not None:
                widget = item.widget()
                if isinstance(widget, CellLineEdit):
                    widget.setStyleSheet(f"""
                        QLineEdit {{
                            border: {CELL_BORDER_WIDTH}px {CELL_BORDER_STYLE} {CELL_BORDER_COLOR};
                            border-radius: {CELL_BORDER_RADIUS}px;
                            background-color: {CELL_BACKGROUND_COLOR};
                            selection-background-color: {CELL_SELECTION_BACKGROUND_COLOR};
                            color: {CELL_FONT_COLOR};
                            font-size: {CELL_FONT_SIZE}px;
                            outline-color: {CELL_OUTLINE_COLOR};
                            outline-radius: {CELL_OUTLINE_RADIUS};
                            outline-style: {CELL_OUTLINE_STYLE};
                            padding: {CELL_PADDING}px;
                            margin: {CELL_MARGIN}px;

                        }}
                        QLineEdit:focus {{
                            border: {CELL_FOCUS_BORDER_WIDTH}px {CELL_FOCUS_BORDER_STYLE} {CELL_FOCUS_BORDER_COLOR};
                            border-radius: {CELL_FOCUS_BORDER_RADIUS}px;
                            background-color: {CELL_FOCUS_BACKGROUND_COLOR};
                            selection-background-color: {CELL_FOCUS_SELECTION_BACKGROUND_COLOR};
                            color: {CELL_FOCUS_FONT_COLOR};
                            font-size: {CELL_FOCUS_FONT_SIZE}px;
                            outline-color: {CELL_OUTLINE_COLOR};
                            outline-radius: {CELL_FOCUS_OUTLINE_RADIUS};
                            outline-style: {CELL_FOCUS_OUTLINE_STYLE};
                            padding: {CELL_FOCUS_PADDING}px;
                            margin: {CELL_FOCUS_MARGIN}px;
                        }}
                    """)
        self.updateGeometry()
'''

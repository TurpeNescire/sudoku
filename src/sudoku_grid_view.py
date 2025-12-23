from PySide6.QtWidgets import QFrame, QGridLayout, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Qt, QEvent

from sudoku_cell_line_edit import CellLineEdit
from sudoku_settings import *


class SudokuGridView(QFrame):
    gridLayout = QGridLayout()
    in_edit_mode = True

    def __init__(self):
        super().__init__()

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus) 

        for row in range(9):
            for col in range(9):
                cell = CellLineEdit(row, col)
                cell.installEventFilter(self)
                cell.setReadOnly(True)
        #self.setAttribute(Qt.WA_MacShowFocusRect, False)    # trying to get rid of focus rect
                cell.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
                cell.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                cell.setMaxLength(1)         # only one digit
                cell.setAlignment(Qt.AlignmentFlag.AlignCenter)

                #layout = QVBoxLayout()
                #self.setLayout(layout)
                self.gridLayout.addWidget(cell, row, col)

        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.gridLayout)


    def keyPressEvent(self, event):
        if self.handleKeyPress(event.key()) is False:
            super().keyPressEvent(event)


    def handleKeyPress(self, key):
        if (
            key == Qt.Key.Key_Return or
            key == Qt.Key.Key_Up or
            key == Qt.Key.Key_Down or
            key == Qt.Key.Key_Left or
            key == Qt.Key.Key_Right
        ):
            # move the current focus highlight down and wrap to the next column on return
            currentFocus = self.focusWidget()
            if currentFocus:
                layout = self.layout()
                assert layout is not None
                index = layout.indexOf(currentFocus)
                if isinstance(layout, QGridLayout) and index != -1:
                    pos = layout.getItemPosition(index)
                    if pos is not None: 
                        row, col, _rowSpan, _colSpan = pos # type: ignore
                                # known limitation in PySide6 type stubs
                                # getItemPosition() always returns a 4-tuple at runtime
                        if key == Qt.Key.Key_Return or key == Qt.Key.Key_Down:
                            if row == 8:
                                if col == 8:
                                    col = 0
                                else:
                                    col += 1
                                row = 0
                            else:
                                row += 1
                        elif key == Qt.Key.Key_Up:
                            if row == 0:
                                if col == 0:
                                    col = 8
                                else:
                                    col -= 1
                                row = 8
                            else:
                                row -= 1
                        elif key == Qt.Key.Key_Left:
                            if col == 0:
                                if row == 0:
                                    row = 8
                                else:
                                    row -= 1
                                col = 8
                            else:
                                col -= 1
                        elif key == Qt.Key.Key_Right:
                            if col == 8:
                                if row == 8:
                                    row = 0
                                else:
                                    row += 1
                                col = 0
                            else:
                                col += 1
                        nextFocus = layout.itemAtPosition(row, col)
                        widget = nextFocus.widget() if nextFocus else None
                        if widget is not None:
                            widget.setFocus()
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


    def resizeEvent(self, event):
        super().resizeEvent(event)
        side = min(self.width(), self.height())
        self.resize(side, side)


    def edit_mode(self):
        # toggle read only mode on cells inside the central layout
        self.in_edit_mode = False if self.in_edit_mode else True

        for i in range(self.gridLayout.count()):
            item = self.gridLayout.itemAt(i)
            if item is not None:
                widget = item.widget()
                if isinstance(widget, CellLineEdit):
                    widget.setReadOnly(self.in_edit_mode)

    def eventFilter(self, obj, event):
        # intercept escape key presses from interior cell widget
        if event.type() == QEvent.KeyPress and isinstance(obj, CellLineEdit):
            if event.key() == Qt.Key.Key_Tab:
                super().eventFilter(obj, event)

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

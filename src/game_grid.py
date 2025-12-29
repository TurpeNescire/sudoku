from PySide6.QtWidgets import QFrame
from PySide6.QtCore import QTimer, QEvent

from cell import Cell, GameViewMode
from border_overlay import BorderOverlay
from sudoku_settings import *


class GameGrid(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        #self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self._viewMode = GameViewMode.SOLUTION
        self.installEventFilter(self)

        self._gridSize = GRID_SIZE
        self._cells: list[Cell] = []
        for cellRow in range(self._gridSize):
            for cellCol in range(self._gridSize):
                cell = Cell(cellRow, cellCol, self)
                #cell.installEventFilter(self)
                self._cells.append(cell)

        # overlay widget to draw borders
        self.overlay = BorderOverlay(self._gridSize, self)
        self.overlay.raise_()       # overlay draws last


    def resizeEvent(self, event):
        super().resizeEvent(event)      # TODO: does it matter where this goes?

        gridWidth = self.width()
        gridHeight = self.height()
        size = min(gridWidth, gridHeight)
        cellSize = size // self._gridSize
        
        # compute any extra vertical and horizontal space after
        # finding the size of the cells, we want to draw cells
        # in the middle of this space ( extra space / 2)
        x_offset = (gridWidth - cellSize * self._gridSize) // 2
        y_offset = (gridHeight - cellSize * self._gridSize) // 2

        # set the size and position of every game grid cell
        for row in range(self._gridSize):
            for col in range(self._gridSize):
                index = row * self._gridSize + col
                self._cells[index].setGeometry(
                    x_offset + col * cellSize,
                    y_offset + row * cellSize,
                    cellSize,
                    cellSize
                )

        QTimer.singleShot(OVERLAY_UPDATE_TIMER_MS, self.updateOverlay)

    
    def updateOverlay(self):
        gridWidth = self.width()
        gridHeight = self.height()
        size = min(gridWidth, gridHeight)
        cellSize = size // self._gridSize

        x_offset = (gridWidth - cellSize * self._gridSize) // 2
        y_offset = (gridHeight - cellSize * self._gridSize) // 2

        self.overlay.setGeometry(x_offset, y_offset, cellSize * self._gridSize, cellSize * self._gridSize)
        self.overlay.raise_()  # Optional: ensure stacking order if needed


    def updateGameViewModes(self):
        for cell in self._cells:
            if self._viewMode == GameViewMode.SOLUTION:
                cell.setMode(GameViewMode.SOLUTION)
            elif self._viewMode == GameViewMode.HINT_GRID:
                cell.setMode(GameViewMode.HINT_GRID)
            elif self._viewMode == GameViewMode.HINT_COMPACT:
                cell.setMode(GameViewMode.HINT_COMPACT)


    def setGameModeTo(self, mode: GameViewMode):
        for cell in self._cells:
            cell.setMode(mode)


    def eventFilter(self, obj, event):
        # intercept key press events from interior cell widgets
        # after calling cell.installEventFilter(self) in the constructor
        # we need to do this becasue QLineEdit was eating arrow keys and escape, etc.
        if event.type() == QEvent.Type.KeyPress:
            return self.handleKeyPress(event.key()) 

        return super().eventFilter(obj, event)


    def keyPressEvent(self, event):
        if self.handleKeyPress(event.key()) is False:
            super().keyPressEvent(event)


    def handleKeyPress(self, key):
        # move the current focus highlight to the next cell
        if (
            key == Qt.Key.Key_Return or key == Qt.Key.Key_Up or
            key == Qt.Key.Key_Down or key == Qt.Key.Key_Left or
            key == Qt.Key.Key_Right or key == Qt.Key.Key_Tab
        ):
            currentFocus = self.focusWidget()
            assert isinstance(currentFocus, Cell)
            #print(f"GameGrid.handleKeyPress({key}) with currentFocus {currentFocus}")

            # after getting the current row/col, handle finding the next
            # cells row/col, wrapping the row or column 
            row, col = currentFocus.row, currentFocus.col
            if SCROLL_MODE == "no v wrap":    # don't wrap at the vertical limits
                index = row * 9 + col
                if key == Qt.Key.Key_Return or key == Qt.Key.Key_Down:
                    index = (index + 9) % 81
                elif key == Qt.Key.Key_Up:
                    index = (index - 9) % 81
                elif key == Qt.Key.Key_Left:
                    index = (index - 1) % 81
                elif key == Qt.Key.Key_Right or key == Qt.Key.Key_Tab:
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
                elif key == Qt.Key.Key_Right or key == Qt.Key.Key_Tab:
                    col, row = (col + 1) % 9, row
                    if col == 0:
                        row = (row + 1) % 9
            nextIndex = row * GRID_SIZE + col
            nextFocus = self._cells[nextIndex]
            assert isinstance(nextFocus, Cell)
            #print(f"GameGrid.handleKeyPress({key}) with nextFocus {nextFocus}")
            nextFocus.setFocus()
             # get the widget of the next focus item using new row/col values

            return True
        elif key == Qt.Key.Key_Tab:         # either Qt or MacOS seems to coopt Key_Tab events, this never runs
            return True
        elif key == Qt.Key.Key_Space:
            if self._viewMode == GameViewMode.SOLUTION:
                self._viewMode = GameViewMode.HINT_GRID
            elif self._viewMode == GameViewMode.HINT_GRID:
                self._viewMode = GameViewMode.SOLUTION
            #self.updateGameViewModes()
            self.setGameModeTo(self._viewMode)

            return True
        elif key == Qt.Key.Key_Escape: 
            return True
       
        return False


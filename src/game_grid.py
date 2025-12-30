from PySide6.QtWidgets import QFrame
from PySide6.QtCore import Qt, QTimer, QEvent

from cell import Cell, GameViewModeObject, GameViewMode
from cell_edit import CellEdit
from border_overlay import BorderOverlay
from sudoku_settings import *


class GameGrid(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        #self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self._gameMode = GameViewModeObject()
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


#    def updateGameViewModes(self):
#        for cell in self._cells:
#            if self._viewMode == GameViewMode.SOLUTION:
#                cell.setMode(GameViewMode.SOLUTION)
#            elif self._viewMode == GameViewMode.HINT_GRID:
#                cell.setMode(GameViewMode.HINT_GRID)
#            elif self._viewMode == GameViewMode.HINT_COMPACT:
#                cell.setMode(GameViewMode.HINT_COMPACT)


    def eventFilter(self, obj, event):
        # intercept key press events from interior cell widgets
        # after calling cell.installEventFilter(self) in the constructor
        # we need to do this becasue QLineEdit was eating arrow keys and escape, etc.
        # TODO: make sure CellEdit is receiving the keypresses it needs from handleKeyPress() 
        if event.type() == QEvent.Type.KeyPress:
            return self.handleKeyPress(event.key()) 

        return super().eventFilter(obj, event)


    def keyPressEvent(self, event):
        if self.handleKeyPress(event.key()) is False:
            super().keyPressEvent(event)
        else:
            event.accept()


    def handleKeyPress(self, key):
        # move the current focus highlight to the next cell
        if (
            key == Qt.Key.Key_Return or key == Qt.Key.Key_Up or
            key == Qt.Key.Key_Down or key == Qt.Key.Key_Left or
            key == Qt.Key.Key_Right or key == Qt.Key.Key_Tab
        ):
            currentFocus = self.focusWidget()
            if isinstance(currentFocus, CellEdit):
                currentFocus = currentFocus.parent().parent()
            if not isinstance(currentFocus, Cell):
                print(f"GameGrid key press, current focus is not Cell: {currentFocus}")
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
            QTimer.singleShot(0, nextFocus.setFocus)
            #nextFocus.setFocus()

            return True
        elif key == Qt.Key.Key_Space:
            # cycle modes
            mode = self._gameMode.mode()
            if mode == GameViewMode.SOLUTION:
                self._gameMode.setMode(GameViewMode.HINT_GRID)
            elif mode == GameViewMode.HINT_GRID:
                self._gameMode.setMode(GameViewMode.SOLUTION)
 
            self.setGameModeTo(self._gameMode.mode())

            return True
        elif key == Qt.Key.Key_Escape: 
            return True
       
        return False


    def setGameModeTo(self, mode: GameViewMode):
        if CELL_TRANSITION_ANIMATE and CELL_TRANSITION_ANIMATE_WAVE:
            self.applyModeSwitchWave(mode)
            return

        for cell in self._cells:
            cell.setModeAnimated(mode) if CELL_TRANSITION_ANIMATE is True else cell.setMode(mode)


    def applyModeSwitchWave(self, targetMode: GameViewMode):
        assert CELL_TRANSITION_ANIMATE_WAVE is True
        baseDelay = CELL_TRANSITION_ANIMATE_WAVE_DELAY_MS 

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                cell = self._cells[row * GRID_SIZE + col]
                
                # skip hint mode for filled cells
                # TODO: do we need this to check if the current cell is empty?
                if targetMode == GameViewMode.HINT_GRID: #and not cell.isEmpty():
                    effectiveMode = GameViewMode.SOLUTION
                else:
                    effectiveMode = targetMode

                if CELL_TRANSITION_ANIMATE_WAVE_FROM_FOCUS:
                    focusWidget = self.focusWidget()
                    if not isinstance(focusWidget, Cell):
                        focusWidget = focusWidget.parent().parent()
#                    if not isinstance(focusWidget, Cell):
#                        print(f"GameGrid applyModeSwitchWave focus should be Cell, is {focusWidget}")
                    assert isinstance(focusWidget, Cell)
                    focusRow, focusCol = focusWidget.row, focusWidget.col
                    delay = (abs(row - focusRow) + abs(col - focusCol)) * baseDelay
                else:
                    delay = (row + col) * baseDelay

                QTimer.singleShot(
                        delay,
                        #lambda c=cell, m=effectiveMode: c.setModeAnimated(m)
                        lambda c=cell, m=targetMode: c.setModeAnimated(m)
                )

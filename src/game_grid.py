from PySide6.QtWidgets import QFrame, QApplication
from PySide6.QtCore import Qt, QTimer, QEvent 

from cell import Cell
from cell_hint import CellHint
from game_view_mode import GameViewMode
from border_overlay import BorderOverlay
from sudoku_settings import *


class GameGrid(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._gameMode = GameViewMode.SOLUTION
        self._initialFocusSet = False
        self._currentHoverCell = None

        self._gridSize = GRID_SIZE
        self._cells: list[Cell] = []
        for cellRow in range(self._gridSize):
            for cellCol in range(self._gridSize):
                cell = Cell(cellRow, cellCol, self)
                self._cells.append(cell)

        # overlay widget to draw grid borders
        self._overlay = BorderOverlay(self, self._gridSize)
        self._overlay.raise_()       # overlay draws last

       

    # just to handle program startup so logical focus is set on Cell 0,0
    def showEvent(self, event):
        super().showEvent(event)

        if not self._initialFocusSet:
            self._initialFocusSet = True
            self._focusRow = 0
            self._focusCol = 0
            self._cells[0].setFocused(True)    


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

        # TODO: why did I make this a singleShot..
        QTimer.singleShot(OVERLAY_UPDATE_TIMER_MS, self.updateBorderOverlay)
 
    # after a window resize, handle resizing the border overlay also
    def updateBorderOverlay(self):
        gridWidth = self.width()
        gridHeight = self.height()
        size = min(gridWidth, gridHeight)
        cellSize = size // self._gridSize

        x_offset = (gridWidth - cellSize * self._gridSize) // 2
        y_offset = (gridHeight - cellSize * self._gridSize) // 2

        self._overlay.setGeometry(x_offset, y_offset, cellSize * self._gridSize, cellSize * self._gridSize)
        self._overlay.raise_()  # Optional: ensure stacking order if needed


    # intercept key and mouse press events from interior cell widgets
    # we need to do this becasue QLineEdit was eating arrow keys and escape, etc.
    def eventFilter(self, obj, event):
        # TODO: this doesn't handle modifier keys, pass event.modifiers() also?
        if event.type() == QEvent.Type.KeyPress:
            if self.handleKeyPress(event.key()):
                return True
        elif event.type() == QEvent.Type.MouseButtonPress or event.type() == QEvent.Type.MouseButtonDblClick:
            if hasattr(obj, "row") and hasattr(obj, "col"):
                oldCell = self._cells[self._focusRow * GRID_SIZE + self._focusCol]
                if isinstance(obj, CellHint):
                    currentCell = obj.parent()
                assert isinstance(currentCell, Cell)
                # focus the current cell if it's a new cell, or toggle focus if it's the same cell
                if currentCell is not oldCell:
                    oldCell.setFocused(False)
                    self._focusRow = obj.row
                    self._focusCol = obj.col
                    currentCell.setFocused(True)
                else:
                    currentCell.setFocused(False if currentCell.getFocused() else True)

                return True
        elif event.type() == QEvent.Type.HoverEnter:
            self._currentHoverCell = obj
            obj.setHovered(True)
        elif event.type() == QEvent.Type.HoverLeave:
            self._currentHoverCell = None
            obj.setHovered(False)
        elif event.type() == QEvent.Type.HoverMove:  # for when hover is cleared, then resumes
            if self._currentHoverCell is None:
                self._currentHoverCell = obj
                obj.setHovered(True)
            # TODO: handle mouse press, hold and move where hover stays after leaving the cell
            # should this be treated as a multiple cell selection, no hovers or focus?


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
            row = self._focusRow
            col = self._focusCol
            currentCell = self._cells[row * GRID_SIZE + col]            
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
            nextFocusCell = self._cells[row * GRID_SIZE + col]
            currentCell.setFocused(False)
            if self._currentHoverCell:
                self._currentHoverCell.setHovered(False)
                self._currentHoverCell = None
            nextFocusCell.setFocused(True)
            self._focusRow = nextFocusCell.row
            self._focusCol = nextFocusCell.col

            return True
        elif key == Qt.Key.Key_Space:
            # cycle modes
            mode = self._gameMode
            if mode == GameViewMode.SOLUTION:
                self._gameMode = GameViewMode.HINT_GRID
            elif mode == GameViewMode.HINT_GRID:
                self._gameMode = GameViewMode.SOLUTION
 
            self.updateGameMode()

            return True
        elif key == Qt.Key.Key_Escape: 
            return True
       
        return False

# TODO: don't need anymore?
#    # clear the focus rect on all cells, then set focus rect on current logical focus cell
#    def updateFocusOverlay(self):
#        for cell in self._cells:
#            cell.setFocused(False)
#
#        index = self._focusRow * GRID_SIZE + self._focusCol
#        if 0 <= index < len(self._cells):
#            self._cells[index].setFocused(True)
#

    def updateGameMode(self, modeToSet=None):       
        mode = modeToSet if modeToSet is not None else self._gameMode

        if CELL_TRANSITION_ANIMATE:
            if CELL_TRANSITION_ANIMATE_WAVE:
                self.applyModeSwitchWave(mode)
            else:
                for cell in self._cells:
                    cell.setViewModeAnimated(mode)
            return

        # update all cells
        for cell in self._cells:
            cell.setViewMode(mode)
       

    # TODO: this needs reworked when we readd animation switching between view modes
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
                    #focusWidget = self.focusWidget()
                    focusWidget = self._cells[self._focusRow * GRID_SIZE + self._focusCol]
                    if not isinstance(focusWidget, Cell):
                        focusWidget = focusWidget.parent().parent()
                    assert isinstance(focusWidget, Cell)
                    focusRow, focusCol = focusWidget.row, focusWidget.col
                    delay = (abs(row - focusRow) + abs(col - focusCol)) * baseDelay
                else:
                    delay = (row + col) * baseDelay

                QTimer.singleShot(
                        delay,
                        #lambda c=cell, m=effectiveMode: c.setModeAnimated(m)
                        lambda c=cell, m=targetMode: c.setViewModeAnimated(m)
                )

from PySide6.QtWidgets import QFrame, QApplication
from PySide6.QtGui import QKeySequence
from PySide6.QtCore import Qt, QTimer, QEvent 

from ux_event import UXEvent, UXFlag
from cell import Cell
from cell_hint import CellHint
from game_view_mode import GameViewMode
from border_overlay import BorderOverlay
from sudoku_settings import *


class GameGrid(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        #self._uxFlags:         UXFlag | None   = None
        self._gameMode:         GameViewMode    = GameViewMode.SOLUTION
        self._initialFocusSet:  bool            = False
        self._focusCell:        Cell | None     = None
        self._oldFocusCell:     Cell | None     = None
        self._hoverCells:       list[Cell]      = []
        self._gridSize:         int             = GRID_SIZE
        self._selectedCells:    list[Cell]      = []
        self._cells:            list[Cell]      = []
        for cellRow in range(self._gridSize):
            for cellCol in range(self._gridSize):
                cell = Cell(cellRow, cellCol, self)
                self._cells.append(cell)

        # overlay widget to draw grid borders
        self._overlay: BorderOverlay = BorderOverlay(self, self._gridSize)
        self._overlay.raise_()       # overlay draws last

       
    # override to handle program startup so logical focus is set on Cell 0,0
    def showEvent(self, event):
        super().showEvent(event)

        if not self._initialFocusSet:
            self._initialFocusSet = True
            uxCtx = UXEvent(None, self._cells[0], UXFlag.SET_LOGICAL_FOCUS)
            self.handleUXEvent(uxCtx)



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
        # QTimer.singleShot(OVERLAY_UPDATE_TIMER_MS, self.updateBorderOverlay)
        self.updateBorderOverlay()

 
    # after a window resize, handle resizing the border overlay also
    def updateBorderOverlay(self):
        gridWidth = self.width()
        gridHeight = self.height()
        size = min(gridWidth, gridHeight)
        cellSize = size // self._gridSize

        x_offset = (gridWidth - cellSize * self._gridSize) // 2
        y_offset = (gridHeight - cellSize * self._gridSize) // 2

        self._overlay.setGeometry(
                x_offset,
                y_offset,
                cellSize * self._gridSize,
                cellSize * self._gridSize
        )
        self._overlay.raise_()  # Optional: ensure stacking order if needed


    # intercept key and mouse press events from interior cell widgets
    # we need to do this becasue QLineEdit was eating arrow keys and escape, etc.
    def eventFilter(self, obj, event):
        # TODO: this doesn't handle modifier keys, pass event.modifiers() also?
        if event.type() == QEvent.Type.KeyPress:
            if self.handleKeyPress(event.key()):
                return True
        elif (
                event.type() == QEvent.Type.MouseButtonPress or
                event.type() == QEvent.Type.MouseButtonDblClick
        ):
            if hasattr(obj, "row") and hasattr(obj, "col"):
                if isinstance(obj, CellHint):
                    currentCell = obj.parent()
                # TODO: will the mouse press ever not be on the CellHint widget?  leave this for now to double check
                assert isinstance(currentCell, Cell)
                uxEvent = UXEvent(self._focusCell, currentCell, UXFlag.CELL_CLICKED | UXFlag.HOVER_LEAVE)
                self.handleUXEvent(uxEvent)
                return True
            return False
        elif event.type() == QEvent.Type.HoverEnter:
            uxEvent = UXEvent(None, obj, UXFlag.HOVER_ENTER)
            self.handleUXEvent(uxEvent)
            return True
        elif event.type() == QEvent.Type.HoverLeave:
            uxEvent = UXEvent(None, obj, UXFlag.HOVER_LEAVE)
            self.handleUXEvent(uxEvent)
            return True
        elif event.type() == QEvent.Type.HoverMove:  # for when hover is cleared, then resumes
            uxEvent = UXEvent(None, obj, UXFlag.HOVER_MOVE)
            self.handleUXEvent(uxEvent)

        return super().eventFilter(obj, event)


    def keyPressEvent(self, event):
        if self.handleKeyPress(event.key()) is False:
            super().keyPressEvent(event)
        else:
            event.accept()


    def handleKeyPress(self, key):
        # move the current focus highlight to the next cell
        if key in MOVEMENT_KEYS:
            assert self._focusCell
            row = self._focusCell.row
            col = self._focusCell.col
            if SCROLL_MODE == "no v wrap":    # don't wrap at the vertical limits
                index = row * GRID_SIZE + col
                numCells = GRID_SIZE * GRID_SIZE
                if key in MOVEMENT_DOWN_KEYS:
                    index = (index + GRID_SIZE) % numCells
                elif key in MOVEMENT_UP_KEYS:
                    index = (index - GRID_SIZE) % numCells
                elif key in MOVEMENT_LEFT_KEYS:
                    index = (index - 1) % numCells
                elif key in MOVEMENT_RIGHT_KEYS:
                    index = (index + 1) % numCells
                row, col = divmod(index, GRID_SIZE)
            elif SCROLL_MODE == "v wrap":      # wrap at the vertical limits
                if key in MOVEMENT_DOWN_KEYS:
                    row, col = (row + 1) % GRID_SIZE, col
                    if row == 0:
                        col = (col + 1) % GRID_SIZE
                elif key in MOVEMENT_UP_KEYS:
                    row, col = (row - 1) % GRID_SIZE, col
                    if row == GRID_SIZE - 1:
                        col = (col - 1) % GRID_SIZE
                elif key in MOVEMENT_LEFT_KEYS:
                    col, row = (col - 1) % GRID_SIZE, row
                    if col == GRID_SIZE - 1:
                        row = (row - 1) % GRID_SIZE
                elif key in MOVEMENT_RIGHT_KEYS:
                    col, row = (col + 1) % GRID_SIZE, row
                    if col == 0:
                        row = (row + 1) % GRID_SIZE
            nextFocusCell = self._cells[row * GRID_SIZE + col]
            flags: UXFlag = (
                UXFlag.HOVER_LEAVE |
                UXFlag.UNSET_LOGICAL_FOCUS |
                UXFlag.SET_LOGICAL_FOCUS
            )
            uxEvent = UXEvent(self._focusCell, nextFocusCell, flags)
            self.handleUXEvent(uxEvent)

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
        elif key in DIGIT_KEYS: 
            assert self._focusCell
            #print(f"GameGrid digit key pressed on Cell r{self._focusCell.row}c{self._focusCell.col}")
            digitFlags = (UXFlag.SET_DIGIT | UXFlag.HOVER_LEAVE)
            uxEvent = UXEvent(self._oldFocusCell, self._focusCell, digitFlags, key)
            self.handleUXEvent(uxEvent)
            # don't return True, we want to handle this both programatically in
            # handleUXEvent, and let handleKeyPress() send the event on to
            # the CellEdit in the event chain - to think about, will this
            # ever cause an issue where CellEdit gets a digit press event
            # before we've handled the CellEdit state through handleUXEvent()?
            return False
        elif key in (Qt.Key.Key_Delete, Qt.Key.Key_Backspace):
            assert self._focusCell
            #print(f"GameGrid delete pressed on Cell r{self._focusCell.row}c{self._focusCell.col}")
            deleteFlags = (UXFlag.CLEAR_CELL | UXFlag.HOVER_LEAVE)
            uxEvent = UXEvent(self._oldFocusCell, self._focusCell, deleteFlags)
            self.handleUXEvent(uxEvent)
            return True
        elif key == Qt.Key.Key_Escape: 
            return True
       
        return False


    def handleUXEvent(self, uxEvent: UXEvent) -> None:
        oldCell = uxEvent.oldCell if isinstance(uxEvent.oldCell, Cell) else None
        cell = uxEvent.cell if isinstance(uxEvent.cell, Cell) else None

        if UXFlag.SET_LOGICAL_FOCUS in uxEvent.flags:
            assert cell
            cell.setFocused(True)    
            self._focusCell = cell

        if UXFlag.UNSET_LOGICAL_FOCUS in uxEvent.flags:
            if oldCell:
                oldCell.setFocused(False)
            else:
                assert cell
                cell.setFocused(False)

        if UXFlag.CELL_CLICKED in uxEvent.flags:
            assert cell
            # focus the current cell if it's a new cell
            if cell is not oldCell:
                assert oldCell
                oldCell.setFocused(False)
                self._focusCell = cell
                cell.setFocused(True) 
            else:   # toggle focus on the same cell
                # TODO: remove, too cute
                cell.setFocused(False if cell.isFocused() else True)
#                if cell.isFocused():
#                    cell.setFocused(True)
#                else:
#                    cell.setFocused(False)

        if UXFlag.HOVER_ENTER in uxEvent.flags:
            assert cell
            self._hoverCells.append(cell)
            cell.setHovered(True)
        if UXFlag.HOVER_LEAVE in uxEvent.flags:
            while len(self._hoverCells) > 0:
                hoverCell = self._hoverCells.pop()
                hoverCell.setHovered(False)
        if UXFlag.HOVER_MOVE in uxEvent.flags:
            if len(self._hoverCells) > 0 and cell:
                self._hoverCells.append(cell)
                cell.setHovered(True)

        if UXFlag.SET_DIGIT in uxEvent.flags:
            assert (cell and uxEvent.key)
            cell.digitEntered(int(QKeySequence(uxEvent.key).toString()))
        if UXFlag.CLEAR_CELL in uxEvent.flags:
            assert cell
            #print(f"GameGrid.handleUXEvent() CLEAR_CELL on r{cell.row}c{cell.col}")
            cell.clearCell()


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
        #print("GameGrid applyModeSwitchWave()")
        assert CELL_TRANSITION_ANIMATE_WAVE is True
        baseDelay = CELL_TRANSITION_ANIMATE_WAVE_DELAY_MS 

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                cell = self._cells[row * GRID_SIZE + col]
                
                # skip hint mode for filled cells
                # TODO: do we need this to check if the current cell is empty?
                if targetMode == GameViewMode.HINT_GRID and not cell.isEmpty():
                    effectiveMode = GameViewMode.SOLUTION
                else:
                    effectiveMode = targetMode

                if CELL_TRANSITION_ANIMATE_WAVE_FROM_FOCUS:
                    assert self._focusCell
                    focusRow, focusCol = self._focusCell.row, self._focusCell.col
                    delay = (abs(row - focusRow) + abs(col - focusCol)) * baseDelay
                else:
                    delay = (row + col) * baseDelay

                QTimer.singleShot(
                        delay,
                        lambda c=cell, m=effectiveMode: c.setViewModeAnimated(m)
                        #lambda c=cell, m=targetMode: c.setViewModeAnimated(m)
                )



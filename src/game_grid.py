from PySide6.QtWidgets import QFrame

from cell import Cell, GameViewMode
from border_overlay import BorderOverlay
from sudoku_settings import *
GRID_SIZE = 9


class GameGrid(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._gridSize = GRID_SIZE
        self._cells: list[Cell] = []
        for cellRow in range(self._gridSize):
            for cellCol in range(self._gridSize):
                cell = Cell(cellRow, cellCol, self)
                self._cells.append(cell)

        # overlay widget to draw borders
        self.overlay = BorderOverlay(self._gridSize, self)
        self.overlay.raise_()


    def resizeEvent(self, event):
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

        # set overlay to cover the entire game grid
        self.overlay.setGeometry(x_offset, y_offset, cellSize * self._gridSize, cellSize * self._gridSize)

        super().resizeEvent(event)


    def set_all_cells_mode(self, mode: GameViewMode):
        for cell in self._cells:
            cell.set_mode(mode)

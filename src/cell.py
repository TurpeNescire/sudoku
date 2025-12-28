from enum import Enum

from PySide6.QtWidgets import QWidget, QStackedWidget
from PySide6.QtCore import QObject, QEnum

from cell_edit import CellEdit
from hint_container import HintContainer


class GameViewMode(Enum):
    SOLUTION = 0            # show CellEdit
    HINT_GRID = 1           # show HintContainer
    HINT_COMPACT = 2        # show CompactHint

class GameViewObject(QObject):
    # Make enum accessible to Qt meta system
    QEnum(GameViewMode)

    def __init__(self, mode: GameViewMode = GameViewMode.SOLUTION):
        super().__init__()
        self.mode = mode


class Cell(QWidget):
    def __init__(self, row, col, parent=None):
        super().__init__(parent)
        self.row = row
        self.col = col

        # stacked widget for switching between multiple game view modes
        self._stacked = QStackedWidget(self)
        self._cellEdit = CellEdit(row, col)
        self._hintContainer = HintContainer()

        self._stacked.addWidget(self._cellEdit)
        self._stacked.addWidget(self._hintContainer)


        self._gameMode = GameViewObject()
        #self._stacked.setCurrentWidget(self._cellEdit)
        #self.setMode(GameViewMode.HINT_GRID)
        self.setMode(GameViewMode.SOLUTION)


    def resizeEvent(self, event):
        self._stacked.setGeometry(self.rect())
        super().resizeEvent(event)


    def setMode(self, mode: GameViewMode):
        self._gameMode = mode
        if mode == GameViewMode.SOLUTION:
            self._stacked.setCurrentWidget(self._cellEdit)
        elif mode == GameViewMode.HINT_GRID or mode == GameViewMode.HINT_COMPACT:
            self._stacked.setCurrentWidget(self._hintContainer)


    def cycleMode(self):
        if self._gameMode == GameViewMode.SOLUTION:
            self.setMode(GameViewMode.HINT_GRID)
        elif self._gameMode == GameViewMode.HINT_GRID:
            self.setMode(GameViewMode.HINT_COMPACT)
        elif self._gameMode == GameViewMode.HINT_COMPACT:
            self.setMode(GameViewMode.SOLUTION)


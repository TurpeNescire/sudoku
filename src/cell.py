from enum import Enum

from PySide6.QtWidgets import QWidget, QStackedWidget, QGraphicsOpacityEffect
from PySide6.QtCore import Qt, QObject, QEnum, QPropertyAnimation, QEasingCurve

from cell_edit import CellEdit
from hint_container import HintContainer
from cell_focus_overlay import CellFocusOverlay


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
    def __init__(self, row, col, parent):
        super().__init__(parent)

        self.row = row
        self.col = col

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        # allow paintEvent to trigger for drawing focus
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self._hasFocus = False

        # stacked widget for switching between multiple game view modes
        self._stacked = QStackedWidget(self)

        self._focusOverlay = CellFocusOverlay(self)
        self._focusOverlay.setGeometry(self.rect())
        self._focusOverlay.raise_()

        self._cellEdit = CellEdit(row, col)
        self._cellEdit.installEventFilter(parent)
        self._hintContainer = HintContainer()
        self._hintContainer.installEventFilter(parent)

        self._stacked.addWidget(self._cellEdit)
        self._stacked.addWidget(self._hintContainer)


        self._gameMode = GameViewObject()
        #self._stacked.setCurrentWidget(self._cellEdit)
        #self.setMode(GameViewMode.HINT_GRID)
        self.setMode(GameViewMode.SOLUTION)
       

    def resizeEvent(self, event):
        self._stacked.setGeometry(self.rect())
        self._focusOverlay.setGeometry(self.rect())
        super().resizeEvent(event)


    def focusInEvent(self, event):
        self._hasFocus = True
        self._focusOverlay.setFocused(True)
        super().focusInEvent(event)


    def focusOutEvent(self, event):
        self._hasFocus = False
        self._focusOverlay.setFocused(False)
        super().focusOutEvent(event)


    def setMode(self, mode: GameViewMode):
        self._gameMode = mode
        if mode == GameViewMode.SOLUTION:
            self._stacked.setCurrentWidget(self._cellEdit)
        elif mode == GameViewMode.HINT_GRID or mode == GameViewMode.HINT_COMPACT:
            self._stacked.setCurrentWidget(self._hintContainer)
        elif mode == GameViewMode.HINT_COMPACT:
            print(f"{self.__repr__}.setMode {mode} set, not implemented")
            #self._stacked.setCurrentWidget(self._hintCompact)


    def cycleMode(self):
        if self._gameMode == GameViewMode.SOLUTION:
            self.setMode(GameViewMode.HINT_GRID)
        elif self._gameMode == GameViewMode.HINT_GRID:
            self.setMode(GameViewMode.HINT_COMPACT)
        elif self._gameMode == GameViewMode.HINT_COMPACT:
            self.setMode(GameViewMode.SOLUTION)


from enum import Enum

from PySide6.QtWidgets import QWidget, QStackedWidget, QGraphicsOpacityEffect
from PySide6.QtCore import Qt, QObject, QEnum, QPropertyAnimation, QEasingCurve

from cell_edit import CellEdit
from hint_container import HintContainer
from cell_focus_overlay import CellFocusOverlay
from sudoku_settings import *


class GameViewMode(Enum):
    SOLUTION = 0            # show CellEdit
    HINT_GRID = 1           # show HintContainer
    HINT_COMPACT = 2        # show CompactHint

class GameViewModeObject(QObject):
    # Make enum accessible to Qt meta system
    QEnum(GameViewMode)

    def __init__(self, mode: GameViewMode = GameViewMode.SOLUTION):
        super().__init__()
        self._mode = mode

    def mode(self):
        return self._mode

    def setMode(self, mode):
        self._mode = mode


class Cell(QWidget):
    def __init__(self, row, col, parent):
        super().__init__(parent)

        self.row = row
        self.col = col
        self._gameMode = GameViewModeObject()

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


        # overlay game mode transition effects
        self._cellEditEffect = QGraphicsOpacityEffect(self._cellEdit)
        self._cellEdit.setGraphicsEffect(self._cellEditEffect)
        self._cellEditEffect.setOpacity(1.0)

        self._hintEffect = QGraphicsOpacityEffect(self._hintContainer)
        self._hintContainer.setGraphicsEffect(self._hintEffect)
        self._hintEffect.setOpacity(0.0)

        self._fadeDuration = CELL_TRANSITION_FADE_DURATION_MS

        self._cellEditAnim = QPropertyAnimation(self._cellEditEffect, b"opacity")
        self._cellEditAnim.setDuration(self._fadeDuration)
        self._cellEditAnim.setEasingCurve(QEasingCurve.Type.InOutQuad)

        self._hintAnim = QPropertyAnimation(self._hintEffect, b"opacity")
        self._hintAnim.setDuration(self._fadeDuration)
        self._hintAnim.setEasingCurve(QEasingCurve.Type.InOutQuad)

        self.setMode(GameViewMode.SOLUTION)
       

    def resizeEvent(self, event):
        self._stacked.setGeometry(self.rect())
        self._focusOverlay.setGeometry(self.rect())
        super().resizeEvent(event)


    def setFocus(self, reason=Qt.FocusReason.OtherFocusReason):
        self._hasFocus = True
        assert not (self.focusPolicy() == Qt.FocusPolicy.NoFocus)
        super().setFocus(reason)


    def focusInEvent(self, event):
        self._hasFocus = True
        self._focusOverlay.setFocused(True)
        super().focusInEvent(event)


    def focusOutEvent(self, event):
        self._hasFocus = False
        self._focusOverlay.setFocused(False)
        super().focusOutEvent(event)


    def setMode(self, mode: GameViewMode):
        self._gameMode.setMode(mode)

        # TODO: fix logic if we add new game view mode like HINT_COMPACT
        if mode == GameViewMode.SOLUTION:
            self._stacked.setCurrentWidget(self._cellEdit)
            self._cellEditEffect.setOpacity(1.0)
            self._hintEffect.setOpacity(0.0)
        elif mode == GameViewMode.HINT_GRID or mode == GameViewMode.HINT_COMPACT:
            self._stacked.setCurrentWidget(self._hintContainer)
            self._cellEditEffect.setOpacity(0.0)
            self._hintEffect.setOpacity(1.0)
        elif mode == GameViewMode.HINT_COMPACT:
            raise NotImplementedError
            print(f"{self.__repr__}.setMode {mode} set, not implemented")
            #self._stacked.setCurrentWidget(self._hintCompact)


    def cycleMode(self):
        if self._gameMode == GameViewMode.SOLUTION:
            self.setMode(GameViewMode.HINT_GRID)
        elif self._gameMode == GameViewMode.HINT_GRID:
            self.setMode(GameViewMode.HINT_COMPACT)
        elif self._gameMode == GameViewMode.HINT_COMPACT:
            self.setMode(GameViewMode.SOLUTION)


    def setModeAnimated(self, mode: GameViewMode):
        self.setMode(mode)

        if mode == GameViewMode.SOLUTION:
            cellEditEndValue = 1.0
            hintEndValue = 0.0
        else:
            cellEditEndValue = 0.0
            hintEndValue = 1.0

        self._cellEditAnim.stop()
        self._hintAnim.stop()

        self._cellEditAnim.setStartValue(self._cellEditEffect.opacity())
        self._cellEditAnim.setEndValue(cellEditEndValue)

        self._hintAnim.setStartValue(self._hintEffect.opacity())
        self._hintAnim.setEndValue(hintEndValue)

        self._cellEditAnim.start()
        self._hintAnim.start()


    def isEmpty(self):
        return False if self._cellEdit.text() else True


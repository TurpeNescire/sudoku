from PySide6.QtWidgets import QWidget, QGraphicsOpacityEffect
from PySide6.QtCore import Qt, QEvent, QPropertyAnimation, QEasingCurve

from cell_edit import CellEdit
from cell_hint import CellHint 
from cell_overlay import CellOverlay
from cell_overlay_type import CellOverlayType
from cell_state import CellState
from sudoku_settings import *
from game_view_mode import GameViewMode


class Cell(QWidget):
    def __init__(self, row, col, parent):
        super().__init__(parent)

        self.row = row
        self.col = col
#        from ux_event import UXFlag
#        self.uxFlags: UXFlag = UXFlag.NONE
        self.state = CellState()
        self.isEditing = False
        self._isFocused = False

        # TODO: testing hover events
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        self.setAttribute(Qt.WidgetAttribute.WA_MacShowFocusRect, False)

        # TODO: get rid of this, since we install one on cellEdit and cellHint?
        self.installEventFilter(parent)

        # visible layers
        self._cellEdit = CellEdit(row, col, self)
        self._cellHint = CellHint(row, col, self)
        self._overlay = CellOverlay(self)

        # stacking order
        self._cellEdit.raise_()
        self._cellHint.raise_()
        self._overlay.raise_()

        # TODO: which of these are necessary and why
        # if cellEdit receives an event, parent is first
        # in the chain to filter, if it doesn't handle it
        # then self filters, then cellEdit, so yes this is
        # what we want
        self._cellEdit.installEventFilter(parent)
        self._cellEdit.installEventFilter(self)
        self._cellHint.installEventFilter(parent)
        self._cellHint.installEventFilter(self)

        # bind QLineEdit.textChanged Qt signal
        # TODO: refactor: better to handle programatically from GameGrid key event filter and handleUXEvent?
        #self._cellEdit.textChanged.connect(self._onTextChanged)
        self._cellEdit.editingFinished.connect(self._onEditingFinished)

        # overlay game mode transition effects
        self._cellEditEffect = QGraphicsOpacityEffect(self._cellEdit)
        self._cellEdit.setGraphicsEffect(self._cellEditEffect)
        self._cellEditEffect.setOpacity(1.0)

        self._cellHintEffect = QGraphicsOpacityEffect(self._cellHint)
        self._cellHint.setGraphicsEffect(self._cellHintEffect)
        self._cellHintEffect.setOpacity(0.0)

        # TODO: animation stuff to reimplement when we add back animated view mode switching
        self._fadeDuration = CELL_TRANSITION_FADE_DURATION_MS

        self._cellEditAnim = QPropertyAnimation(self._cellEditEffect, b"opacity")
        self._cellEditAnim.setDuration(self._fadeDuration)
        self._cellEditAnim.setEasingCurve(QEasingCurve.Type.InOutQuad)

        self._cellHintAnim = QPropertyAnimation(self._cellHintEffect, b"opacity")
        self._cellHintAnim.setDuration(self._fadeDuration)
        self._cellHintAnim.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # TODO: should Cell have StrongFocus?
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        # allow paintEvent to trigger for drawing focus
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        # explicitly make _cellEdit the receiver of key events?
        self.setFocusProxy(self._cellEdit)

        self._gameMode = GameViewMode.SOLUTION
       

    def resizeEvent(self, event):
        rect = self.rect()
        self._cellEdit.setGeometry(rect)
        self._cellHint.setGeometry(rect)
        self._overlay.setGeometry(rect)
        self._overlay.raise_()

        super().resizeEvent(event)

    def focusInEvent(self):
        self.setFocused(True)

    def focusOutEvent(self):
        self.setFocused(False)

    def setFocused(self, isFocused=True) -> None:
        self._isFocused = isFocused
        if isFocused:
            self._cellEdit.setFocus()
        self._overlay.setOverlayVisible(CellOverlayType.FOCUS, isFocused)  
        self._overlay.setOverlayVisible(CellOverlayType.BACKGROUND, isFocused)

    def getFocused(self) -> bool:
        return self._isFocused

    def setHovered(self, hovered=True) ->None:
        self._overlay.setOverlayVisible(CellOverlayType.HOVER, hovered)

    # TODO: do we need this?
    def getOverlayVisible(self, overlayType: CellOverlayType) -> bool:
        return self._overlay.getOverlayVisible(overlayType)

    def digitEntered(self, digit: int) -> None:
        if not self.state.given:
            self._cellEdit.setReadOnly(False)
            self._cellEdit.clear()
        if self._gameMode == GameViewMode.HINT_GRID:
            if CELL_TRANSITION_ANIMATE:
                self.setViewModeAnimated(GameViewMode.SOLUTION)
            else:
                self.setViewMode(GameViewMode.SOLUTION)
        self.state.value = digit

    def _onEditingFinished(self) -> None:
        self._cellEdit.setReadOnly(True)
        self._cellEdit.clearFocus()



    def setViewMode(self, mode: GameViewMode) -> None:
        self._gameMode = mode

        if mode == GameViewMode.SOLUTION:
            self._cellEditEffect.setOpacity(1.0)
            self._cellEdit.setVisible(True)
            self._cellHintEffect.setOpacity(0.0)
            self._cellHint.setVisible(False)
        elif mode in (GameViewMode.HINT_GRID, GameViewMode.HINT_COMPACT):
            self._cellHint.setMode(mode)
            self._cellEditEffect.setOpacity(0.0)
            self._cellEdit.setVisible(False)
            self._cellHintEffect.setOpacity(1.0)
            self._cellHint.setVisible(True)


    def setViewModeAnimated(self, mode: GameViewMode):
        self._gameMode = mode

        if mode == GameViewMode.SOLUTION:
            editEndValue = 1.0
            hintEndValue = 0.0
        else:
            editEndValue = 0.0
            hintEndValue = 1.0

        self._cellEditAnim.stop()
        self._cellHintAnim.stop()

        self._cellEditAnim.setStartValue(self._cellEditEffect.opacity())
        self._cellEditAnim.setEndValue(editEndValue)

        self._cellHintAnim.setStartValue(self._cellHintEffect.opacity())
        self._cellHintAnim.setEndValue(hintEndValue)

        self._cellEditAnim.start()
        self._cellHintAnim.start()

    def isEmpty(self):
        return self.state.value is None

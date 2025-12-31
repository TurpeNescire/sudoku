from PySide6.QtWidgets import QWidget, QGraphicsOpacityEffect
from PySide6.QtCore import Qt, QEvent

from cell_edit import CellEdit
from cell_hint import CellHint 
from cell_focus_overlay import CellFocusOverlay
from sudoku_settings import *
from game_view_mode import GameViewMode


class Cell(QWidget):
    def __init__(self, row, col, parent):
        super().__init__(parent)

        self.row = row
        self.col = col

        # TODO: get rid of this, since we install one on cellEdit and cellHint?
        self.installEventFilter(parent)


        # visible layers

        self._cellEdit = CellEdit(row, col, self)
        self._cellHint = CellHint(row, col, self)
        self._focusOverlay = CellFocusOverlay(self)

        # TODO: which of these are necessary and why
        # if cellEdit receives an event, parent is first
        # in the chain to filter, if it doesn't handle it
        # then self filters, then cellEdit, so yes this is
        # what we want
        self._cellEdit.installEventFilter(parent)
        self._cellEdit.installEventFilter(self)
        self._cellHint.installEventFilter(parent)
        self._cellHint.installEventFilter(self)

        # stacking order
        self._cellEdit.raise_()
        self._cellHint.raise_()
        self._focusOverlay.raise_()

        # overlay game mode transition effects
        self._cellEditEffect = QGraphicsOpacityEffect(self._cellEdit)
        self._cellEdit.setGraphicsEffect(self._cellEditEffect)
        self._cellEditEffect.setOpacity(1.0)

        self._cellHintEffect = QGraphicsOpacityEffect(self._cellHint)
        self._cellHint.setGraphicsEffect(self._cellHintEffect)
        self._cellHintEffect.setOpacity(0.0)

        # TODO: animation stuff to reimplement when we add back animated view mode switching
#        self._fadeDuration = CELL_TRANSITION_FADE_DURATION_MS

#        self._cellEditAnim = QPropertyAnimation(self._cellEditEffect, b"opacity")
#        self._cellEditAnim.setDuration(self._fadeDuration)
#        self._cellEditAnim.setEasingCurve(QEasingCurve.Type.InOutQuad)

#        self._hintAnim = QPropertyAnimation(self._hintEffect, b"opacity")
#        self._hintAnim.setDuration(self._fadeDuration)
#        self._hintAnim.setEasingCurve(QEasingCurve.Type.InOutQuad)

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
        self._focusOverlay.setGeometry(rect)
        self._focusOverlay.raise_()

        super().resizeEvent(event)


    def setViewMode(self, mode: GameViewMode):
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


    def focusInEvent(self):
        self.setFocused()

    def focusOutEvent(self):
        self.setFocused(False)

    def setFocused(self, hasFocus=True):
        self._cellEdit.setFocus()
        self._focusOverlay.setFocused(hasFocus)
        

    # TODO: do we need this?
    def getFocused(self):
        return self._focusOverlay.getFocused()


    # TODO: add back when we reintroduce animation switching between view modes
#    def setModeAnimated(self, mode: GameViewMode):
#        self.setMode(mode)
#
#        if mode == GameViewMode.SOLUTION:
#            cellEditEndValue = 1.0
#            hintEndValue = 0.0
#        else:
#            cellEditEndValue = 0.0
#            hintEndValue = 1.0
#
#        self._cellEditAnim.stop()
#        self._hintAnim.stop()
#
#        self._cellEditAnim.setStartValue(self._cellEditEffect.opacity())
#        self._cellEditAnim.setEndValue(cellEditEndValue)
#
#        self._hintAnim.setStartValue(self._hintEffect.opacity())
#        self._hintAnim.setEndValue(hintEndValue)
#
#        self._cellEditAnim.start()
#        self._hintAnim.start()
#

    def isEmpty(self):
        return False if self._cellEdit.text() else True


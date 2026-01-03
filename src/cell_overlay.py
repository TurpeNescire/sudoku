from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QBrush, QPainterPath
from PySide6.QtCore import Qt, QRectF

from cell_overlay_type import CellOverlayType
from sudoku_settings import *


class CellOverlay(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        # TODO: refactor: removing this
#        self._visible = False
        self._overlays: dict[CellOverlayType, bool] = {}

        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)   
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.setAutoFillBackground(False)


    # sets whether the entire overlay is visible or not
    # TODO: refactor: removing this
#    def setVisible(self, visible: bool):
#        self._visible = visible
#        super().setVisible(visible)
#        self.update()

    # set whether a particular type of overlay is visible or not
    def setOverlayVisible(self, overlayType: CellOverlayType, visible: bool = True) -> None:
        self._overlays[overlayType] = visible
        self.update()

    def getOverlayVisible(self, overlayType: CellOverlayType) -> bool:
        # TODO: is this correct?
        return self._overlays.get(overlayType, False)


# TODO: add hover events that don't take focus
    def paintEvent(self, event):
        # TODO: can we remove this and just rely on self._overlays?
        # TODO: refactor: removing this
#        if not self._visible:
#            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()

        # draw each active overlay type
        for overlayType, visible in self._overlays.items():
            if overlayType is None or visible is False:
                continue
            if overlayType == CellOverlayType.FOCUS:
                self._drawFocusRect(painter, rect)
            elif overlayType == CellOverlayType.HOVER:
                self._drawHover(painter, rect)
            elif overlayType == CellOverlayType.HOVER_FOCUS:
                #self._drawHoverFocus(painter, rect)
                pass
            elif overlayType == CellOverlayType.HINT_RECT:
                # self._drawHintRect(painter, rect, digit)
                pass
            elif overlayType == CellOverlayType.BACKGROUND:
                self._drawBackground(painter, rect)

            
    def _drawFocusRect(self, painter, rect):
        #self._drawBackground(painter, rect)

        color = QColor(CELL_FOCUS_RECT_COLOR)
        color.setAlpha(CELL_FOCUS_RECT_ALPHA)
        pen = QPen(color)
        pen.setWidth(CELL_FOCUS_RECT_WIDTH)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        #rect = self.rect().adjusted(4, 4, -4, -4)
        rect = self.rect().adjusted(
                CELL_FOCUS_RECT_INSET,
                CELL_FOCUS_RECT_INSET,
                -CELL_FOCUS_RECT_INSET,
                -CELL_FOCUS_RECT_INSET
        )
        #painter.drawRoundedRect(rect, 4, 4)
        painter.drawRoundedRect(rect, CELL_FOCUS_RECT_RADIUS, CELL_FOCUS_RECT_RADIUS)

    def _drawHover(self, painter, rect):
        #hoverColor = QColor(200, 200, 255, 60)  # semi-transparent light blue
        hoverColor = QColor(HOVER_BACKGROUND_COLOR) 
        hoverColor.setAlpha(HOVER_BACKGROUND_ALPHA)
        painter.fillRect(rect, hoverColor)

    def _drawHoverFocus(self, painter, rect):
        self._drawHover(painter, rect)
        self._drawFocusRect(painter, rect)

    def _drawHintRect(self, painter, rect):
        hintColor = QColor(180, 255, 180, 80)  # semi-transparent light green
        painter.fillRect(rect, hintColor)

    def _drawBackground(self, painter, rect):
        # bgColor = QColor(240, 240, 240)
        # painter.fillRect(rect, bgColor)

        bgColor = QColor(CELL_FOCUS_BACKGROUND_COLOR)
        bgColor.setAlpha(CELL_FOCUS_BACKGROUND_ALPHA)
        bgPen = QPen(bgColor)
        painter.setPen(bgPen)
        bgBrush = QBrush(bgColor)
        painter.setBrush(bgBrush)

        path = QPainterPath()
        CELL_FOCUS_BACKGROUND_INSET = 0
        rect.adjust(
                CELL_FOCUS_BACKGROUND_INSET,
                CELL_FOCUS_BACKGROUND_INSET,
                -CELL_FOCUS_BACKGROUND_INSET,
                -CELL_FOCUS_BACKGROUND_INSET
        )
        path.addRect(rect)
        painter.fillPath(path, painter.brush())
        painter.strokePath(path, painter.pen())
        # end drawing background color



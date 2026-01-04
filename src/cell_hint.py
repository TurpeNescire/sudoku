from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QRectF, QRect
from PySide6.QtGui import QPainter, QColor, QFont 

from game_view_mode import GameViewMode
from sudoku_settings import *


class CellHint(QWidget):
    def __init__(self, row: int, col: int, parent):
        super().__init__(parent)

        self.row = row
        self.col = col
        self._mode = GameViewMode.HINT_GRID
        #self._hints = list(range(1,10))

        # TODO: ai slop for random hints
        import random
        list_type = random.choices(['all_false', 'mixed'], weights=[1, 3])[0]
        if list_type == 'all_false':
            self._hints = [False] * 9
        else:
            count = random.randint(1, 9)
            values = [True] * count + [False] * (9 - count)
            random.shuffle(values)
            self._hints = values
        #print(self._hints)

        # TODO: ai slop for random digit hints
#        import random
#        digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
#        # Higher weight increases chance of selecting ['']
#        list_type = random.choices(['single_empty', 'mixed'], weights=[3, 1])[0]
#        if list_type == 'single_empty':
#            self._hints = ['']
#        else:
#            length = random.randint(1, 9)
#            self._hints = [random.choice(digits) for _ in range(length)]
#        print(self._hints)
        
        #self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # TODO: while having issues with click focus not working in hint modes,
        # this WA doesn't appear to matter for why CellHint mouse events are
        # never being seen
        #self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)

        # TODO: is this necessary?  doesn't appear to be
        #self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, True)

        # TODO: remove, doesn't seem necessary
        #self.setAutoFillBackground(False)


#    def setMode(self, mode: GameViewMode):
#        self._mode = mode
#        self.update()

    def setHints(self, hints):
        self._hints = hints
        self.update()


#    def mousePressEvent(self, event):
#        print(f"r{self.row}c{self.col} {self}.mousePressEvent {event}")
#        super().mousePressEvent(event)
#        #event.ignore()
#
#    def mouseReleaseEvent(self, event):
#        print(f"r{self.row}c{self.col} {self}.mouseReleaseEvent {event}")
#        super().mouseReleaseEvent(event)
#        #event.ignore()
#
#    def mouseDoubleClickEvent(self, event):
#        print(f"r{self.row}c{self.col} {self}.mouseDoubleClickEvent {event}")
#        super().mouseReleaseEvent(event)
#        #event.ignore()


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.fillRect(self.rect(), CELL_HINT_BACKGROUND_COLOR)
        
        if self._mode == GameViewMode.HINT_GRID:
            self._paintCellHints(painter)
        elif self._mode == GameViewMode.HINT_COMPACT:
            self._paintCompactHints(painter)

    
    def _paintCellHints(self, painter): 
        availableWidth = self.width()
        availableHeight = self.height()
        cellSize = min(availableWidth, availableHeight)
        inset = cellSize * CELL_HINT_INSET_RATIO
        # sanity check inset amount, it should be in pixels now
        inset = max(CELL_HINT_INSET_MIN, inset)
        inset = min(CELL_HINT_INSET_MAX, inset)

        newCellSize = cellSize - inset * 2
        left = (self.width() - newCellSize) / 2
        top = (self.height() - newCellSize) / 2
        left = int(round(left))
        top = int(round(top))
        size = int(round(newCellSize))
        drawRect = QRect(left, top, size, size)
        hintSize = newCellSize / 3

        #font = QFont("Arial", int(round(min(hintSize, hintSize) / HINT_FONT_SIZE_SCALE)))
        font = QFont(CELL_HINT_FONT_FAMILY, int(round(min(hintSize, hintSize) / CELL_HINT_FONT_SIZE_SCALE)))
        painter.setFont(font)
        painter.setPen(QColor(CELL_HINT_FONT_COLOR))

        # TODO: if we're using self._hints as True/False based on index
        for index, value in enumerate(self._hints):
            row = index % 3
            col = index // 3
            hint_text = str(index + 1) if self._hints[index] else '' 

            hintRect = QRectF(
                    drawRect.left() + col * hintSize,
                    drawRect.top() + row * hintSize,
                    hintSize,
                    hintSize
            )
            
            painter.drawText(
                hintRect,
                Qt.AlignmentFlag.AlignCenter,
                hint_text
            )

            painter.drawText(
                    hintRect,
                    Qt.AlignmentFlag.AlignCenter,
                    hint_text
            )       


    def _paintCompactHints(self, painter):
        print(f"{self}._paintCompactHints stub")

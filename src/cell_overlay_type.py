from enum import Enum

from PySide6.QtCore import QObject, QEnum


class CellOverlayType(Enum):
    NONE = 0                
    FOCUS = 1               # show logical focus rect
    HOVER = 2               # hover background highlight
    HOVER_FOCUS = 3         # mouseover hover highlight with temporary focus rect
    HINT_RECT = 4           # show logical focus rect on specific hint digit
    SELECTED = 5            # selection background highlight
    BACKGROUND = 6          # highlight background

class CellOverlayTypeObject(QObject):
    # Make enum accessible to Qt meta system
    QEnum(CellOverlayType)

    def __init__(self, overlayType: CellOverlayType = CellOverlayType.NONE):
        super().__init__()
        self._overlayType = overlayType

    def getOverlayType(self):
        return self._overlayType

    def setOverlayType(self, overlayType):
        self._overlayType = overlayType




from enum import Enum

from PySide6.QtCore import QObject, QEnum


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



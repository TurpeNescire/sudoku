'''
Key Bitwise Operations:
OR (|): Combines flags.
Example: Flag.A | Flag.B creates a new IntFlag with both A and B set.
AND (&): Tests if a flag is set.
Example: (flags & Flag.A) is non-zero if A is active.
XOR (^): Toggles flags.
Example: flags ^ Flag.C flips the state of C.

Example:
if (UXFlag.flagA | UXFlag.flagB) in otherFlags:
    print("At least flagA and flagB are set")
'''

from enum import IntFlag, auto

from PySide6.QtCore import Qt

from cell import Cell


# TODO: separate into board flags and cell flags?
class UXFlag(IntFlag):
    NONE = 0

    # hover
    HOVER_ENTER = auto()
    HOVER_LEAVE = auto()
    HOVER_MOVE = auto()

    # mouse
    CELL_CLICKED = auto()
    CELL_DOUBLE_CLICKED = auto()

    # digit solution press
    SET_DIGIT = auto()
    CLEAR_CELL = auto()

    # logical focus
    HAS_LOGICAL_FOCUS = auto()
    SET_LOGICAL_FOCUS = auto()
    UNSET_LOGICAL_FOCUS = auto()

    # Qt focus
    HAS_QT_FOCUS = auto()
    SET_QT_FOCUS = auto()
    UNSET_QT_FOCUS = auto()

    # hints / modes
    SET_HINT_FOCUS = auto()
    UNSET_HINT_FOCUS = auto()

    # SET_INITIAL_FOCUS = auto()    # TODO: don't need? just use SET_LOGICAL_FOCUS


class UXEvent:
    def __init__(
            self,
            oldCell: Cell | None = None,
            cell: Cell | None = None,
            flag: UXFlag = UXFlag.NONE,
            key: Qt.Key | None = None,
    ):
        self.oldCell: Cell | None = oldCell 
        self.cell: Cell | None = cell
        self.flags: UXFlag = flag
        self.key: Qt.Key | None = key
#        self.mouseButton = None         # TODO: remove?

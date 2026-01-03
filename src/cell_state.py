'''
This class is an interface between Cell UI objects and the underlying Sudoku model.
'''

from dataclasses import dataclass, field

@dataclass
class CellState:
    value: int | None = None    # Cell solution value, e.g. None or 1-9
    given: bool = False         # is this Cell's value part of the initial puzzle's given solutions
    hints: set[int] = field(default_factory=set)     # each CellState object has its own unique set, not shared
    selected: bool = False      # the Cell is currently part of the UI selection
    conflicting: bool = False   # the Cell solution conflicts with the given Solutions


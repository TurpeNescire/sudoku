from dataclasses import dataclass, field


@dataclass
class GridState:
    from cell import Cell

    logicalFocusCell: Cell | None = None
    qtFocusCell: Cell | None = None
    hovering: bool = False

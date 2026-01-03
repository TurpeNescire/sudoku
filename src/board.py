from cell_state import CellState


class SudokuBoard:
    def __init__(self):
        self.cells: list[CellState] = [CellState() for _ in range(81)]

    def cell(self, row: int, col: int) -> CellState:
        return self.cells[row * 9 + col]


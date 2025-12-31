## File "game_grid.py"
    
### `GameGrid()`
- initializes the following instance variables
`self._gridSize: int`
`self._focusRow: int`
`self._focusCol: int`
`self._gameMode: GameViewMode`
`self._overlay: BorderOverlay`
`self._cells: list[Cell]`
- `_gridSize`tracks the dimensions of the Sudoku board, could be something other than 9x9
- `_focusRow` and `_focusCol` track the current logical focus `Cell` position
- `_gameMode` tracks the current game view (`SOLUTION`, `HINT_GRID` or `HINT_COMPACT`)
- `_overlay` is a `BorderOverlay`widget that draws Sudoku grids onto the `GameGrid` widget.
- `_cells`contains `_gridSize * _gridSize` `Cell` widgets.

#### `resizeEvent(event: QResizeEvent)`
- on window resizes, calculates the current size to set the central `GameGrid`
- also how to resize each individual cell of `GRID_SIZE` x `GRID_SIZE`
- calls `updateOverlay()` to redraw the border overlay

#### `updateOverlay()`
- updates `self._overlay` after `resizeEvent()`, recalculating the drawing of the overlay border

#### `eventFilter(obj: QObject, event: QEvent)`
- filters `QEvent.Type.KeyPress`
    - passes `event.key()` to `handleKeyPress(key: Qt.Key) -> bool`
	- returns `True` if `handleKeyPress()` "used" the key and returns `True`, otherwise passes the event on to the next event filter object
		- We install the game's `GameGrid` object in its child widgets as an event filter using (pseudocode here) `observedWidget.installEventFilter(gameGridObserverWidget)`, so if a child widget receives an event, we filter it here first and pass it on if it's not handled, like regular keypresses that will go to the `CellEdit`
- filters `QEvent.Type.MouseButtonPress`
	- checks that `hasattr(obj, "row")` and `hasattr(obj, "col")`
		- in other words, obj is a`Cell`, `CellEdit` or `CellHint`
	- finds the previous focus `Cell` using `self._focusRow` and `self._focusCol`
		- calls `oldCell.setFocused(False)` to stop drawing the focus rectangle on `oldCell` then updates the logical focus position in `self._focusRow` and `self._focusCol` to the new focus position
		- find the new focus `cell` and if we're in `GameViewMode.SOLUTION` call `setFocused(True)` and `setFocus()`, 

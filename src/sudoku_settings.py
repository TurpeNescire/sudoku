from PySide6.QtCore import Qt

WINDOW_TITLE = "Sudoku Solver"
GRID_SIZE = 9
MAIN_WINDOW_X = 100
MAIN_WINDOW_Y = 100
MAIN_WINDOW_WIDTH = 500
MAIN_WINDOW_HEIGHT = 500

SCROLL_MODE = "v wrap" # "wrap/no wrap"

OVERLAY_UPDATE_TIMER_MS = 33

BORDER_THICK_COLOR = "black"
#BORDER_THIN_COLOR = "blue"
BORDER_THIN_COLOR = "lightgray"
BORDER_THIN_STYLE = Qt.PenStyle.DashLine        # SolidLine, DashLine, DotLine, DashDotLine, DashDotDotLine
BORDER_THICK_STYLE = Qt.PenStyle.SolidLine

CELL_EDIT_BACKGROUND_COLOR = "white"
CELL_EDIT_FONT_COLOR = "blue"
CELL_EDIT_BORDER_SIZE = "none"
CELL_EDIT_PADDING_SIZE = 0

HINT_BACKGROUND_COLOR = Qt.white      # Qt color enums or color bytes #FF00FF etc., or Qt.transparent
HINT_FONT_SIZE_SCALE = 1.6
HINT_FONT_COLOR = "blue"
HINT_INSET_RATIO = 0.05   # e.g., inset by 12% of cell size
HINT_INSET_MIN = 4        # px
HINT_INSET_MAX = 14       # px

CELL_FOCUS_RECT_COLOR = "#3399FF"
CELL_FOCUS_RECT_ALPHA = 160                # 0-255 (transparent to opaque)
CELL_FOCUS_RECT_WIDTH = 3
CELL_FOCUS_RECT_INSET = 4
CELL_FOCUS_RECT_RADIUS = 4

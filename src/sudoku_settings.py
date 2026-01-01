from PySide6.QtCore import Qt

'''
Color values can be Qt.GlobalColor enum values like Qt.GlobalColor.lightGray, a string of the color like "lightGray", or hexcode values like #FF00FF.
If part of CSS, then color codes can differ, like CSS uses "lightgray" vs. GlobalColor "lightGray".
'''

WINDOW_TITLE = "Sudoku Solver"
GRID_SIZE = 9
MAIN_WINDOW_X = 100
MAIN_WINDOW_Y = 100
MAIN_WINDOW_WIDTH = 500
MAIN_WINDOW_HEIGHT = 500

SHOW_FOCUS_IN_HINT_MODES = True
SHOW_HOVER_HIGHLIGHT = True
OVERLAY_UPDATE_TIMER_MS = 33
SCROLL_MODE = "v wrap" # "wrap/no wrap"

BORDER_THICK_COLOR = "black"
BORDER_THIN_COLOR = "lightgray"
BORDER_THIN_STYLE = Qt.PenStyle.DashLine        # SolidLine, DashLine, DotLine, DashDotLine, DashDotDotLine
BORDER_THICK_STYLE = Qt.PenStyle.SolidLine

CELL_EDIT_BACKGROUND_COLOR = "white"
CELL_EDIT_FONT_FAMILY = "Verdana"
CELL_EDIT_FONT_COLOR = "blue"
CELL_EDIT_FONT_SCALE = 0.7
CELL_EDIT_BORDER_SIZE = "none"
CELL_EDIT_PADDING_SIZE = 0

CELL_HINT_BACKGROUND_COLOR = Qt.GlobalColor.white      # Qt color enums or color bytes #FF00FF etc., or Qt.transparent
CELL_HINT_FONT_FAMILY = "Verdana"
CELL_HINT_FONT_COLOR = "blue"
CELL_HINT_FONT_SIZE_SCALE = 1.6
CELL_HINT_INSET_RATIO = 0.05   # e.g., inset by 12% of cell size
CELL_HINT_INSET_MIN = 4        # px
CELL_HINT_INSET_MAX = 14       # px

CELL_FOCUS_RECT_COLOR = "#3399FF"
CELL_FOCUS_RECT_ALPHA = 160                # 0-255 (transparent to opaque)
CELL_FOCUS_RECT_WIDTH = 3
CELL_FOCUS_RECT_INSET = 5
CELL_FOCUS_RECT_RADIUS = 4
CELL_FOCUS_BACKGROUND_COLOR = "lightGray"
#CELL_FOCUS_BACKGROUND_COLOR = Qt.GlobalColor.lightGray
CELL_FOCUS_BACKGROUND_ALPHA = 85

CELL_TRANSITION_FADE_DURATION_MS = 150
CELL_TRANSITION_ANIMATE = True
CELL_TRANSITION_ANIMATE_WAVE = True
CELL_TRANSITION_ANIMATE_WAVE_DELAY_MS = 20
CELL_TRANSITION_ANIMATE_WAVE_FROM_FOCUS = True

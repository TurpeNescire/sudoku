from PySide6.QtWidgets import QMainWindow, QSizePolicy, QHBoxLayout, QVBoxLayout, QWidget, QLayout
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction 


from sudoku_settings import (
        WINDOW_TITLE, MAIN_WINDOW_X, MAIN_WINDOW_Y,
        MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT
)

from sudoku_grid_view import SudokuGridView


class MainWindow(QMainWindow):
    edit_mode_triggered_signal = Signal()
    solve_mode_triggered_signal = Signal()
    central_widget = SudokuGridView()

    def __init__(self):
        super().__init__()

        self.setWindowTitle(WINDOW_TITLE)
        self.setGeometry(MAIN_WINDOW_X, MAIN_WINDOW_Y, MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)
        #self.setWindowIcon(QIcon('./assets/editor.png'))
        
        # connect signals
        self.edit_mode_triggered_signal.connect(self.central_widget.edit_mode)
        self.solve_mode_triggered_signal.connect(self.solve_mode)

        # set up menus
        menuBar = self.menuBar()
        game_menu = menuBar.addMenu("Game")
        edit_mode_action = QAction("&Edit clues..", self)
        edit_mode_action.setShortcut("Ctrl+E")
        edit_mode_action.setMenuRole(QAction.MenuRole.NoRole)
        edit_mode_action.triggered.connect(self.central_widget.edit_mode)
        game_menu.addAction(edit_mode_action)
        solve_mode_action = QAction("&Solve cells", self)
        solve_mode_action.setShortcut("Ctrl+S")
        solve_mode_action.setMenuRole(QAction.MenuRole.NoRole)
        solve_mode_action.triggered.connect(self.solve_mode)
        game_menu.addAction(solve_mode_action)

        # qmainwindow has to register a central widget
        self.setCentralWidget(self.central_widget)

        self.show()


    def solve_mode(self):
        print("solve mode")



import sys

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Signal 
from PySide6.QtGui import QAction

from game_grid import GameGrid
from sudoku_settings import *


class MainWindow(QMainWindow):
    cycleGameModeTriggeredSignal = Signal()
    #edit_mode_triggered_signal = Signal()
    #solve_mode_triggered_signal = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self._grid = GameGrid()
        self.setCentralWidget(self._grid)
        self.setGeometry(MAIN_WINDOW_X, MAIN_WINDOW_Y, MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)

        # connect signals
        self.cycleGameModeTriggeredSignal.connect(self._grid.updateGameMode)
        #self.solve_mode_triggered_signal.connect(self._grid.solve_mode)

        # set up menus
        menuBar = self.menuBar()
        game_menu = menuBar.addMenu("Game")
        cycleModeAction = QAction("Cycle Game Mode", self)
        cycleModeAction.setShortcut("Ctrl+E")
        cycleModeAction.setMenuRole(QAction.MenuRole.NoRole) 
        cycleModeAction.triggered.connect(self._grid.updateGameMode)
        game_menu.addAction(cycleModeAction)
        #edit_mode_action = QAction("&Edit clues..", self)
        #edit_mode_action.setShortcut("Ctrl+E")
        #edit_mode_action.setMenuRole(QAction.MenuRole.NoRole)
        #edit_mode_action.triggered.connect(self.central_widget.edit_mode)
        #game_menu.addAction(edit_mode_action)
        #solve_mode_action = QAction("&Solve cells", self)
        #solve_mode_action.setShortcut("Ctrl+S")
        #solve_mode_action.setMenuRole(QAction.MenuRole.NoRole)
        #solve_mode_action.triggered.connect(self.solve_mode)
        #game_menu.addAction(solve_mode_action)




if __name__ == "__main__":
    app = QApplication([])
    w = MainWindow()
    w.show()
    sys.exit(app.exec())


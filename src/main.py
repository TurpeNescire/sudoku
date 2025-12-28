import sys

from PySide6.QtWidgets import QApplication, QProxyStyle, QStyle #QWidget, QMainWindow, QGridLayout, QLineEdit,
from PySide6.QtCore import Qt  # imported here to keep top small
#from PySide6.QtCore import QObject, Signal
#from PySide6.QtGui import QAction 

if __name__ == "__main__":
    #app = QApplication(sys.argv)
    app = QApplication([])
    from sudoku_main_window import SudokuMainWindow
    window = SudokuMainWindow()
    sys.exit(app.exec())

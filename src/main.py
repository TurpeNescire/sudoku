import sys

from PySide6.QtWidgets import QApplication, QProxyStyle, QStyle #QWidget, QMainWindow, QGridLayout, QLineEdit,
from PySide6.QtCore import Qt  # imported here to keep top small
#from PySide6.QtCore import QObject, Signal
#from PySide6.QtGui import QAction 

# attempt to suppress qlineedit widget's from having the macos only focus
# rectangle drawn
class NoFocusRectStyle(QProxyStyle):
    def drawPrimitive(self, element, option, painter, widget=None):
        if element == QStyle.PrimitiveElement.PE_FrameFocusRect:
            print("FOUND THE CULPRIT!")
            return  # Skip focus rectangle drawing
        super().drawPrimitive(element, option, painter, widget)




if __name__ == "__main__":
    #app = QApplication(sys.argv)
    app = QApplication([])
    app.setStyle(NoFocusRectStyle())
    from sudoku_main_window import SudokuMainWindow
    window = SudokuMainWindow()
    sys.exit(app.exec())

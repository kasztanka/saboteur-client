from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot

from saboteur_gui import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.create_room.clicked.connect(self.create_room_click)

    @pyqtSlot()
    def create_room_click(self):
        print('Creating room named:', self.ui.room_name.toPlainText())


import sys

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
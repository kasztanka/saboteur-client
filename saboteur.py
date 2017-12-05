import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMessageBox

from saboteur_gui import Ui_MainWindow
from saboteur_client import SaboteurClient
from saboteur_client import IncorrectActionError


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, client, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.client = client
        self.ui = Ui_MainWindow()
        self.setupUi()

    def setupUi(self):
        self.ui.setupUi(self)
        self.ui.create_room.clicked.connect(self.create_room_click)
        self.ui.join_room.clicked.connect(self.join_room_click)
        self.prepare_game()

    def prepare_game(self):
        self.ui.available_rooms.addItems(self.client.get_available_rooms())

    def _validate_action(func):
        def safe_action(self):
            try:
                func(self)
            except IncorrectActionError as e:
                print(e)
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Ta akcja jest niedozwolona")
                msg.setWindowTitle("Niepoprawna akcja")
                msg.exec_()
        return safe_action

    @_validate_action
    @pyqtSlot()
    def create_room_click(self):
        room_name = self.ui.room_name.toPlainText()
        print('Creating room named:', room_name)
        self.client.create_room(room_name)

    @_validate_action
    @pyqtSlot()
    def join_room_click(self):
        room_name = self.ui.available_rooms.currentText()
        print('Joinging room named:', room_name)
        self.client.join_room(room_name)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    client = SaboteurClient()
    w = MainWindow(client)
    w.show()
    sys.exit(app.exec_())
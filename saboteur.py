import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMessageBox

from saboteur_gui import Ui_MainWindow
from saboteur_client import SaboteurClient
from saboteur_client import IncorrectActionError


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.ui = Ui_MainWindow()
        self.setupUi()
        self.client = self.setup_client()
        self.setup_game()

    def setupUi(self):
        self.ui.setupUi(self)
        self.ui.create_room.clicked.connect(self.create_room_click)
        self.ui.join_room.clicked.connect(self.join_room_click)
        self.ui.send_message.clicked.connect(self.send_message_click)
        self.ui.new_message.returnPressed.connect(self.send_message_click)

    def setup_client(self):
        client = SaboteurClient()
        client.receive_message.connect(self.receive_message)
        client.start()
        return client

    def setup_game(self):
        self.ui.available_rooms.addItems(self.client.get_available_rooms())
        self.ui.chat.clear()

    def _validate_action(func):
        def safe_action(self):
            try:
                func(self)
            except IncorrectActionError as e:
                print(e)
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText('Ta akcja jest niedozwolona')
                msg.setWindowTitle('Niepoprawna akcja')
                msg.exec_()
        return safe_action

    @_validate_action
    @pyqtSlot()
    def create_room_click(self):
        room_name = self.ui.room_name.text()
        print('Creating room named:', room_name)
        self.client.create_room(room_name)

    @_validate_action
    @pyqtSlot()
    def join_room_click(self):
        room_name = self.ui.available_rooms.currentText()
        print('Joinging room named:', room_name)
        self.client.join_room(room_name)

    @pyqtSlot()
    def send_message_click(self):
        message = self.ui.new_message.text()
        self.ui.new_message.clear()
        self.client.send_message(message)
        self.receive_message(message)

    def receive_message(self, message):
        self.ui.chat.append(message)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
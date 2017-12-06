import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMessageBox, QGraphicsScene, QGraphicsView

from saboteur_gui import Ui_MainWindow
from saboteur_client import SaboteurClient
from saboteur_client import IncorrectActionError
from game_board import GameBoard


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.ui = Ui_MainWindow()
        self.setupUi()
        self.client = self.setup_client()
        self.game_board = self.setup_game_board()
        self.prepare_for_next_game()

    def setupUi(self):
        super(MainWindow, self).__init__()
        self.ui.setupUi(self)
        self.ui.create_room.clicked.connect(self.create_room_click)
        self.ui.join_room.clicked.connect(self.join_room_click)
        self.ui.send_message.clicked.connect(self.send_message_click)
        self.ui.new_message.returnPressed.connect(self.send_message_click)

    def setup_game_board(self):
        game_board_scene = QGraphicsScene(self.ui.game_board)
        game_board = GameBoard(self)
        game_board_scene.addItem(game_board)
        game_board_scene.setSceneRect(
            0, 0,
            GameBoard.CARD_WIDTH * GameBoard.COLS,
            GameBoard.CARD_HEIGHT * GameBoard.ROWS
        )
        self.ui.game_board.setScene(game_board_scene)
        self.ui.game_board.setCacheMode(QGraphicsView.CacheBackground)
        return game_board

    def setup_client(self):
        client = SaboteurClient()
        client.receive_message.connect(self.receive_message)
        client.start()
        return client

    def prepare_for_next_game(self):
        self.ui.available_rooms.addItems(self.client.get_available_rooms())
        self.ui.chat.clear()
        #self.game_board.reset_cards()

    def validate_action(func):
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

    @validate_action
    @pyqtSlot()
    def create_room_click(self):
        room_name = self.ui.room_name.text()
        print('Creating room named:', room_name)
        self.client.create_room(room_name)

    @validate_action
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
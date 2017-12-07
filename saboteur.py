import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QMessageBox, QGraphicsScene, QGraphicsView, QListWidgetItem

from blockades import Blockades
from cards import Card
from player import Player
from saboteur_gui import Ui_MainWindow
from saboteur_client import SaboteurClient
from saboteur_client import IncorrectActionError
from board import GameBoard, HandBoard


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.ui = Ui_MainWindow()
        self.setupUi()
        self.client = self.setup_client()
        self.game_board = self.setup_game_board()
        self.hand_board = self.setup_hand_board()
        self.selected_card = None
        self.prepare_for_next_game()

    def setupUi(self):
        super(MainWindow, self).__init__()
        self.ui.setupUi(self)
        self.ui.create_room.clicked.connect(self.create_room_click)
        self.ui.join_room.clicked.connect(self.join_room_click)
        self.ui.send_message.clicked.connect(self.send_message_click)
        self.ui.new_message.returnPressed.connect(self.send_message_click)

    def setup_game_board(self):
        game_board = GameBoard(self)
        self.setup_board(self.ui.game_board, game_board)
        return game_board

    def setup_hand_board(self):
        hand_board = HandBoard(self)
        self.setup_board(self.ui.hand_board, hand_board)
        return hand_board

    def setup_board(self, ui_board, board):
        board_scene = QGraphicsScene(ui_board)
        board_scene.addItem(board)
        board_scene.setSceneRect(
            0, 0,
            Card.WIDTH * board.COLS,
            Card.HEIGHT * board.ROWS
        )
        ui_board.setScene(board_scene)
        ui_board.setCacheMode(QGraphicsView.CacheBackground)

    def setup_client(self):
        client = SaboteurClient()
        client.receive_message.connect(self.receive_message)
        client.card_played.connect(self.add_card_to_game_board)
        client.player_joined_room.connect(self.player_joined_room)
        client.player_left_room.connect(self.player_left_room)
        client.block_player.connect(self.add_blockade_to_player)
        client.start()
        return client

    def prepare_for_next_game(self):
        self.ui.available_rooms.addItems(self.client.get_available_rooms())
        self.ui.chat.clear()
        self.selected_card = None
        self.game_board.reset_cards()

    def validate_action(func):
        def safe_action(self, *args, **kwargs):
            try:
                func(self, *args, **kwargs)
            except IncorrectActionError as e:
                print(e)
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText('Ta akcja jest niedozwolona')
                msg.setWindowTitle('Niepoprawna akcja')
                msg.exec_()
        return safe_action

    @validate_action
    def create_room_click(self, event=None):
        room_name = self.ui.room_name.text()
        print('Creating room named:', room_name)
        self.client.create_room(room_name)

    @validate_action
    def join_room_click(self, event=None):
        room_name = self.ui.available_rooms.currentText()
        self.client.join_room(room_name)
        print('Joining room named:', room_name)

    def send_message_click(self, event=None):
        message = self.ui.new_message.text()
        self.ui.new_message.clear()
        self.client.send_message(message)
        self.receive_message(message)

    @pyqtSlot(str)
    def receive_message(self, message):
        self.ui.chat.append(message)

    @validate_action
    def play_tunnel_card(self, x ,y):
        if self.selected_card:
            self.client.play_tunnel_card(x, y, self.selected_card)

    @pyqtSlot(Card)
    def add_card_to_game_board(self, card):
        self.hand_board.remove_selected_card()
        card.is_selected = False
        self.game_board.add_card(card)
        self.selected_card = None

    @pyqtSlot(Player)
    def player_joined_room(self, player):
        new_item = QListWidgetItem()
        new_item.setData(Qt.UserRole, player)
        self.ui.players_list.addItem(new_item)
        self.update_players_list()

    @pyqtSlot(str)
    def player_left_room(self, name_to_delete):
        for i, player in enumerate(self.get_players()):
            if player.name == name_to_delete:
                self.ui.players_list.takeItem(i)
                break

    def update_players_list(self):
        for i in range(self.ui.players_list.count()):
            item = self.ui.players_list.item(i)
            player = item.data(Qt.UserRole)
            item.setText(str(player))

    @pyqtSlot(str, Blockades)
    def add_blockade_to_player(self, name, blockade):
        for player in self.get_players():
            if player.name == name:
                print('blokujemy', str(player))
                player.blockades.add(blockade)
                print('po blokujemy', str(player))
                break
        self.update_players_list()

    def get_players(self):
        players = []
        for i in range(self.ui.players_list.count()):
            players.append(self.ui.players_list.item(i).data(Qt.UserRole))
        return players


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
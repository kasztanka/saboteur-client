import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QListWidgetItem

from blockades import Blockades
from cards import Card
from decorators import validate_action, active_player_required, selected_card_required
from player import Player, LocalPlayer
from saboteur_gui import Ui_MainWindow
from saboteur_client import SaboteurClient
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
        self.local_player = None
        self.prepare_for_next_game()

    def setupUi(self):
        super(MainWindow, self).__init__()
        self.ui.setupUi(self)
        self.ui.create_room.clicked.connect(self.create_room_click)
        self.ui.join_room.clicked.connect(self.join_room_click)
        self.ui.send_message.clicked.connect(self.send_message_click)
        self.ui.new_message.returnPressed.connect(self.send_message_click)

    def setup_client(self):
        client = SaboteurClient()
        client.receive_message.connect(self.receive_message)
        client.card_played.connect(self.add_card_to_game_board)
        client.player_joined_room.connect(self.player_joined_room)
        client.player_left_room.connect(self.player_left_room)
        client.block_player.connect(self.add_blockade_to_player)
        client.heal_player.connect(self.remove_blockade_from_player)
        client.player_activation.connect(self.activate_player)
        client.start_game.connect(self.start_game)
        client.start()
        return client

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

    def prepare_for_next_game(self):
        self.ui.available_rooms.addItems(self.client.get_available_rooms())
        self.ui.chat.clear()
        self.selected_card = None
        self.game_board.reset_cards()

    @pyqtSlot(str)
    def start_game(self, local_player_name):
        self.local_player = LocalPlayer(local_player_name, num_of_cards=0)
        self.player_joined_room(self.local_player)

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
    @active_player_required
    @selected_card_required
    def play_tunnel_card(self, x ,y):
        self.client.play_tunnel_card(x, y, self.selected_card)

    @validate_action
    @active_player_required
    @selected_card_required
    def play_blockade_card(self, player):
        self.client.play_blockade_card(player, self.selected_card)

    @validate_action
    @active_player_required
    @selected_card_required
    def play_heal_card(self, player):
        self.client.play_heal_card(player, self.selected_card)

    @pyqtSlot(Card)
    def add_card_to_game_board(self, card):
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
        player = self.get_player_by_name(name)
        player.blockades.add(blockade)
        self.update_players_list()

    @pyqtSlot(str, Blockades)
    def remove_blockade_from_player(self, name, blockade):
        player = self.get_player_by_name(name)
        player.blockades.discard(blockade)
        self.update_players_list()

    def get_players(self):
        players = []
        for i in range(self.ui.players_list.count()):
            players.append(self.ui.players_list.item(i).data(Qt.UserRole))
        return players

    def get_player_by_name(self, name):
        chosen_player = None
        for player in self.get_players():
            if player.name == name:
                chosen_player = player
                break
        return chosen_player

    @pyqtSlot(str)
    def activate_player(self, name):
        for player in self.get_players():
            player.is_active = False
        player = self.get_player_by_name(name)
        player.is_active = True
        self.update_players_list()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
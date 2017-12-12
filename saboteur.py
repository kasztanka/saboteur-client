import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QListWidgetItem

from blockade import Blockade
from cards import Card, HealCard, BlockCard, TunnelCard
from decorators import validate_action, active_player_required, selected_card_required, IncorrectActionError
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
        self.ui.send_message.clicked.connect(self.send_chat_message_click)
        self.ui.new_message.returnPressed.connect(self.send_chat_message_click)
        self.ui.players_list.clicked.connect(self.play_action_card)

    def setup_client(self):
        client = SaboteurClient()
        client.chat_message_received.connect(self.receive_message)
        client.card_played.connect(self.add_card_to_game_board)
        client.player_joined_room.connect(self.player_joined_room)
        client.player_left_room.connect(self.player_left_room)
        client.player_blocked.connect(self.add_blockade_to_player)
        client.player_healed.connect(self.remove_blockade_from_player)
        client.player_activation.connect(self.activate_player)
        client.game_started.connect(self.start_game)
        client.start()
        return client

    def setup_game_board(self):
        game_board = GameBoard(self)
        game_board.setup(self.ui.game_board)
        return game_board

    def setup_hand_board(self):
        hand_board = HandBoard(self)
        hand_board.setup(self.ui.hand_board)
        return hand_board

    def prepare_for_next_game(self):
        self.ui.available_rooms.addItems(self.client.get_available_rooms())
        self.ui.chat.clear()
        self.selected_card = None
        self.game_board.reset_cards()

    @pyqtSlot()
    def start_game(self):
        self.local_player = LocalPlayer(self.ui.player_name.text(), num_of_cards=0)
        self.player_joined_room(self.local_player)

    @validate_action
    def create_room_click(self, event=None):
        room_name = self.ui.room_name.text()
        player_name = self.get_local_player_name()
        self.client.create_room(room_name, player_name)
        print('Creating room named:', room_name)

    @validate_action
    def join_room_click(self, event=None):
        room_name = self.ui.available_rooms.currentText()
        player_name = self.get_local_player_name()
        self.client.join_room(room_name, player_name)
        print('Joining room named:', room_name)

    def get_local_player_name(self):
        player_name = self.ui.player_name.text()
        self.ui.player_name.setReadOnly(True)
        return player_name

    def send_chat_message_click(self, event=None):
        chat_message = self.ui.new_message.text()
        self.ui.new_message.clear()
        self.client.send_chat_message(chat_message)

    @pyqtSlot(str)
    def receive_message(self, message):
        self.ui.chat.append(message)

    @validate_action
    @selected_card_required
    @active_player_required
    def play_action_card(self, event=None):
        item = self.ui.players_list.currentItem()
        player = item.data(Qt.UserRole)
        if isinstance(self.selected_card, BlockCard):
            self.client.block_player(self.selected_card.blockade, player.name)
        elif isinstance(self.selected_card, HealCard):
            self.client.heal_player(self.selected_card.blockade, player.name)
        else:
            raise IncorrectActionError('Nie możesz zakładać/zdejmować blokad tą kartą.')

    @validate_action
    @selected_card_required
    @active_player_required
    def play_tunnel_card(self, x ,y):
        if isinstance(self.selected_card, TunnelCard):
            self.client.play_tunnel_card(x, y, self.selected_card)
        else:
            raise IncorrectActionError('Nie możesz możesz budować tuneli tą kartą.')

    @pyqtSlot(Card)
    def add_card_to_game_board(self, card):
        self.game_board.add_card(card)

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

    @pyqtSlot(Blockade, str)
    def add_blockade_to_player(self, blockade, name):
        player = self.get_player_by_name(name)
        player.add_blockade(blockade)
        self.update_players_list()

    @pyqtSlot(Blockade, str)
    def remove_blockade_from_player(self, blockade, name):
        player = self.get_player_by_name(name)
        player.remove_blockade(blockade)
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
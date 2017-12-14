import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QListWidgetItem, QMessageBox

from blockade import Blockade
from cards import Card, HealCard, BlockCard, TunnelCard
from decorators import active_player_required, selected_card_required, player_name_required
from player import Player, LocalPlayer
from saboteur_gui import Ui_MainWindow
from saboteur_client import SaboteurClient
from board import GameBoard, HandBoard


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, ip_address, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.ui = Ui_MainWindow()
        self.setupUi()
        self.client = self.setup_client(ip_address)
        self.game_board = self.setup_game_board()
        self.hand_board = self.setup_hand_board()
        self.selected_card = None
        self.local_player = None
        self.player_name = None
        self.room_name = None
        self.prepare_for_next_game()

    def setupUi(self):
        super(MainWindow, self).__init__()
        self.ui.setupUi(self)
        self.ui.create_room.clicked.connect(self.create_room_click)
        self.ui.join_room.clicked.connect(self.join_room_click)
        self.ui.send_message.clicked.connect(self.send_chat_message_click)
        self.ui.new_message.returnPressed.connect(self.send_chat_message_click)
        self.ui.players_list.clicked.connect(self.play_action_card)
        self.ui.draw_card.clicked.connect(self.draw_card)
        self.ui.set_player_name.clicked.connect(self.set_player_name)

    def setup_client(self, ip_address):
        client = SaboteurClient(ip_address)
        client.chat_message_received.connect(self.receive_chat_message)
        client.tunnel_card_played.connect(self.add_card_to_game_board)
        client.player_joined_room.connect(self.add_player_to_room)
        client.player_left_room.connect(self.player_left_room)
        client.player_blocked.connect(self.add_blockade_to_player)
        client.player_healed.connect(self.remove_blockade_from_player)
        client.player_activated.connect(self.activate_player)
        client.game_started.connect(self.start_game)
        client.error_received.connect(self.show_warning)
        client.rooms_received.connect(self.add_rooms)
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
        self.client.request_available_rooms()
        self.ui.chat.clear()
        self.selected_card = None
        self.game_board.reset_cards()

    @pyqtSlot()
    def start_game(self):
        self.update_player_info()

    @player_name_required
    def create_room_click(self, event=None):
        room_name = self.ui.room_name.text()
        self.client.create_room(room_name, self.player_name)
        print('Creating room named:', room_name)

    @player_name_required
    def join_room_click(self, event=None):
        room_number = self.ui.available_rooms.currentIndex()
        self.client.join_room(room_number, self.player_name)
        print('Joining room named:', room_number)

    def set_player_name(self):
        self.player_name = self.ui.player_name.text()
        self.ui.player_name.setReadOnly(True)

    def send_chat_message_click(self, event=None):
        chat_message = self.ui.new_message.text()
        self.ui.new_message.clear()
        self.client.send_chat_message(chat_message)

    @pyqtSlot(str)
    def receive_chat_message(self, message):
        self.ui.chat.append(message)

    @active_player_required
    @selected_card_required
    def play_action_card(self, event=None):
        item = self.ui.players_list.currentItem()
        player = item.data(Qt.UserRole)
        if isinstance(self.selected_card, BlockCard):
            self.client.block_player(self.selected_card.blockade, player.name)
        elif isinstance(self.selected_card, HealCard):
            self.client.heal_player(self.selected_card.blockade, player.name)
        else:
            self.show_warning('Nie możesz zakładać/zdejmować blokad tą kartą.')

    @active_player_required
    @selected_card_required
    def play_tunnel_card(self, x ,y):
        if isinstance(self.selected_card, TunnelCard):
            self.client.play_tunnel_card(x, y, self.selected_card)
        else:
            self.show_warning('Nie możesz możesz budować tuneli tą kartą.')

    @active_player_required
    def draw_card(self):
        self.client.draw_card()

    def discard_used_card(self):
        self.hand_board.remove_selected_card()
        self.selected_card.is_selected = False
        self.selected_card = None

    @pyqtSlot(Card)
    def add_card_to_game_board(self, card):
        self.game_board.add_card(card)

    @pyqtSlot(str)
    def add_player_to_room(self, player_name):
        if player_name == self.player_name:
            player = LocalPlayer(player_name, num_of_cards=5)
            self.local_player = player
        else:
            player = Player(player_name, num_of_cards=5)
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

    @pyqtSlot(str)
    def show_warning(self, warning_message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(warning_message)
        msg.setWindowTitle('Niepoprawna akcja')
        msg.exec_()

    def update_player_info(self):
        player_info_text = '''
        Nazwa gracza: {}
        Pokój: {}
        '''.format(self.player_name, self.room_name)
        self.ui.player_info.setText(player_info_text)

    @pyqtSlot(list)
    def add_rooms(self, rooms):
        self.ui.available_rooms.addItems(rooms)

    def closeEvent(self, *args, **kwargs):
        self.client.network_client.close_connection()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Za mało argumentów. Podaj adres IP serwera.')
        sys.exit(1)
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow(sys.argv[1])
    w.show()
    sys.exit(app.exec_())
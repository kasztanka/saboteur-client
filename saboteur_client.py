from PyQt5.QtCore import QThread, pyqtSignal

from blockade import Blockade
from cards import Card
from client import Client, MessageCode
from decorators import validate_blockade, IncorrectActionError
from player import Player


class SaboteurClient(QThread):
    chat_message_received = pyqtSignal(str)
    card_played = pyqtSignal(Card)
    player_joined_room = pyqtSignal(Player)
    player_left_room = pyqtSignal(str)
    player_blocked = pyqtSignal(Blockade, str)
    player_healed = pyqtSignal(Blockade, str)
    player_activation = pyqtSignal(str)
    game_started = pyqtSignal()

    def __init__(self):
        self.network_client = Client()
        super(SaboteurClient, self).__init__()

    def run(self):
        while True:
            message_code = self.network_client.receive_int()
            if message_code == MessageCode.CHAT_MESSAGE.value:
                chat_message = self.network_client.receive_text()
                print('Receiving message: ', chat_message)
                self.receive_message(chat_message)
            elif message_code == MessageCode.ADD_PLAYER.value:
                new_player_name = self.network_client.receive_text()
                new_player = Player(new_player_name, 0)
                print('Dodamy gracza')
                self.add_player_to_room(new_player)
                print('Dodano gracza')
            elif message_code == MessageCode.INCORRECT_ACTION.value:
                error_message = self.network_client.receive_text()
            else:
                print('Bledny kod: ', message_code)

    def get_available_rooms(self):
        return ['Pokój Piotrka', 'Room 2']

    def create_room(self, room_name, player_name):
        self.network_client.send_int(MessageCode.CREATE_ROOM.value)
        self.send_username(player_name)
        self.network_client.send_text(room_name)
        self.game_started.emit()
        self.activate_player(player_name)

    def join_room(self, room_number, player_name):
        self.network_client.send_int(MessageCode.JOIN_ROOM.value)
        self.send_username(player_name)
        self.network_client.send_int(room_number)
        self.game_started.emit()
        self.activate_player(player_name)

    def send_username(self, username):
        self.network_client.send_text(username)

    def send_chat_message(self, chat_message):
        self.network_client.send_int(MessageCode.CHAT_MESSAGE.value)
        self.network_client.send_text(chat_message)

    def receive_message(self, chat_message):
        self.chat_message_received.emit(chat_message)

    def play_tunnel_card(self, x, y, card):
        card.x = x
        card.y = y
        self.card_played.emit(card)

    def add_player_to_room(self, new_player):
        self.player_joined_room.emit(new_player)

    def delete_player_from_room(self, player_name):
        self.player_left_room.emit(player_name)

    @validate_blockade
    def block_player(self, blockade, player_name):
        self.player_blocked.emit(blockade, player_name)

    @validate_blockade
    def heal_player(self, blockade, player_name):
        self.player_healed.emit(blockade, player_name)

    def activate_player(self, name):
        self.player_activation.emit(name)
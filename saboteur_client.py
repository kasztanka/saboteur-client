from PyQt5.QtCore import QThread, pyqtSignal

from blockade import Blockade
from cards import Card
from client import Client, MessageCode
from player import Player


class SaboteurClient(QThread):
    chat_message_received = pyqtSignal(str)
    tunnel_card_played = pyqtSignal(Card)
    player_joined_room = pyqtSignal(str)
    player_left_room = pyqtSignal(str)
    player_blocked = pyqtSignal(Blockade, str)
    player_healed = pyqtSignal(Blockade, str)
    player_activated = pyqtSignal(str)
    game_started = pyqtSignal()
    error_received = pyqtSignal(str)

    def __init__(self, ip_address):
        self.network_client = Client(ip_address)
        super(SaboteurClient, self).__init__()

    def run(self):
        while True:
            message_code = self.network_client.receive_int()
            if message_code == MessageCode.CHAT_MESSAGE.value:
                chat_message = self.network_client.receive_text()
                self.chat_message_received.emit(chat_message)
            elif message_code == MessageCode.ADD_PLAYER.value:
                new_player_name = self.network_client.receive_text()
                self.player_joined_room.emit(new_player_name)
            elif message_code == MessageCode.INCORRECT_ACTION.value:
                error_message = self.network_client.receive_text()
                self.error_received.emit(error_message)
            else:
                print('Bledny kod: ', message_code)

    def get_available_rooms(self):
        return ['Pokój Piotrka', 'Room 2']

    def create_room(self, room_name, player_name):
        self.network_client.send_int(MessageCode.CREATE_ROOM.value)
        self.send_username(player_name)
        self.network_client.send_text(room_name)
        self.game_started.emit()
        self.player_activated.emit(player_name)

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

    def play_tunnel_card(self, x, y, card):
        card.x = x
        card.y = y
        self.tunnel_card_played.emit(card)

    def draw_card(self):
        pass

    def block_player(self, blockade, player_name):
        self.player_blocked.emit(blockade, player_name)

    def heal_player(self, blockade, player_name):
        self.player_healed.emit(blockade, player_name)

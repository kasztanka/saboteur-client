from PyQt5.QtCore import QThread, pyqtSignal

from blockade import Blockade
from cards import Card
from client import Client, MessageCode
from decorators import validate_blockade, IncorrectActionError
from player import Player


class SaboteurClient(QThread):
    chat_message_received = pyqtSignal(str)
    tunnel_card_played = pyqtSignal(Card)
    player_joined_room = pyqtSignal(Player)
    player_left_room = pyqtSignal(str)
    player_blocked = pyqtSignal(Blockade, str)
    player_healed = pyqtSignal(Blockade, str)
    player_activated = pyqtSignal(str)
    game_started = pyqtSignal()

    def __init__(self):
        self.network_client = Client()
        super(SaboteurClient, self).__init__()

    def run(self):
        while True:
            message_code = self.network_client.receive_int()
            if message_code == MessageCode.CHAT_MESSAGE.value:
                chat_message = self.network_client.receive_text()
                self.receive_message(chat_message)

    def get_available_rooms(self):
        return ['Pokój Piotrka', 'Room 2']

    def create_room(self, room_name, player_name):
        for name, num_of_cards in [('Magda', 4), ('Andrzej', 3)]:
            self.add_player_to_room(Player(name, num_of_cards))
        self.game_started.emit()
        self.activate_player(player_name)

    def join_room(self, room_name, player_name):
        raise IncorrectActionError('Nie możesz dołączać do innych pokoi')

    def send_chat_message(self, chat_message):
        self.network_client.send_int(MessageCode.CHAT_MESSAGE.value)
        self.network_client.send_text(chat_message)

    def receive_chat_message(self, chat_message):
        self.chat_message_received.emit(chat_message)

    def play_tunnel_card(self, x, y, card):
        card.x = x
        card.y = y
        self.tunnel_card_played.emit(card)

    def draw_card(self):
        pass

    def add_player_to_room(self, new_player):
        self.player_joined_room.emit(new_player)

    def delete_player_from_room(self, player_name):
        self.player_left_room.emit(player_name)

    def block_player(self, blockade, player_name):
        self.player_blocked.emit(blockade, player_name)

    def heal_player(self, blockade, player_name):
        self.player_healed.emit(blockade, player_name)

    def activate_player(self, name):
        self.player_activated.emit(name)
from time import sleep

from PyQt5.QtCore import QThread, pyqtSignal

from blockades import Blockades
from cards import Card
from player import Player


class IncorrectActionError(Exception):
    pass


class SaboteurClient(QThread):

    message_received = pyqtSignal(str)
    card_played = pyqtSignal(Card)
    player_joined_room = pyqtSignal(Player)
    player_left_room = pyqtSignal(str)
    player_blocked = pyqtSignal(str, Blockades)
    player_healed = pyqtSignal(str, Blockades)
    player_activation = pyqtSignal(str)
    game_started = pyqtSignal()

    def run(self):
        for i in range(3):
            sleep(4)
            self.receive_message('New message' + str(i))

    def get_available_rooms(self):
        return ['Pokój Piotrka', 'Room 2']

    def create_room(self, room_name, player_name):
        for name, num_of_cards in [('Magda', 4), ('Andrzej', 3)]:
            self.add_player_to_room(Player(name, num_of_cards))
        self.game_started.emit()
        self.activate_player(player_name)

    def join_room(self, room_name, player_name):
        raise IncorrectActionError()

    def send_message(self, message):
        pass

    def receive_message(self, message):
        self.message_received.emit(message)

    def play_tunnel_card(self, x, y, card):
        card.x = x
        card.y = y
        self.card_played.emit(card)

    def add_player_to_room(self, new_player):
        self.player_joined_room.emit(new_player)

    def delete_player_from_room(self, player_name):
        self.player_left_room.emit(player_name)

    def block_player(self, name, blockade):
        self.player_blocked.emit(name, blockade)

    def heal_player(self, name, blockade):
        self.player_healed.emit(name, blockade)

    def activate_player(self, name):
        self.player_activation.emit(name)
from time import sleep

from PyQt5.QtCore import QThread, pyqtSignal

from blockades import Blockades
from cards import Card
from player import Player


class IncorrectActionError(Exception):
    pass


class SaboteurClient(QThread):

    receive_message = pyqtSignal(str)
    card_played = pyqtSignal(Card)
    player_joined_room = pyqtSignal(Player)
    player_left_room = pyqtSignal(str)
    block_player = pyqtSignal(str, Blockades)

    def run(self):
        for i in range(3):
            sleep(1)
            self.receive_message.emit('New message' + str(i))
        for name, num_of_cards in [('Magda', 4), ('Andrzej', 3)]:
            sleep(1)
            self.add_player_to_room(Player(name, num_of_cards))
        sleep(1)
        self.add_blockade_to_player('Andrzej', Blockades.LAMP)
        sleep(2)
        self.delete_player_from_room('Magda')
        print('nie ma klienta')

    def get_available_rooms(self):
        return ['Pokój Piotrka', 'Room 2']

    def create_room(self, room_name):
        pass

    def join_room(self, room_name):
        raise IncorrectActionError()

    def send_message(self, message):
        pass

    def play_tunnel_card(self, x, y, card):
        card.x = x
        card.y = y
        self.card_played.emit(card)

    def add_player_to_room(self, new_player):
        self.player_joined_room.emit(new_player)

    def delete_player_from_room(self, player_name):
        self.player_left_room.emit(player_name)

    def add_blockade_to_player(self, name, blockade):
        self.block_player.emit(name, blockade)
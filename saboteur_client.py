from time import sleep

from PyQt5.QtCore import QThread, pyqtSignal

from cards import Card


class IncorrectActionError(Exception):
    pass


class SaboteurClient(QThread):

    receive_message = pyqtSignal(str)
    card_played = pyqtSignal(Card)

    def run(self):
        for i in range(3):
            sleep(5)
            self.receive_message.emit('New message' + str(i))
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
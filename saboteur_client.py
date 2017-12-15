from PyQt5.QtCore import QThread, pyqtSignal

from blockade import Blockade
from cards import CardType
from client import Client, MessageCode


class SaboteurClient(QThread):
    chat_message_received = pyqtSignal(str)
    card_added_to_game_board = pyqtSignal(str, CardType, int, int)
    card_added_to_hand_board = pyqtSignal(str, CardType)
    player_joined_room = pyqtSignal(str)
    player_left_room = pyqtSignal(str)
    player_blocked = pyqtSignal(Blockade, str)
    player_healed = pyqtSignal(Blockade, str)
    player_activated = pyqtSignal(str)
    game_started = pyqtSignal()
    error_received = pyqtSignal(str)
    rooms_received = pyqtSignal(list)

    def __init__(self, ip_address):
        self.network_client = Client(ip_address)
        super(SaboteurClient, self).__init__()

    def run(self):
        while True:
            message_code = self.network_client.receive_int()
            if message_code == MessageCode.REQUEST_ROOMS.value:
                num_rooms = self.network_client.receive_int()
                rooms = []
                for _ in range(num_rooms):
                    room_name = self.network_client.receive_text()
                    rooms.append(room_name)
                self.rooms_received.emit(rooms)
            elif message_code == MessageCode.CHAT_MESSAGE.value:
                chat_message = self.network_client.receive_text()
                self.chat_message_received.emit(chat_message)
            elif message_code == MessageCode.ADD_PLAYER.value:
                new_player_name = self.network_client.receive_text()
                self.player_joined_room.emit(new_player_name)
            elif message_code == MessageCode.START_GAME.value:
                self.game_started.emit()
            elif message_code == MessageCode.ACTIVATE_PLAYER.value:
                player_name = self.network_client.receive_text()
                self.player_activated.emit(player_name)
            elif message_code == MessageCode.DRAW_CARD.value:
                card_type = self.network_client.receive_int()
                card_name = self.network_client.receive_text()
                print(card_type, card_name)
            elif message_code == MessageCode.INCORRECT_ACTION.value:
                error_message = self.network_client.receive_text()
                self.error_received.emit(error_message)
            else:
                print('Bledny kod: ', message_code)

    def request_available_rooms(self):
        self.network_client.send_int(MessageCode.REQUEST_ROOMS.value)

    def create_room(self, room_name, player_name):
        self.network_client.send_int(MessageCode.CREATE_ROOM.value)
        self.network_client.send_text(player_name)
        self.network_client.send_text(room_name)

    def join_room(self, room_number, player_name):
        self.network_client.send_int(MessageCode.JOIN_ROOM.value)
        self.network_client.send_text(player_name)
        self.network_client.send_int(room_number)

    def send_chat_message(self, chat_message):
        self.network_client.send_int(MessageCode.CHAT_MESSAGE.value)
        self.network_client.send_text(chat_message)

    def play_tunnel_card(self, x, y, card):
        card.x = x
        card.y = y
        self.card_added_to_game_board.emit(card.filename, CardType.TUNNEL, x, y)

    def draw_card(self):
        self.network_client.send_int(MessageCode.DRAW_CARD.value)

    def block_player(self, blockade, player_name):
        self.player_blocked.emit(blockade, player_name)

    def heal_player(self, blockade, player_name):
        self.player_healed.emit(blockade, player_name)

from PyQt5.QtCore import QThread, pyqtSignal
from enum import Enum

from blockade import Blockade
from cards import CardType
from client import Client


class MessageCode(Enum):
    INCORRECT_ACTION = -1
    REQUEST_ROOMS = 0
    CREATE_ROOM = 1
    JOIN_ROOM = 2
    ADD_PLAYER = 3
    CHAT_MESSAGE = 4
    START_GAME = 5
    ACTIVATE_PLAYER = 6
    DRAW_CARD = 7
    ADD_CARD_TO_BOARD = 8
    REMOVE_CARD_FROM_HAND = 9
    BLOCK = 10
    HEAL = 11
    CLOSE_CONNECTION = 12


class SaboteurClient(QThread):
    chat_message_received = pyqtSignal(str)
    card_added_to_game_board = pyqtSignal(str, CardType, int, int, bool)
    card_added_to_hand_board = pyqtSignal(str, CardType)
    player_joined_room = pyqtSignal(str)
    player_left_room = pyqtSignal(str)
    player_blocked = pyqtSignal(Blockade, str)
    player_healed = pyqtSignal(Blockade, str)
    player_activated = pyqtSignal(str)
    game_started = pyqtSignal()
    error_received = pyqtSignal(str)
    rooms_received = pyqtSignal(list)
    card_discarded = pyqtSignal(int)

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
                self.card_added_to_hand_board.emit(card_name, CardType(card_type))
            elif message_code == MessageCode.ADD_CARD_TO_BOARD.value:
                filename = self.network_client.receive_text()
                x = self.network_client.receive_int()
                y = self.network_client.receive_int()
                is_rotated = bool(self.network_client.receive_int())
                self.card_added_to_game_board.emit(filename, CardType.TUNNEL, x, y, is_rotated)
            elif message_code == MessageCode.REMOVE_CARD_FROM_HAND.value:
                card_index = self.network_client.receive_int()
                self.card_discarded.emit(card_index)
            elif message_code == MessageCode.INCORRECT_ACTION.value:
                error_message = self.network_client.receive_text()
                self.error_received.emit(error_message)
            elif message_code == MessageCode.BLOCK.value:
                blockade = self.network_client.receive_int()
                player_name = self.network_client.receive_text()
                self.player_blocked.emit(Blockade(blockade), player_name)
            elif message_code == MessageCode.HEAL.value:
                blockade = self.network_client.receive_int()
                player_name = self.network_client.receive_text()
                self.player_healed.emit(Blockade(blockade), player_name)
            elif message_code == MessageCode.CLOSE_CONNECTION.value:
                break
            else:
                print('Bledny kod: ', message_code)
        self.network_client.sock.close()
        print('Connection closed')

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

    def play_tunnel_card(self, card_index, x, y, is_rotated):
        self.network_client.send_int(MessageCode.ADD_CARD_TO_BOARD.value)
        self.network_client.send_int(card_index)
        self.network_client.send_int(x)
        self.network_client.send_int(y)
        self.network_client.send_int(int(is_rotated))

    def draw_card(self):
        self.network_client.send_int(MessageCode.DRAW_CARD.value)

    def block_player(self, card_index, player_index):
        self.network_client.send_int(MessageCode.BLOCK.value)
        self.network_client.send_int(card_index)
        self.network_client.send_int(player_index)

    def heal_player(self, card_index, player_index):
        self.network_client.send_int(MessageCode.HEAL.value)
        self.network_client.send_int(card_index)
        self.network_client.send_int(player_index)

    def close_connection(self):
        self.network_client.send_int(MessageCode.CLOSE_CONNECTION.value)

import socket
import struct
from enum import Enum


class MessageCode(Enum):
    CHAT_MESSAGE = 1


class Client:
    BUFFER_SIZE = 4

    def __init__(self):
        server_address = ('localhost', 42010)
        print('connecting to {} port {}'.format(*server_address))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(server_address)

    def send_int(self, num):
        packed_int = struct.pack('!i', num)
        self.sock.sendall(packed_int)

    def send_text(self, text):
        self.send_int(len(text))
        self.sock.sendall(text.encode())

    def receive_buffer(self, amount_expected):
        buffer = []
        amount_received = 0
        while amount_received < amount_expected:
            data = self.sock.recv(self.BUFFER_SIZE)
            if data == b'':
                raise RuntimeError('socket connection broken')
            amount_received += len(data)
            buffer.append(data)
        return buffer

    def receive_int(self):
        buffer = self.receive_buffer(4)
        number = struct.unpack('!i', b''.join(buffer))[0]
        return number

    def receive_text(self):
        length = self.receive_int()
        buffer = self.receive_buffer(length)
        text = b''.join(buffer).decode('utf-8')
        return text

    def __del__(self):
        self.sock.close()
        print('Connection closed')

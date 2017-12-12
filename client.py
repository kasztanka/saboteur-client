import socket
import struct
import threading
from enum import Enum


class Code(Enum):
    MESSAGE = 1


class Client():
    BUFFER_SIZE = 4

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_address = ('192.168.0.47', 42010)
        print('connecting to {} port {}'.format(*server_address))
        self.sock.connect(server_address)
        try:
            t1 = threading.Thread(target=self.listen)
            t1.start()
            text = 'Ala budzi cara'
            self.send_message(text)
            t1.join()
        finally:
            print('closing socket')
            self.sock.close()

    def send_message(self, text):
        self.send_int(Code.MESSAGE.value)
        self.send_text(text)

    def send_int(self, num):
        packed_int = struct.pack('!i', num)
        self.sock.sendall(packed_int)

    def send_text(self, text):
        self.send_int(len(text))
        self.sock.sendall(text.encode())

    def listen(self):
        while(True):
            message_num = self.receive_int()
            if message_num == Code.MESSAGE.value:
                print('Odebrano wiadomość: ' + self.receive_text())

    def receive_buffer(self, amount_expected):
        buffer = []
        amount_received = 0
        while amount_received < amount_expected:
            data = self.sock.recv(self.BUFFER_SIZE)
            if data == b'':
                raise RuntimeError("socket connection broken")
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


if __name__ == '__main__':
    a = Client()
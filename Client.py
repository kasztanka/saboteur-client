import socket
import struct


class Client():

    BUFFER_SIZE = 4

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_address = ('192.168.0.106', 42010)
        print('connecting to {} port {}'.format(*server_address))
        self.sock.connect(server_address)
        try:
            self.send_text('Ala budzi cara durne emu fika')
            self.receive_text()
        finally:
            print('closing socket')
            self.sock.close()

    def send_int(self, num):
        packed_int = struct.pack('!i', num)
        print('sending: ', num)
        self.sock.sendall(packed_int)

    def send_text(self, text):
        self.send_int(len(text))
        print('sending: ', text)
        self.sock.sendall(text.encode())

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
        print('receiving: ', number)
        return number

    def receive_text(self):
        length = self.receive_int()
        buffer = self.receive_buffer(length)
        text = b''.join(buffer).decode('utf-8')
        print('receiving: ', text)
        return text


if __name__ == '__main__':
    a = Client()
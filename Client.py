import socket
import struct


class Client():

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_address = ('192.168.0.13', 42010)
        print('connecting to {} port {}'.format(*server_address))
        self.sock.connect(server_address)
        try:

            amount_received = 0
            amount_expected = 3
            char_per_message = 16

            while amount_received < amount_expected:
                data = self.sock.recv(char_per_message)
                amount_received += len(data)
                print('received {}'.format(data))

            self.send_int(14792)
            self.send_text('Ala budzi cara durne emu fika')
            self.send_text('gna hiena i jenot krokiem lunatyka')

        finally:
            print('closing socket')
            self.sock.close()

    def send_int(self, num):
        packed_int = struct.pack('i', num)
        print('sending: ', num)
        self.sock.sendall(packed_int)

    def send_text(self, text):
        self.send_int(len(text))
        print('sending: ', text)
        self.sock.sendall(text.encode())


if __name__ == '__main__':
    a = Client()
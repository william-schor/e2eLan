import socket


class LanSocket(object):
    """docstring for LanSocket"""

    def __init__(self):
        self.sock_tell = None
        self.sock_listen = None

    def connect(self, host, port):
        if self.sock_tell:
            self.sock_tell.shutdown(socket.SHUT_RDWR)

        self.sock_tell = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_tell.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock_tell.connect((host, port))

    def listen(self, host, port):
        if self.sock_listen:
            self.sock_listen.shutdown(socket.SHUT_RDWR)

        self.sock_listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock_listen.bind((host, port))
        self.sock_listen.listen(5)

    def close(self):
        self.sock_tell.close()
        self.sock_listen.close()

    def shutdown(self):
        self.sock_tell.shutdown(socket.SHUT_RDWR)
        self.sock_listen.shutdown(socket.SHUT_RDWR)

    def send(self, message):
        message = f"{len(message)}|{message}".encode("utf-8")
        totalsent = 0
        while totalsent < len(message):
            sent = self.sock_tell.send(message[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def receive(self):
        connection, address = self.sock_listen.accept()

        char = ""
        length = []
        pipe = "|".encode("utf-8")

        while True:
            char = connection.recv(1)
            if char == pipe or not char:
                break
            length.append(char.decode("utf-8"))

        if len(length) == 0:
            return None

        try:
            length = int("".join(length))

        except ValueError:
            print("Message does not follow protocol")
            return None

        return self.receive_all(connection, length)

    def receive_all(self, connection, n):
        data = []
        bytes_rec = 0
        while bytes_rec < n:
            packet = connection.recv(n - len(data))
            if not packet:
                return None
            bytes_rec += len(packet)
            data.append(packet.decode("utf-8"))

        return "".join(data)

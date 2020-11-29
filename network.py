import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # client address will be automatically be
        # fetched
        self.server = "192.168.0.107"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:  # when we try to connect, we will try to immediately send some information back to the object
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()  # we are using decode instead of pickle because we are getting
            # player number, is it player 0 or player 1
            # each player thinks they are player 1 but actually they can be both 0 or 1 depending on the server
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))  # sending string data to the server
            return pickle.loads(self.client.recv(2048))  # we are going to receive object data
        except socket.error as e:
            print(e)

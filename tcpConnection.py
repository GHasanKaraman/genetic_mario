import socket
import threading
import time
import pickle

from sqlalchemy import false

_port = 1234
_server = socket.gethostbyname(socket.gethostname())


class User:
    def __init__(self, clientName, port):
        self.clientName = clientName
        self.port = port
        self.data = ""

    def startListen(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((_server, self.port))
            self.server.listen()
            self.receive_thread = threading.Thread(target=self.receive)
            self.receive_thread.start()
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            return False
        except:
            return True

    def receive(self):
        while True:
            client, address = self.server.accept()

            thread1 = threading.Thread(target=self.getData, args=(client,))
            thread1.start()

    def getData(self, client):
        while True:
            try:
                data = pickle.loads(client.recv(1024))
                self.data = data
            except:
                client.close()
                break

    def sendData(self, msg):
        self.client.send(pickle.dumps(msg))
        time.sleep(0.1)

    def clientConnect(self, server, port):
        try:
            self.client.connect((server, port))
            thread1 = threading.Thread(target=self.getData, args=(self.client,))
            thread1.start()
            return True
        except:
            return False

    def clientDisconnect(self):
        self.client.close()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
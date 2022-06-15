import socket
import threading
import time
import pickle
from xmlrpc import client

_port = 1234
_server = socket.gethostbyname(socket.gethostname())


class User:
    def __init__(self, clientName, port):
        self.clientName = clientName
        self.port = port
        self.messageBox = []

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

            thread1 = threading.Thread(target=self.getMessage, args=(client,))
            thread1.start()

    def getMessage(self, client):
        while True:
            try:
                msg = pickle.loads(client.recv(1024))
                self.messageBox.append(msg)
                if(len(self.messageBox) > 5):
                    self.messageBox.pop(0)
            except:
                client.close()
                break

    def sendMessage(self, msg):
        self.client.send(pickle.dumps(msg))
        time.sleep(0.1)

    def clientConnect(self, server, port):
        self.client.connect((server, port))
        thread1 = threading.Thread(target=self.getMessage, args=(self.client,))
        thread1.start()

    def clientDisconnect(self):
        self.client.close()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
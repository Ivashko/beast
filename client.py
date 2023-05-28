import SocketServer
import argparse
import ssl
import threading
import random
import string
import socket
import select
from Crypto.Cipher import AES
from Crypto import Random


class AESCipher:
    def __init__(self):
        self.iv = Random.new().read(AES.block_size)

    def set_vector_init(self, iv):
        self.iv = iv

    def pad(self, s):
        return s + (16 - len(s) % 16) * chr(16 - len(s) % 16)

    def encrypt(self, raw):
        raw = self.pad(raw)
        iv = self.iv
        cipher = AES.new('V38lKILOJmtpQMHt', AES.MODE_CBC, iv)
        return iv + cipher.encrypt(raw)


class ClientTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        socket_server = socket.create_connection(('localhost', 1111))
        inputs = [socket_server, self.request]
        running = True
        while running:
            readable = select.select(inputs, [], [])[0]
            for source in readable:
                if source is socket_server:
                    data = socket_server.recv(1024)
                    if len(data) == 0:
                        running = False
                        break
                    # server -> client
                    self.request.send(data)
                elif source is self.request:
                    data = self.request.recv(1024)
                    if len(data) == 0:
                        running = False
                        break
                    if 'set_vector_init' in data[:-1]:
                        cbc.set_vector_init(data[15:])
                    elif 'history' == data[:-1]:
                        self.request.send("get history: ")
                        data = cbc.encrypt("history"+ "_" + cookie)
                        socket_server.send(data)
                    elif data[:-1]:
                        # client -> server
                        self.request.send("get password: ")
                        data = cbc.encrypt(data + "_" + cookie)
                        socket_server.send(data)
        return


class Client:
    def connection(self):
        SocketServer.TCPServer.allow_reuse_address = True
        self.httpd = SocketServer.TCPServer(('localhost', 1112), ClientTCPHandler)
        print('Server is serving HTTPS on localhost port 1112')
        self.httpd.serve_forever()
        return


    def disconnect(self):
        print('\nServer stop serving HTTPS on localhost port 1112')
        self.httpd.shutdown()
        return

        

        

if __name__ == '__main__':
    cookie = ''.join(random.SystemRandom().choice(string.uppercase + string.digits + string.lowercase) for _ in xrange(15))
    cbc = AESCipher()
    try:
        client = Client()
        client.connection()
    except KeyboardInterrupt:
        client.disconnect()

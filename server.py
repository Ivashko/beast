import SocketServer
import argparse
import ssl
import threading
import random
import string
import json
from Crypto.Cipher import AES
from Crypto import Random


class AESCipher:
    def __init__(self):
        self.iv = Random.new().read(AES.block_size)

    def unpad(self, s):
        return s[:-ord(s[len(s)-1:])]

    def decrypt(self, enc):
        iv = enc[:16]
        cipher = AES.new('V38lKILOJmtpQMHt', AES.MODE_CBC, iv)
        return self.unpad(cipher.decrypt(enc[16:]))





class SecureTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        while True:
            try:
                data = self.request.recv(1024)
                if data == '':
                    break
                data = cbc.decrypt(data)[:-1].split("_")
                if len(data) != 2:
                    self.request.send("Error")
                    return
                if data[1].isalnum():
                    if 'history' == data[0]:
                        request_data = json.dumps(history.get(data[1], {}))
                    elif 'password' == data[0][:-1] or 'password' == data[0]:
                        request_data = ''.join(random.SystemRandom().choice(string.uppercase + string.digits + string.lowercase) for _ in xrange(10))
                        if not history.get(data[1]):
                            history[data[1]] = [request_data]
                        else:
                            history[data[1]].append(request_data)
                    else:
                        request_data = 'Error'
                    request_data = request_data + "\n"
                    self.request.send(request_data)
                else:
                    self.request.send("Unauthorized request")
            except ssl.SSLError:
                pass
        return


class Server:
    def connection(self):
        SocketServer.TCPServer.allow_reuse_address = True
        self.httpd = SocketServer.TCPServer(('localhost', 1111), SecureTCPHandler)
        print('Server is serving HTTPS on localhost port 1111')
        self.httpd.serve_forever()
        return

    def disconnect(self):
        print('\nServer stop serving HTTPS on localhost port 1111')
        self.httpd.shutdown()
        return
      

if __name__ == '__main__':
    history = {}
    cbc = AESCipher()
    try:
        server = Server()
        server.connection()
    except KeyboardInterrupt:
        server.disconnect()
        

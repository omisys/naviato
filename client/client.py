#!/usr/bin/env python3

### client.py ###
import socket
import os

CHUNK_SIZE = 1024

directory = "/home/derek/code/naviato"
filename  = "naviato.png"
#host     = socket.gethostname()
#host     = socket.gethostbyname("localhost")
#host     = '192.168.2.94'
host      = '127.0.0.1'
port      = 5037

def bitstring_to_bytes(s):
    return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')

# set up connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

# send filename size as 2 bytes
size = bin(len(filename))[2:].zfill(16)
s.send(bitstring_to_bytes(size))

# send filename
s.send(filename.encode('utf-8'))

filename = os.path.join(directory, filename)
filesize = os.path.getsize(filename)
print("Filesize:", filesize)

# send filesize as 4 bytes
size = bin(filesize)[2:].zfill(32)
s.send(bitstring_to_bytes(size))

'''
with open(filename, 'rb') as f:
    while filesize > 0:
        data_chunk = f.read(CHUNK_SIZE)
        s.send(data_chunk)
'''

s.shutdown(socket.SHUT_WR)

s.close()

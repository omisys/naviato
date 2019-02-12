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

def send_all(s, filename):
    with open(filename, 'rb') as f:
        data = f.read();
        s.sendall(data)

def send_chunk(s, filename, filesize):
    with open(filename, 'rb') as f:
        while filesize > CHUNK_SIZE:
            data = f.read(CHUNK_SIZE)
            s.send(data)
            filesize -= CHUNK_SIZE

        # send last bytes
        data = f.read(filesize)
        s.send(data)

try:
    # set up connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    # send filename size as 2 bytes
    size = len(filename).to_bytes(2, byteorder='big')
    s.send(size)

    # send filename
    s.send(filename.encode('utf-8'))

    filename = os.path.join(directory, filename)
    filesize = os.path.getsize(filename)
    print("Filesize:", filesize)

    # send filesize as 4 bytes
    size = filesize.to_bytes(4, byteorder='big')
    s.send(size)

    # start sending file
    if filesize < CHUNK_SIZE:
        send_all(s, filename)
    else:
        send_chunk(s, filename, filesize)

    print("Successfully send: " + filename)

except Exception as e:
    print("cannot connect to server:", e)

# cleanup, close socket
finally:
    s.shutdown(socket.SHUT_WR)
    s.close()
    print("Connection closed")

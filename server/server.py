#!/usr/bin/env python3

### server.py ###
import socket

# create socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# set port and hostname visible to outside world
print(socket.gethostname())
#host = socket.gethostname()
#host = socket.gethostbyname("localhost")
#host = '192.168.2.94'
host = '127.0.0.1'
port = 5037

# bind the socket to port and hostname
serversocket.bind((host, port))

# maximum connections to listen to
serversocket.listen(5)
print("waiting for connection...")

# main loop of server
while True:
    # accept connections from outside
    (clientsocket, address) = serversocket.accept()
    print("Got a connection from %s" % str(address))

    while True:
        # receive filename size as binary data (max 2 bytes)
        received = clientsocket.recv(2)
        size = int.from_bytes(received, byteorder='big')

        # receive filename
        filename = clientsocket.recv(size).decode('utf-8')
        if not filename:
            break
        print("Filename: " + filename)

        # receive filesize as 4 bytes
        received = clientsocket.recv(4)
        filesize = int.from_bytes(received, byteorder='big')
        if not filesize:
            break
        print("Filesize:", filesize)

'''
        f = open(filename, 'wb')
        if filesize > 0:
            data = conn.recv(1024)
            if not data:
                break
            # write bytes on file
            f.write(data)
'''

serversocket.close()



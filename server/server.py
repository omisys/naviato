#!/usr/bin/env python3

### server.py ###
import socket

CHUNK_SIZE = 1024

# create socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# set port and host - open to all connections
host = ''
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
    print("Got a connection from {0}".format(address))

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

        # start receiving file
        with open(filename, 'wb') as f:
            print("Start receiving " + filename)
            while filesize > CHUNK_SIZE:
                data = clientsocket.recv(CHUNK_SIZE)
                if not data:
                    break
                # write bytes in file
                f.write(data)
                print("Written {0} bytes, {1} bytes left".format(CHUNK_SIZE, filesize))
                filesize -= CHUNK_SIZE

            # receive remaining bytes
            data = clientsocket.recv(filesize)
            f.write(data)

            # done
            print("Successfully received: " + filename)


serversocket.close()



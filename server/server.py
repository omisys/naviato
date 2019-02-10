#!/usr/bin/env python3

### server.py ###
import socket

# create socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#serversocket = socket.socket()

# set port and hostname visible to outside world
#host = socket.gethostname()
print(socket.gethostname())
#host = socket.gethostbyname("localhost")
host = '192.168.2.94'
#host = '81.204.229.136'
port = 5037

# bind the socket to port and hostname
serversocket.bind((host, port))

# maximum connections to listen to
serversocket.listen(5)
print("waiting for connection...")

# main loop of server
#while True:
    # accept connections from outside
(clientsocket, address) = serversocket.accept()
print("Got a connection from %s" % str(address))

while True:
    # receive filename (max 256 bytes)
    buffer = bytearray(32)
    view = memoryview(buffer)

    received = clientsocket.recv_into(buffer)
    print(received)
    filename = view[:received].tobytes().decode('utf-8')
    #filename = clientsocket.recv(16).decode('utf-8') # Note that you limit your filename length to 255 bytes.
    if not filename:
        break
    print("Filename :" + filename)

    # receive filesize
    filesize = clientsocket.recv(1024).decode('utf-8')
    filesize = int(filesize)
    if not filesize:
        break
    print("Filesize :" + filesize)

    f = open(filename, 'wb')
    if filesize > 0:
        data = conn.recv(1024)
        if not data:
            break
        # write bytes on file
        f.write(data)


'''
    size = int(size, 2)
    filename = clientsocket.recv(size)

    # recieve the filesize as binary data
    filesize = clientsocket.recv(32)
    filesize = int(filesize, 2)

    # write the new file
    file_to_write = open(filename, 'wb')
    chunksize = 4096
    while filesize > 0:
        if filesize < chunksize:
            chunksize = filesize
        data = clientsocket.recv(chunksize)
        file_to_write.write(data)
        filesize -= len(data)

    file_to_write.close()
    print("File received successfully")
    '''

serversocket.close()



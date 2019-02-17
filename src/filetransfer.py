#!/usr/bin/env python3

### filetransfer.py ###
import socket
import os

CHUNK_SIZE = 1024

class Filetransfer:
    """
    Filetransfer class.
    contains all send and receive functions for sockets.
    """

    """ Init functions """

    def __init__(self):
        self.s = None
        self._filepath = None
        self._filename = None
        self._filesize = None

    def receive_init(self, clientsocket):
        self.s = clientsocket

    def send_init(self, host, port):
        # create a socket and try to connect
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((host, port))
            print("Connected to server")
        except ConnectionError as error:
            print("Unable to connect: {}".format(error))
            self.close_socket()
            raise Exception(error)


    """ Send functions """

    def send_filename(self, filename):
        print("Filename:", filename)
        # send filename size as 2 bytes
        size = len(filename).to_bytes(2, byteorder='big')
        self.s.send(size)

        # send filename
        self.s.send(filename.encode('utf-8'))

    def send_filesize(self, filepath):
        self._filepath = filepath
        self._filesize = os.path.getsize(filepath)
        print("Filesize:", self._filesize)

        # send filesize as 4 bytes
        size = self._filesize.to_bytes(4, byteorder='big')
        self.s.send(size)

    def send_chunk(self):
        filesize = self._filesize
        with open(self._filepath, 'rb') as f:
            while filesize > CHUNK_SIZE:
                data = f.read(CHUNK_SIZE)
                self.s.send(data)
                filesize -= CHUNK_SIZE

            # send last bytes
            data = f.read(filesize)
            self.s.send(data)

        print("Success, closing socket")
        self.s.shutdown(socket.SHUT_WR)


    """ Receive functions """

    def receive_filename(self):
        # receive filename size as binary data (max 2 bytes)
        received = self.s.recv(2)
        size = int.from_bytes(received, byteorder='big')

        # receive filename
        self._filename = self.s.recv(size).decode('utf-8')
        if not self._filename:
            self.s.shutdown(socket.SHUT_WR)
            raise Exception("Failed to receive filename")
        else:
            print("Filename: {}".format(self._filename))

    def receive_filesize(self):
        # receive filesize as 4 bytes
        received = self.s.recv(4)
        self._filesize = int.from_bytes(received, byteorder='big')
        if not self._filesize:
            self.s.shutdown(socket.SHUT_WR)
            raise Exception("Failed to receive filesize")
        else:
            print("Filesize:", self._filesize)

    def receive_chunk(self):
        filesize = self._filesize

        # start receiving file
        print("Start receiving " + self._filename)
        with open(self._filename, 'wb') as f:
            while filesize > CHUNK_SIZE:
                data = self.s.recv(CHUNK_SIZE)
                if not data:
                    self.s.shutdown(socket.SHUT_WR)
                    raise ConnectionAbortedError("Failed to receive chunk")

                # write bytes in file
                f.write(data)
                print("Written {0} bytes, {1} bytes left".format(CHUNK_SIZE, filesize))
                filesize -= CHUNK_SIZE

            # receive remaining bytes
            data = self.s.recv(filesize)
            if not data:
                self.s.shutdown(socket.SHUT_WR)
                raise ConnectionAbortedError("Failed to receive chunk")
            f.write(data)

            # done
            print("Successfully received: {}".format(self._filename))
            self.s.shutdown(socket.SHUT_WR)


    def close_socket(self):
        self.s.close()

#!/usr/bin/env python3

### client.py ###
import socket
import os

CHUNK_SIZE = 1024


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s = socket.socket()

print(socket.gethostname())
#host = socket.gethostname()
#host = socket.gethostbyname("localhost")
host = '192.168.2.94'
#host = '81.204.229.136'
port = 5037

s.connect((host, port))

directory = "/home/derek/code/"
#filename = input("Type shit: ")
filename = "stm32f411re.pdf"

'''
filenamesize = len(filename)
# encode filename size as 16 bit binary, pad left side with zeros
filenamesizebin = bin(filenamesize)[2:].zfill(16)
#print(filenamesizebin)
filenamesizebytes = bytes(filenamesizebin)
print(filenamesizebytes)

# send the file size, followed by the filename
s.send(filenamesizebin.encode('utf-8'))
'''
s.send(filename.encode('utf-8'))

filename = os.path.join(directory, filename)
filesize = os.path.getsize(filename)
print(filesize)
s.send(str(filesize).encode('utf-8'))

with open(filename, 'rb') as f:
    while filesize > 0:
        data_chunk = f.read(CHUNK_SIZE)
        s.send(data_chunk)


'''
# encode filesize as 32 bit binary
filesize = bin(filesize)[2:].zfill(32)
s.send(filesize)

file_to_send = open(filename, 'rb')
l = file_to_send.read()
s.sendall(l)
file_to_send.close()
print("file sent")
'''

s.shutdown(socket.SHUT_WR)

s.close()

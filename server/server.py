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

filename = ''
while True:
    data = clientsocket.recv(1024).decode('utf-8')
    if not data:
        break
    filename += data

print("From connection: " + filename)
myfile = open(filename, "rb")
clientsocket.send(myfile.read())

serversocket.close()



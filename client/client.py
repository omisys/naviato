# client.py
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s = socket.socket()

print(socket.gethostname())
#host = socket.gethostname()
#host = socket.gethostbyname("localhost")
host = '192.168.2.94'
#host = '81.204.229.136'
port = 5037

s.connect((host, port))

filename = input("Type shit: ")
s.send(filename.encode('utf-8'))
s.shutdown(socket.SHUT_WR)
data = s.recv(1024).decode('utf-8')
print(data)

s.close()

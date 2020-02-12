import socket

HOST = '127.0.0.1'
PORT = 8080

server = socket.socket()
print('Socket created')

server.bind((HOST, PORT))
print('Socket is binded')

server.listen(5)
print('Socket is listening')

conn, addr = server.accept()
print('Connected to {}'.format(addr))

while True:
    data = conn.recv(1024)
    print('data recieved: {}'.format(data))
    if not data:
        break

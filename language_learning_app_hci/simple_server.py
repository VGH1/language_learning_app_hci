# Python program to implement server side of chat room.
import socket
from _thread import start_new_thread
import threading

class SocketServer:
    def __init__(self, ip, host):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((ip, host))
        server.listen(5)
        self.server = server
        self.list_of_clients = []

    """ Thread for new client """
    def clientthread(self, conn, addr):
        # sends a message to the client whose user object is conn
        #conn.send("Welcome to this chatroom!".encode())
        while True:
            try:
                message = conn.recv(2048)
                if message:
                    print("<" + addr[0] + "> " + message)

                    # Calls broadcast function to send message to all
                    message_to_send = "<" + addr[0] + "> " + message
                    self.broadcast(message_to_send, conn)
                else:
                    self.remove(conn)

            except Exception:
                continue


    """ Broadcast a message to all connected clients"""
    def broadcast(self, message):
        #print("ALL connections: %s" % self.list_of_clients)
        print("Number of connections: %s" % len(self.list_of_clients))
        for clients in self.list_of_clients:
            try:
                print("Sending %s to: %s" % (message, clients))
                clients.send(message.encode())
            except Exception:
                clients.close()
                self.remove(clients)

    """ Remove a sockets connection """
    def remove(self, connection):
        if connection in self.list_of_clients:
            self.list_of_clients.remove(connection)

    """ Accept new socketes connections """
    def accept_connections(self):
        while True:
            conn, addr = self.server.accept()

            self.list_of_clients.append(conn)

            # prints the address of the user that just connected
            print(addr[0] + " connected")

            # creates and individual thread for every user that connects
            threading.Thread(target=self.clientthread, args=((conn, addr)))

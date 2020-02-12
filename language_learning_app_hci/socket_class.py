import socket

class SocketClass():
    def __init__(self, host, port):
        self.listening = True
        self.host = host
        self.port = port
        self.allDataReceived = []
        self.my_scoket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    """
    A function that opens a socket with Matlab PC
    """
    def open_socket(self):
        try:
            connected = self.my_socket.connect((self.host, self.port))
        except Exception as e:
            print("Error creating socket, %s" % str(e))
            return False

    """
    function that sends data throught the socket to Matlab PC
    """
    def send_data(self, data):
        try:
            self.my_socket.sendall(data.encode('utf-8')) # send marker data to Matlab PC
        except Exception as e:
            print(e)

    """
    Get method that returns allDataRecieved list
    """
    def get_all_data_received (self):
        return self.allDataReceived

    """
    A function that closes the socket
    """
    def close_socket(self):
        try:
            self.listening = False
            self.my_socket.close()
        except Exception as e:
            print(e)

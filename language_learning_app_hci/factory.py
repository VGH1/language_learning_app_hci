from flask import Flask
from flask_socketio import SocketIO
from SocketClass import Socket_Class

'''Config & set up Flask app'''
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

websocket = SocketIO(app)

'''Socket IP connection'''
# Matlab ip
# HOST = '192.168.2.201'
# PORT = 30000

# selfServer ip
HOST = '127.0.0.1'
PORT = 60000
socket = Socket_Class(HOST, PORT)

import socket
import config
from function.requestHandler import *

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

sendRequest(client, 'example.com')

client.close()
print('Socket disconnected')
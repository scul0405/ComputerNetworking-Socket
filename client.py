import socket
import config
from function.requestHandler import *
from function.responseHandler import *
from function.utilities import *

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

sendRequest(client, config.LINKS[0])
data = getResponse(client)

client.close()
print('Socket disconnected')
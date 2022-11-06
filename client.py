import socket
import config

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')


client.close()
print('Socket disconnected')
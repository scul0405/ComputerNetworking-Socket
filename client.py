import socket
import config
from function.method import *
from function.requestHandler import getHostAndRoute
from threading import Thread

def createAConnection(LINK):
    HOST, _ = getHostAndRoute(LINK)
    socket.getaddrinfo(HOST,config.PORT)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')

    makeRequest(client, LINK)

    client.close()
    print('Socket disconnected')

# Multiple connection in parallel
for LINK in config.LINKS:
    #print(LINK)
    thread = Thread(target=createAConnection, args=(LINK,))
    thread.start()
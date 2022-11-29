import socket
import config
from function.method import *
from function.requestHandler import getHostAndRoute
from threading import Thread
from datetime import datetime

def createAConnection(LINK, index):
    HOST, _ = getHostAndRoute(LINK)
    socket.getaddrinfo(HOST,config.PORT)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    now = datetime.now().time()
    print(f'Socket {index} created at: {now}')

    client.settimeout(config.TIMEOUT_DEFAULT)
    try:
        makeRequest(client, LINK)
    except Exception:
        print("Loss connection! Download Failed...")

    client.close()
    now = datetime.now().time()
    print(f'Socket {index} disconnected at: {now}')

# Multiple connection in parallel
for index, LINK in enumerate(config.LINKS):
    thread = Thread(target=createAConnection, args=(LINK, index + 1, ))
    thread.start()
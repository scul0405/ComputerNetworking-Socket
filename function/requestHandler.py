import config

def getHostAndRoute(LINK):
    indexOfSplit = LINK.find('/')
    if indexOfSplit == -1:
        ROUTE = '/'
        HOST = LINK
    else:
        HOST = LINK[:indexOfSplit]
        ROUTE = LINK[indexOfSplit:]


    return HOST, ROUTE

def makeHeader(LINK):
    HOST, ROUTE = getHostAndRoute(LINK)
    HEADER = ("GET " + ROUTE + " HTTP/1.1\r\nHost: " + HOST + "\r\n\r\n").encode('utf-8')

    return HEADER

def sendRequest(client, LINK):
    HEADER = makeHeader(LINK)
    client.send(HEADER)
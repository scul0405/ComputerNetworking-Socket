import config
from function.requestHandler import *
from function.responseHandler import *
from function.utilities import *
from function.makefile import *
def getResponseByRequest(client, LINK):
    #Send request
    sendRequest(client,LINK)

    #Get data
    data = getResponse(client)

    #Make File
    print("data len: ",len(data))
    #mf = MakeFile(LINK,data)
    #mf.createFile()
    

def makeRequest(client, LINK):
    #Connect to HOST
    HOST, ROUTE = getHostAndRoute(LINK)
    client.connect((HOST,config.PORT))
    print(f'Connect to {HOST} : {config.PORT}')

    #Check ROUTE is a file or folder
    print(HOST, ROUTE)
    if isFile(ROUTE) == True:
        getResponseByRequest(client,LINK)
    else:
        sendRequest(client, LINK)
        htmlData = getResponse(client)
        files = getFolderFiles(htmlData)
        for file in files:
            fileLink = LINK + file
            getResponseByRequest(client, fileLink)



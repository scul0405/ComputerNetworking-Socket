import config
from function.requestHandler import *
from function.responseHandler import *
from function.utilities import *
from function.makefile import *

def getResponseByRequest(client, LINK):
    #Send request
    sendRequest(client,LINK)
    #Get data
    data, isChunk = getResponse(client)
    # Loss connection
    if len(data) == 0:
        raise
    #Make File
    mf = MakeFile(LINK,"",data)
    mf.createFile(isChunk)

def makeRequest(client, LINK):
    #Connect to HOST
    HOST, ROUTE = getHostAndRoute(LINK)
    client.connect((HOST,config.PORT))
    folderName = ""
    #Check ROUTE is a file or folder
    if isFile(ROUTE) == True:
        getResponseByRequest(client,LINK)
    else:
        if ROUTE[len(ROUTE)-1] == "/":
            temp = ROUTE[:-1]
        else:
            temp = ROUTE
        folderName = temp[temp.rfind("/")+1:]
        sendRequest(client, LINK)
        htmlData, ischunk = getResponse(client)
        # Loss connection
        if len(htmlData) == 0:
            raise
        files = getFolderFiles(htmlData)

        # export .html of folder
        mf = MakeFile(LINK + "/" + "index.html",folderName,htmlData)
        mf.createFile(ischunk)
        
        # download file from folder if exist
        for file in files:
            fileLink = LINK + file
            getResponseByRequest(client, fileLink)

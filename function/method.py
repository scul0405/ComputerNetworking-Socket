import config
from function.requestHandler import *
from function.responseHandler import *
from function.utilities import *
from function.makefile import *

def getResponseByRequest(client, LINK):
    #Send request
    sendRequest(client,LINK)
    #Get data
    data, ischunk = getResponse(client)
    if ischunk:
        print("La file chunk")
    #Make File
    print("data len: ",len(data))
    mf = MakeFile(LINK,"",data)
    mf.createFile(ischunk)
    

def makeRequest(client, LINK):
    #Connect to HOST
    HOST, ROUTE = getHostAndRoute(LINK)
    client.connect((HOST,config.PORT))
    print(f'Connect to {HOST} : {config.PORT}')
    folderName = ""
    #Check ROUTE is a file or folder
    print(HOST, ROUTE)
    if isFile(ROUTE) == True:
        getResponseByRequest(client,LINK)
    else:
        print("///La folder///")
        if ROUTE[len(ROUTE)-1] == "/":
            temp = ROUTE[:-1]
        else:
            temp = ROUTE
        folderName = temp[temp.rfind("/")+1:]
        print("new route:",folderName)
        sendRequest(client, LINK)
        htmlData, ischunk = getResponse(client)
        files = getFolderFiles(htmlData)

        # export .html of folder
        mf = MakeFile(LINK + "/" + "index.html",folderName,htmlData)
        mf.createFile(ischunk)
        
        # download file from folder if exist
        for file in files:
            fileLink = LINK + file
            getResponseByRequest(client, fileLink)



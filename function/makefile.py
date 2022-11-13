import os
import os.path
from function.requestHandler import*
from function.utilities import*
from function.responseHandler import*


class MakeFile:
    def __init__(self, LINK, content):
        self.HOST, self.ROUTE = getHostAndRoute(LINK)
        self.fileName = self.HOST[:self.HOST.find(".")] #Lay ten de tao folder root
        dir = os.getcwd() + "\\downloads\\" #chi dinh dia chi luu file
        path = os.path.join(dir, self.fileName)        
        if (not(os.path.exists(path))): #Kiem tra folder ten fileName co ton tai trong download chua, neu chua thi tao folder root
            os.mkdir(path)
        os.chdir(dir+self.fileName) #thay doi dia chi workspace
        self.content = content
    def createFile(self):
        print("test")
        if isFile(self.ROUTE): #truong hop link chi co 1 file index
            #print(os.getcwd())
            
            print(self.content[:self.content.find(b"\r\n\r\n")])
            print(getContentType(self.content[:self.content.find(b"\r\n\r\n")]))
            if (getContentType(self.content[:self.content.find(b"\r\n\r\n")])=="text/html"):
                fout = open("index.html","w")
                #print("contet len: ",len(self.content))
                fout.write(self.content.decode("utf-8"))
                fout.close()
                os.startfile("index.html")
            else:
                print("testelse")
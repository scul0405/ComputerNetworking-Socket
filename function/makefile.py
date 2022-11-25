import os
import os.path
from function.requestHandler import*
from function.utilities import*
from function.responseHandler import*


class MakeFile:
    def __init__(self, LINK, content):
        self.LINK=LINK
        self.HOST, self.ROUTE = getHostAndRoute(LINK)
        self.folderName = self.HOST[:self.HOST.rfind(".")] #Lay ten de tao folder root
        print(self.folderName)
        # if isFile(self.ROUTE[:self.ROUTE.rfind("/")]) == False:
        #     print("testFolder")
        #     last_index = self.LINK.rfind("/")
        #     temp_LINK = self.LINK[1:last_index]
        #     self.folderName = temp_LINK[temp_LINK.rfind("/"):]
        print("folder name: ",self.folderName)
        if os.getcwd().find("downloads\\") == -1: #neu dia chi current working directory chua co downloads thi thay doi dia chi de luu file download
            if not(os.path.exists(os.getcwd()+"\\downloads\\")):
                os.mkdir(os.getcwd()+"\\downloads\\")
            os.chdir(os.getcwd()+"\\downloads\\")
            dir = os.getcwd() #chi dinh dia chi luu file
            path = os.path.join(dir, self.folderName) #nối download/foldername   
            if (not(os.path.exists(path))): #Kiem tra folder ten fileName co ton tai trong download chua, neu chua thi tao folder root
                os.mkdir(path)
            os.chdir(path) #thay doi dia chi workspace
        self.content = content
        print('test')
        print(LINK)
        self.content_type=LINK[LINK.rfind(".")+1:]
        print(self.content_type)
        
    def createFile(self,ischunk):
        if ischunk == False: #truong hop khong phai la file chunk
            if self.content_type == 'com/' or self.content_type == 'com': #truong hop la file html
                fout = open("index.html","w")
                fout.write(self.content.decode("utf-8"))
                fout.close()
                os.startfile("index.html")
            else: #truong hop la loai file khac
                fileName = self.LINK[self.LINK.rfind("/")+1:self.LINK.rfind(".")]
                fout = open(fileName+"."+self.content_type,"wb")
                fout.write(self.content)
                fout.close()
                os.startfile(fileName+"."+self.content_type)
        else: #truong hop link la chunk
            if self.content_type == 'com/' or self.content_type == 'com' or self.content_type =='': #truong hop la file html
                fout = open("index.html","wb")
                fout.write(self.content)
                fout.close()
                os.startfile("index.html")
            else:
                fileName = self.LINK[self.LINK.rfind("/")+1:self.LINK.rfind(".")]
                fout = open(fileName+"."+self.content_type,"wb")
                fout.write(self.content)
                fout.close()
                os.startfile(fileName+"."+self.content_type)


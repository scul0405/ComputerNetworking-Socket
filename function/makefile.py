import os
import os.path
from function.requestHandler import*
from function.utilities import*
from function.responseHandler import*


class MakeFile:
    def __init__(self, LINK, folderName,content): #tham so folderName neu la file thi rong, la folder thi la ten
        self.LINK=LINK
        self.HOST, self.ROUTE = getHostAndRoute(LINK)
        dir_cur = os.getcwd()
        dir_cur = dir_cur[dir_cur.rfind("\\")+1:]
        if self.ROUTE.find(dir_cur) == -1: #folder leaf cua work space hien tai khong co trong route, tuc la day la mot file le voi file truoc do nen ta tao folder de luu file
            if folderName == "": #truong hop la file chua co ten folder de luu thi lay ten trong HOST
                self.folderName = self.HOST[:self.HOST.rfind(".")] #Lay ten de tao folder root
            else: #truong hop co folderName thi chi can gan
                self.folderName = folderName
            if os.getcwd().find("downloads\\") == -1: #neu dia chi current working directory chua co downloads thi thay doi dia chi de luu file download
                if not(os.path.exists(os.getcwd()+"\\downloads\\")):
                    os.mkdir(os.getcwd()+"\\downloads\\")
                os.chdir(os.getcwd()+"\\downloads\\")
                dir = os.getcwd() #chi dinh dia chi luu file
                path = os.path.join(dir, self.folderName) #nối download/foldername   
                if (not(os.path.exists(path))): #Kiem tra folder ten fileName co ton tai trong download chua, neu chua thi tao folder root
                    os.mkdir(path)
                os.chdir(path) #thay doi dia chi workspace
            if (os.getcwd().find(self.folderName) == -1): #neu dia chi hien tai khong co folderName (tuc day la dia chi luu file cua link truoc do) nen ta rut dir ve truoc downloads vao dan lai folder moi
                os.chdir(os.getcwd()[:os.getcwd().find("downloads")-1])
                if not(os.path.exists(os.getcwd()+"\\downloads\\")):
                    os.mkdir(os.getcwd()+"\\downloads\\")
                os.chdir(os.getcwd()+"\\downloads\\")
                dir = os.getcwd() #chi dinh dia chi luu file
                path = os.path.join(dir, self.folderName) #nối download/foldername   
                if (not(os.path.exists(path))): #Kiem tra folder ten fileName co ton tai trong download chua, neu chua thi tao folder root
                    os.mkdir(path)
                os.chdir(path) #thay doi dia chi workspace
        self.content = content
        self.content_type = LINK[LINK.rfind(".")+1:].rsplit('/')[0]
        # in case file extension is domain extension of the HOST
        if self.HOST.rsplit(".", 1)[1]  == self.content_type:
            self.content_type = ".domainEx"
        
    def createFile(self,ischunk):
        if ischunk == False: #truong hop khong phai la file chunk
            if self.content_type == '.domainEx': #truong hop la file html
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
            if self.content_type == '.domainEx' or self.content_type =='': #truong hop la file html
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


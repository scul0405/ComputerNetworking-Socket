import os
class MakeFile:
    def __init__(self,name,content):
        self.fileName = "ComputerNetworking-Socket"+""
    def createFile(self):
        fout = open(self.fileName,"w")
        fout.write(self.content)
        fout.close()
        os.startfile(self.fileName)
        return 
import subprocess
class MakeFile():
    def __init__(self, content):
        self.fileName = ""
    def createFile(URL, binary_data):
        
        URL = "http://web.stanford.edu/class/cs224w/slides/01-intro.pdf"

        PATH = URL.split("/", 1)[1]
        PATH = PATH.rsplit("/", 1)[0] + "/"
        FILE_NAME =  URL.rsplit("/", 1)
        
        FILE = open(PATH + FILE_NAME, 'wb')
        FILE.write(binary_data)
        FILE.close()

        subprocess.call(FILE_NAME, shell=True)
        return 
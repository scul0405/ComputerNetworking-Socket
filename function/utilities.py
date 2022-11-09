import re

#Ham de xu ly xem route dua vao la folder hay file
def isFile(ROUTE):
    # '/' cho index.html va chua '.' nghia la file co duoi mo rong -> la file
    if ROUTE !=  '/' or ROUTE.find('.') != -1:
        return True
    return False


#Ham boc tach cac link de thuc hien multiple connect
def getFolderFiles(str):
    findStr = b'<td><a href="'
    fileIndexes = [m.start() for m in re.finditer(findStr,str)]
    files = []
    for i in fileIndexes:
        startIndex = i + len(findStr)
        endIndex = str.find(b'"',startIndex)
        files.append(str[startIndex:endIndex])
    return files[1:]
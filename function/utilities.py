import re

#Ham de xu ly xem route dua vao la folder hay file
def isFile(ROUTE):
    # '/' cho index.html va chua '.' nghia la file co duoi mo rong -> la file
    if ROUTE !=  '/' and ROUTE.find('.') == -1:
        return False
    return True


#Ham boc tach cac link de thuc hien multiple connect
def getFolderFiles(str):
    findStr = b'<td><a href="'
    fileIndexes = [m.start() for m in re.finditer(findStr,str)]
    files = []
    for i in fileIndexes:
        startIndex = i + len(findStr)
        endIndex = str.find(b'"',startIndex)
        files.append((str[startIndex:endIndex]).decode())
    return files[1:]
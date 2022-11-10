import config


def getLengthOfContent(resHeader):
    indexStart = resHeader.find(b"Content-Length") + len(b"Content-Length: ")
    indexEnd = resHeader.find(b"\r\n",indexStart)
    if indexEnd == -1:
        indexEnd = len(resHeader)
    return int(resHeader[indexStart:indexEnd])

def getContentType(resHeader):
    indexStart = resHeader.find(b"Content-Type") + len(b"Content-Type: ")
    indexEnd = resHeader.find(b";",indexStart)
    if indexEnd == -1:
        indexEnd = len(resHeader)
    return resHeader[indexStart:indexEnd].decode()

def getContent(client, resHeader, total):
    data = b""
    # xu ly buffer size cho nay
    # Voi content-type: text/html -> file be -> buff chi can 1KB moi lan la du
    # Voi content-type loai khac -> file to -> tang buff size len
    contentType = getContentType(resHeader)
    contentLength = getLengthOfContent(resHeader)

    print(contentType, contentLength, total)

    match contentType:
        case "text/html":
            buff = config.BUFFER_SIZE
            while total < contentLength:
                res = client.recv(buff)
                data += res
                total += len(res)
        case _: #default
            buff = 50*config.BUFFER_SIZE
            while total < contentLength:
                res = client.recv(buff)
                data += res
                total += len(res)
    return data

def getResponse(client):
    splitStr = b"\r\n\r\n"
    data = b""
    while data.find(splitStr) == -1:
        data += client.recv(config.BUFFER_SIZE)
    
    indexStartContent = data.find(splitStr)
    resHeader = data[:indexStartContent]

    #Lay data con lai sau khi loai bo header, sau do noi them tu getContent
    data = data[indexStartContent + 4:]
    total = len(data)
    data += getContent(client,resHeader,total)

    return data

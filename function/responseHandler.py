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
    print(contentLength, contentType)

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

def getContent_chunked(client):
    data = b""
    rec = b""
    while True:
        chunk_data = b""
        # get data for the first time
        if not rec:
            rec = client.recv(config.BUFFER_SIZE)
        # Split chunk-length && chunk-data
        splitChunk = rec.split(b"\r\n", 1)
        chunk_leng16 = splitChunk[0]                    # chunk-length in hex
        chunk_leng10 = int(chunk_leng16.decode(), 16)   # conver to decimal for calculate
        chunk_data = splitChunk[1]
        
        # End of download
        if chunk_leng10 == 0:
            break
        # If it not have enough chunk-data -> get more
        while len(chunk_data) < chunk_leng10:
            chunk_data += client.recv(config.BUFFER_SIZE)
     
        # Add chunk-data to data
        data += chunk_data[:chunk_leng10]
        # Give data remaining in chunk-data for the next chunk (loop)
        rec = chunk_data[chunk_leng10 + 2:]

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

def getResponse_chunked(client):
    data = b""
    startStr = b"\r\n\r\n" 
    # Get Header
    data += client.recv(4)
    while data[:len(data)][len(data)-4:] != startStr:
        data += client.recv(1)
    
    # Lay data con lai sau khi loai bo header
    HEADER = data.rsplit(b"\r\n\r\n")[0]
    if (HEADER.find('Transfer-Encoding: chunked') != -1):
        return getResponse(client)
    
    # Noi them tu getContent_chunked
    data += getContent_chunked(client)
    
    return data
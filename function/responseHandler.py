import config
import timeit

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

def getContent(client, resHeader, content):
    data = content
    total = len(content)
    contentLength = getLengthOfContent(resHeader)

    start = timeit.default_timer()
    while total < contentLength:
        try:
            buff = contentLength - total
            time = timeit.default_timer() - start
            client.settimeout(config.TIMEOUT_DEFAULT + 2*time)
            res = client.recv(buff)
            data += res
            total += len(res)
        except Exception:
            print("Waiting connection...")
            return ""
    
    return data

def getContent_chunked(client,resHeader,content):
    contentType = getContentType(resHeader)
    buff_size = config.BUFFER_SIZE
    if (contentType != b"text/html"):
        buff_size = 50*config.BUFFER_SIZE
    
    data = b""
    rec = content
    while True:
        chunk_data = b""
        # get data for the first time      
        try:
            if not rec:
                rec = client.recv(buff_size)
        except Exception:
            print("Waiting connection...")
            return ""
        # Split chunk-length && chunk-data
        splitChunk = rec.split(b"\r\n", 1)
        chunk_leng16 = splitChunk[0]                    # chunk-length in hex
        chunk_leng10 = int(chunk_leng16.decode(), 16)   # conver to decimal for calculate
        chunk_data = splitChunk[1]
        
        # End of download
        if chunk_leng10 == 0:
            break
        # If it not have enough chunk-data -> get more
        start = timeit.default_timer()
        while len(chunk_data) < chunk_leng10:          
            try:
                time = timeit.default_timer() - start
                client.settimeout(config.TIMEOUT_DEFAULT + 2*time)
                chunk_data += client.recv(buff_size)
            except Exception:
                print("Waiting connection...")
                return ""

        # Add chunk-data to data
        data += chunk_data[:chunk_leng10]
        # Give data remaining in chunk-data for the next chunk (loop)
        rec = chunk_data[chunk_leng10 + 2:]

    return data

def getHeader(client):
    splitStr = b"\r\n\r\n"
    data = b""
    while data.find(splitStr) == -1:    
        try:
            data += client.recv(config.BUFFER_SIZE)
        except Exception:
            print("Loss connection")
            return ""
    
    indexStartContent = data.find(splitStr)
    #Lay Header
    resHeader = data[:indexStartContent]
    #Lay data con lai sau khi loai bo header
    data = data[indexStartContent + 4:]
    
    return resHeader, data

def getResponse(client):
    resHeader, data = getHeader(client)
    if len(resHeader) == 0:
        return "", ""
    #Kiem tra Header co can su dung chunked hay khong
    if (resHeader.find(b"Transfer-Encoding: chunked") == -1):
        # Xu li content length
        data = getContent(client,resHeader,data)
        checkChunked = False
    else:
        # Xu li chunked
        data = getContent_chunked(client,resHeader,data)
        checkChunked = True
        
    return data, checkChunked
# Implements a simple HTTP client
import socket
import os
import datetime
import time
#connect to the server and read user input
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 80
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))
request = input('Input HTTP request command:\n')
#try to analyse the input
try:
    headers = request.split('\n')
    fields = headers[0].split()
    filename = fields[1]
    needopen=1
    #try to get the modify time of the requested file
    try:
        if filename!='/':
            modTimesinceEpoc = os.path.getmtime('receive' + filename)
            modificationTime = time.strftime('If-Modified-Since: %a, %d %b %Y %H:%M:%S GMT\r', time.localtime(modTimesinceEpoc))
            request=request+'\n'+modificationTime
    #skip if none
    except:
        pass
    #send the request after adding the If-Modified-Since header (or none)
    client_socket.send(request.encode())
    isimage=0
    if filename.rpartition(".")[2]=='jpg' or filename.rpartition(".")[2]=='png':
        response=client_socket.recv(512)
        isimage=1
    #decode only when the file is not an image
    else:
        response=client_socket.recv(512).decode()
    #when the request is GET
    if fields[0]=='GET':
        #if the response is not 304
        test304='HTTP/1.1 304 Not Modified\n\n'
        if response!=test304.encode():
            print('HI')
            #when the requested file is an image
            if isimage==1:
                headers = response.split('\n'.encode())
                fields = headers[2].split()
                length = int(fields[1].decode())
                header=(response[:length]).decode()
                data1=response[length:]
                data2=client_socket.recv(512)
                while True:
                    imgData = client_socket.recv(512)
                    data2=data2+imgData
                    if not imgData:
                        break
                    """
                    if needopen==1:
                        imgFile = open('receive/'+filename+'.jpg', 'wb')
                        needopen=0
                    """
                imgFile = open('receive/'+filename, 'wb')
                imgFile.write(data1+data2)
                imgFile.close()
            #when the requested file is a text file
            else:
                header= response
        #when the response is 304
        else:
            #decode the response only when the file is image
            if isimage==1:
                print()
                header= response.decode()
            else:  
                header= response
    #when the request is HEAD
    else:
        #decode the response only when the file is image
        if isimage==1:
            print()
            header= response.decode()
        else:
            header= response
    print ('Server response:\n')
    print (header)
    client_socket.close()
#when error in request
except:
    client_socket.send(request.encode())
    response=client_socket.recv(512).decode()
    print(response)
    client_socket.close()
    

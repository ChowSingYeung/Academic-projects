import socket
import threading
import os
import time
import datetime


# Handle the HTTP request.
def handle_client(client_connection, client_address):
    #try to receive and analyse the request
    try:
        print(f"[NEW CONNECTION] {client_address} connected.")
        error=0
        request= client_connection.recv(1024).decode()
        # Parse HTTP headers
        headers = request.split('\n')
        fields = headers[0].split()
        request_type = fields[0]
        filename = fields[1]
        # See if there is a if modified-since header
        matching = [s for s in headers if 'If-Modified-Since:' in s]
        compare=0
        if matching!=[]:
            compare=1
            date_time_obj1 = datetime.datetime.strptime(matching[0], 'If-Modified-Since: %a, %d %b %Y %H:%M:%S %Z\r')
    except:
        error=1
    #print the request
    print(f"[NEW CONNECTION] {client_address} request.")
    print(request)
    #when request is a GET and no error
    if request_type == 'GET' and error==0:
        if filename == '/':
            filename = '/index.html'
           
        try:
            isimage=filename.rpartition(".")[2]
            modTimesinceEpoc = os.path.getmtime('Data' + filename)
            modificationTime = time.strftime('Last-Modified: %a, %d %b %Y %H:%M:%S GMT\n', time.localtime(modTimesinceEpoc))
            #when an if modificed-since header appears
            if compare==1:
                date_time_obj2 =datetime.datetime.strptime(modificationTime, 'Last-Modified: %a, %d %b %Y %H:%M:%S %Z\n')
                #compare the time of the requested file in the local and from the client, send 304 if localtime<=clienttime
                if (date_time_obj2<=date_time_obj1):
                    response = 'HTTP/1.1 304 Not Modified'+'\n\n'
                    client_connection.sendall(response.encode())
                #the file has been modified or it is the first time getting
                else:
                    #when request file is an image
                    if (isimage=='jpg' or isimage=='png'):
                        imgFile = open('Data' + filename, "rb")
                        response = 'HTTP/1.1 200 OK\n'+modificationTime
                        header='header_length: '+'\n\n'
                        headerlength=len(header.encode('utf-8'))+len(response.encode('utf-8'))
                        finalheaderlength='header_length: '+str(headerlength+len(str(headerlength).encode('utf-8')))+'\n\n'
                        print(finalheaderlength)
                        response=response+finalheaderlength
                        x=imgFile.readline(512)
                        while True:
                            imgData = imgFile.readline(512)
                            x=x+imgData
                            if not imgData:
                                break
                        client_connection.sendall(response.encode()+x)
                        imgFile.close()
                    #when the request file is text
                    else:
                        fin = open('Data' + filename)
                        content = fin.read()
                        fin.close()
                        response = 'HTTP/1.1 200 OK\n'+modificationTime+'\n'+ content
                        client_connection.sendall(response.encode())
            #no if modified since header
            else:
                #when request file is an image
                if (isimage=='jpg' or isimage=='png'):
                    imgFile = open('Data' + filename, "rb")
                    response = 'HTTP/1.1 200 OK\n'+modificationTime
                    header='header_length: '+'\n\n'
                    headerlength=len(header.encode('utf-8'))+len(response.encode('utf-8'))
                    finalheaderlength='header_length: '+str(headerlength+len(str(headerlength).encode('utf-8')))+'\n\n'
                    response=response+finalheaderlength
                    x=imgFile.readline(512)
                    while True:
                        imgData = imgFile.readline(512)
                        x=x+imgData
                        if not imgData:
                            break
                    client_connection.sendall(response.encode()+x)
                    imgFile.close()
                #when the request file is text
                else:
                    fin = open('Data' + filename)
                    content = fin.read()
                    fin.close()
                    response = 'HTTP/1.1 200 OK\n'+modificationTime+'\n'+ content
                    client_connection.sendall(response.encode())
        #404 when cannot find the request file
        except FileNotFoundError:
            response = 'HTTP/1.1 404 Not Found\n\nFile Not Found'
            client_connection.sendall(response.encode())
        
    #when request type is HEAD with no errors, the following code is same as GET but without the file data transmittion
    elif request_type== 'HEAD' and error==0:
        if filename == '/':
            filename = '/index.html'
           
        try:
            isimage=filename.rpartition(".")[2]
            modTimesinceEpoc = os.path.getmtime('Data' + filename)
            modificationTime = time.strftime('Last-Modified: %a, %d %b %Y %H:%M:%S GMT\n', time.localtime(modTimesinceEpoc))
            if compare==1:
                date_time_obj2 =datetime.datetime.strptime(modificationTime, 'Last-Modified: %a, %d %b %Y %H:%M:%S %Z\n')
                if (date_time_obj2>date_time_obj1):
                    if (isimage=='jpg' or isimage=='png'):
                        response = 'HTTP/1.1 200 OK\n'+modificationTime
                        header='header_length: '+'\n\n'
                        headerlength=len(header.encode('utf-8'))+len(response.encode('utf-8'))
                        finalheaderlength='header_length: '+str(headerlength+len(str(headerlength).encode('utf-8')))+'\n\n'
                        response=response+finalheaderlength
                        client_connection.sendall(response.encode())
                    else:
                        response = 'HTTP/1.1 200 OK\n'+modificationTime+'\n'
                        client_connection.sendall(response.encode())
                else:
                    response = 'HTTP/1.1 304 Not Modified\n\n'
                    client_connection.sendall(response.encode())
            else:
                if (isimage=='jpg' or isimage=='png'):
                    response = 'HTTP/1.1 200 OK\n'+modificationTime
                    header='header_length: '+'\n\n'
                    headerlength=len(header.encode('utf-8'))+len(response.encode('utf-8'))
                    finalheaderlength='header_length: '+str(headerlength+len(str(headerlength).encode('utf-8')))+'\n\n'
                    response=response+finalheaderlength
                    client_connection.sendall(response.encode())
                else:
                    response = 'HTTP/1.1 200 OK\n'+modificationTime+'\n'
                    client_connection.sendall(response.encode())
        except FileNotFoundError:
            response = 'HTTP/1.1 404 Not Found\n\nFile Not Found'
            client_connection.sendall(response.encode())
    #when there is an error from the request
    else:
        response = 'HTTP/1.1 400 Bad Request\n\nRequest Not Supported'
        filename=''
        client_connection.sendall(response.encode())
    #print the response and write the logs 
    print(f"[NEW CONNECTION] {client_address} response.")
    print(response)
    client_connection.close()
    accesstime=datetime.datetime.now()
    responsebyline = response.split('\n')
    responsetype = responsebyline[0]
    f = open("log.txt", "a")
    f.write('client hostname/IP address: '+str(client_address)+' access time: '+str(accesstime)+' requested file name: '+filename+' response type: '+responsetype)   
    f.write('\n')
    f.close()

Serverhost= '127.0.0.1'
Serverport= 80

# Create socket
Serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
Serversocket.bind((Serverhost, Serverport))
print('Listening on port %s ...' % Serverport)
while True:
    Serversocket.listen(1)
# Wait for client connections
    client_connection, client_address = Serversocket.accept()
    #start thread
    thread = threading.Thread(target=handle_client, args=(client_connection, client_address))
    thread.start()
    print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")



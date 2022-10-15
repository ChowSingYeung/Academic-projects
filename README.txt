This file aims to help you run the client.py and server.py program

Open console and go to the directory of the COMP2322_Project file, for example, cd c:\Users\Asus\Desktop\COMP2322_project

Server.py:

To run Server.py, type Server.py
You should see "Listening on port 80 ..."
That means your server is ready
You can see connection informations from clients and their request and server response
An active connection count is also avaliable

The log.txt file is for logging the information for client connection
The Data folder is for storing the server data, you can modify information in there.
If there is no response from the server, try closing it and executing server.py again and request again

Clinet.py:

To run Client.py, type Client.py (make sure Server.py is operating)
You should see "Input HTTP request command:"
Type your request using the format and press enter
"request type" "/filename" "HTTP:/1.1"(optional), for example, GET /Apple.jpg HTTP:/1.1, make sure there is an space between
The server should receive your request and send the response back

The receive folder is for data receiving for client program which only image files is stored, DO NOT modify them or the IF-MODIFIED SINCE field will be changed

When connecting first time to the server with Client.py or browser, make sure the receive folder and log.txt is empty 

Browsers:

With browsers, clear your cache first
There might be multiple connections to the server.py with one refresh or access, ignore the errors it brings and the connection message from the server of them










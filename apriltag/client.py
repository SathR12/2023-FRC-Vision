import socket

client = socket.socket() #create client socket
client.connect(("127.0.0.1", 9570))
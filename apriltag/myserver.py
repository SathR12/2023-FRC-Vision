from socket import *

server_socket = socket.socket() #function socket() creates websocket connection
print("Socket created")

#bind socket with port number
server_socket.bind(("127.0.0.1", 9570))

server_socket.listen() # number of listeners
print("Waiting for connection")

while True:
    client_socket, address = server_socket.accept()
    print("Connected to socket with", address)
    
    client_socket.send(bytes("Apriltag data", "utf-8")) #must send data through bytes only
    
    client_socket.close() #important to close
    
    
    
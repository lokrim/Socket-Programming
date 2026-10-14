# Vanilla TCP server
# 1) create socket with params ipv4 (AF_INET) and tcp (SOCK_STREAM)
# 2) bind to addr and port
# 3) listen
# 4) accept client connection
# 5) recieve data
# 6) send data
# 7) close socket

import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("127.0.0.1", 5001))

server.listen(1)
print("Server waiting for connection")

conn, addr = server.accept()
print("Connected to", addr)

data = conn.recv(1024)
print("Data recieved: ", data.decode())

conn.send("Hello from server.".encode())

conn.close()
server.close()

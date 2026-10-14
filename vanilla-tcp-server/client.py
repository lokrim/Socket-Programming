# Vanilla TCP client
# 1) create socket
# 2) connect to server using addr and port
# 3) send/recv
# 4) close

import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(("127.0.0.1", 5001))

client.send("Hello from client.".encode())

data = client.recv(1024)
print("Server sent: ", data.decode())

client.close()

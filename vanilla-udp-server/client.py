# Vanilla UDP client
# 1) create socket with params
# 2) send/recv - no connect()
# 3) close client socket

import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client.sendto("Hello from client.".encode(), ("127.0.0.1", 5000))

data, addr = client.recvfrom(1024)
print("Server sent: ", data.decode())

client.close()

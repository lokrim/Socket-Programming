# Vanilla UDP server
# 1) create socket with SOCK_DGRAM
# 2) bind to addr and port
# 3) While loop to send/recv - both require addr as params - no accept()

import socket

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server.bind(("127.0.0.1", 5000))
print("UDP server waiting for connection...")

while True:

    data, addr = server.recvfrom(1024)
    print("Client sent: ", data.decode())

    server.sendto("Hello from server".encode(), addr)

# Threaded TCP server
# 1) Handle client helper - treats conn as a file
# 2) create socket, bind, listen
# 3) while loop to accept connections - connections can be simultaneosly handled
# 4) define thread target as handle client helper

import socket
import threading

def handle_client(conn, addr):
    print("Connected to: ", addr)

    # treat conn as file
    with conn:
        data = conn.recv(1024)

        if data:
            print("Client sent: ", data.decode())
            conn.sendall("Hello from server.".encode())

    print("Disconnected ", addr)

# standard tcp server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 5001))
server.listen(1)
print("Server listening...")

while True:

    conn, addr = server.accept()

    thread = threading.Thread(target=handle_client, args=(conn, addr))

    thread.start()

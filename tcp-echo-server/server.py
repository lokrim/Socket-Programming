import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind(("127.0.0.1", 5001))

server.listen()
print("Server waiting for connection")

while True:
    conn, addr = server.accept()
    print("Connected to", addr)

    with conn:
        data = conn.recv(1024)
        if not data:
            print("Client has disconnected")
            break
        print("Data Recieved: ", data.decode())

        # echo back same data recieved
        conn.sendall(data)

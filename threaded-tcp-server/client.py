import socket
import time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(("127.0.0.1", 5001))

client.send("Hello from client".encode())

time.sleep(10)

data = client.recv(1024)
print("Server sent: ", data.decode())

client.close()

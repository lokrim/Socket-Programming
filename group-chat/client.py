import socket
import threading


def receive(sock):
    with sock.makefile("rb") as f:
        for line in f:
            print(line.decode(), end="")


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 9004))

group = input("Group name: ")
name = input("Your name: ")

client.sendall(f"JOIN {group} {name}\r\n".encode())

threading.Thread(
    target=receive,
    args=(client,),
    daemon=True
).start()

try:
    while True:
        message = input()

        if message.upper() == "QUIT":
            client.sendall(b"QUIT\r\n")
            break

        client.sendall(f"MSG {message}\r\n".encode())

finally:
    client.close()

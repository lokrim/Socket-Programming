
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client.connect(("127.0.0.1", 9000))
print("Connected to server. Type 'quit' to exit.")

with client, client.makefile("rwb", buffering=0) as f:
    while True:
        msg = input("You: ")

        # Send message terminated by newline
        f.write(msg.encode() + b"\n")

        if msg.lower() == "quit":
            break

        # Receive echoed response
        response = f.readline()
        print("Server:", response.decode().rstrip("\r\n"))

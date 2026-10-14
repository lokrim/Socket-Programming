
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 9001))

with client, client.makefile("rwb") as f:
    while True:
        cmd = input("Command: ")

        f.write((cmd + "\n").encode())
        f.flush()

        if cmd.upper() == "QUIT":
            break

        if cmd.upper().startswith(("FILE ", "GREP ")):
            while True:
                line = f.readline()

                if not line:
                    break

                if line.rstrip(b"\r\n") == b"<EOF>":
                    break

                print(line.decode(errors="replace"), end="")

            print()
        else:
            print("Server:", f.readline().decode().strip())

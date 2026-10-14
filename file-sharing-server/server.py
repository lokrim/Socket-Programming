import socket, threading
from pathlib import Path

SHARED = Path("shared")
SHARED.mkdir(exist_ok=True)

def handle_client(conn, addr):
    print("Connected to: ", addr)

    with conn, conn.makefile("rwb") as f:
        for line in f:
            parts = line.decode().strip().split(" ", 2)
            cmd = parts[0].upper()

            if cmd == "PING":
                f.write(b"PONG\n")
                f.flush()

            elif cmd == "FILE" and len(parts) >= 2:
                send_file(f, parts[1])

            elif cmd == "GREP" and len(parts) == 3:
                send_file(f, parts[1], parts[2])

            elif cmd == "QUIT":
                break

            else:
                f.write(b"ERR unknown cmd.")
                f.flush()

    print("Connection disconnected.")

def send_file(f, name, search=None):

    if Path(name).name != name:
        f.write(b"ERR invalid filename\n<EOF>\n")
        f.flush()
        return

    try:
        with open(SHARED / name, encoding="utf-8") as file:
            for line in file:
                if search is None or search in line:
                    f.write(line.encode('utf-8'))

        f.write(b"\n<EOF>\n")

    except OSError:
        f.write(b"ERR cannot open file\n<EOF>\n")

    f.flush()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("127.0.0.1", 9001))
server.listen()

print("Server listening on port 9001...")

while True:
    conn, addr = server.accept()
    threading.Thread(
        target=handle_client,
        args=(conn, addr),
        daemon=True
    ).start()

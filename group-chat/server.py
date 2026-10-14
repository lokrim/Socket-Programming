import socket
import threading

groups = {}
lock = threading.Lock()

def broadcast(group, name, message):

    # wraps aquiring and releasing lock in a clean block
    with lock:
        clients = list(groups.get(group, {}).keys())

    for client in clients:
        try:
            client.sendall(f"[{name}] {message}\r\n".encode())
        except OSError:
            pass

def handle(conn, addr):
    group = name = None

    try:
        with conn.makefile("rb") as f:
            for raw in f:
                line = raw.decode().rstrip("\r\n")

                if line.startswith("JOIN"):
                    parts = line.split(" ", 2)

                    if len(parts) != 3 or not parts[1] or not parts[2]:
                        conn.sendall(f"ERR {name} could not join group {group}\r\n".encode())
                        continue

                    group, name = parts[1], parts[2]

                    with lock:
                        groups.setdefault(group, {})[conn] = name

                    conn.sendall(f"Joined group {group}\r\n".encode())

                elif line.startswith("MSG "):

                    if group == None:
                        conn.sendall(b"ERR Join a group first\r\n")
                    else:
                        broadcast(group, name, line[4:])

                elif line.upper() == "QUIT":
                    break

                else:
                    conn.sendall(b"ERR unknown command\r\n")

    except OSError:
        pass

    finally:
        # exectutes when client disconnects
        with lock:
            if group is not None:
                # client is removed from the group
                groups.get(group, {}).pop(conn, None)

        conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("127.0.0.1", 9004))
server.listen()

print("Chat server listening on port 9004...")

while True:
    conn, addr = server.accept()
    threading.Thread(
        target=handle,
        args=(conn, addr),
        daemon=True
    ).start()

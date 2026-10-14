# message framing, file-like socket I/O, connection reuse, daemon threading and graceful server configuration

import socket
import threading

def handle_client(conn, addr):
    # treat conn as a framed file
    with conn, conn.makefile("rwb", encoding="utf-8", buffering=0) as f:
        for line in f:
            # strip eof chars of the bytes recieved
            msg = line.rstrip(b"\r\n")

            if msg.lower == "quit":
                break

            # write to client conn file
            f.write(msg + b"\r\n")

def main():

    # standard tcp server with reusable addr
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # SOL_SOCKET - socket layer option
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("127.0.0.1", 9000))
    server.listen(128)
    print("Server listening...")

    while True:

        conn, addr = server.accept()

        thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)

        thread.start()

if __name__ == "__main__":
    main()

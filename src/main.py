import socket


def main():
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", 3003))
    server.listen()
    client_socket, _address = server.accept()
    while True:
        data = receive_data(client_socket)
        client_socket.sendall("hello\0".encode("utf-8"))


def receive_data(client_socket):
    buffer = b""

    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        buffer += data
        if buffer.endswith(b"\0"):
            break
    return buffer.decode("utf-8")


if __name__ == "__main__":
    main()

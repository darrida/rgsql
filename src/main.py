import socket

from parser import assign_nodes, parse

HOST = "0.0.0.0"
PORT = 3003


def main():
    try:
        server = socket.socket()
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
        print("Server listening on 3003")

        while True:
            client_socket, _address = server.accept()
            print("Connection started...")

            while True:
                data = receive_data(client_socket)
                if not data:
                    print("Connection ended.")
                    break

                # print(data.split(","))

                data = parse(data)
                parsed = assign_nodes(data)

                client_socket.sendall(f"{parsed}\0".encode("utf-8"))

            client_socket.close()

    except KeyboardInterrupt as e:
        print(e)
        print("Server shutdown")


def receive_data(client_socket) -> bytes:
    buffer = b""

    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        buffer += data
        if buffer.endswith(b"\0"):
            break

        if data:
            print(data)

    return buffer.decode("utf-8")


if __name__ == "__main__":
    main()

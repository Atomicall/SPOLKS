import socket


class ClientDescriptor:
    ip_address: str
    connection: socket.socket
    client_id: str

    def __init__(self, new_connection: socket.socket,
                 client_ip_address: str):
        self.connection = new_connection
        self.ip_address = client_ip_address

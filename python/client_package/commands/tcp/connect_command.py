import socket

from client_package.commands.command import Command
from client_package.errors.invalid_command import InvalidCommand
from shared.consts import (KEEP_ALIVE_COUNT, KEEP_ALIVE_INTERVAL,
                           KEEP_ALIVE_TIME, CLIENT_TIMEOUT)
from shared.utils.socket import set_socket_keep_alive


class ConnectCommand(Command):
    _connection: socket.socket
    _server_address: str
    _server_port: int

    def __init__(self, params: list,
                 set_executor_connection: callable):
        self._connection = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)

        self._connection.settimeout(CLIENT_TIMEOUT)

        set_socket_keep_alive(
            self._connection,
            keep_alive_time=KEEP_ALIVE_TIME,
            keep_alive_interval=KEEP_ALIVE_INTERVAL,
            max_probes=KEEP_ALIVE_COUNT)

        set_executor_connection(self._connection)

        address = params[0].split(':')

        try:
            socket.inet_aton(address[0])

            self._server_address = address[0]
            self._server_port = int(address[1])
        except socket.error:
            raise InvalidCommand

    def execute(self):
        self._connection.connect(
            (self._server_address, self._server_port))

        print(
            f'Successfully connected to server on {self._server_address}:{self._server_port}')

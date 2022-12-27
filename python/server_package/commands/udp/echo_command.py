import socket
from typing import Tuple

from server_package.commands.command import Command
from shared.udp.udp_transport import receive
from shared.utils.logger import Log


class UdpEchoCommand(Command):
    _sock: socket.socket

    def __init__(self, sock: socket.socket, address: Tuple[str, int]):
        self._sock = sock
        self._address = address

    def generate_message(self):
        data, address = receive(self._sock, self._address)

        message = data.decode('utf-8')

        print(f'Echoed from client: {message}')
        Log.logger.info(
            f'Echoed from client: {message}')

import os
import socket
from typing import Tuple

from server_package.commands.command import Command
from shared.udp.udp_transport import receive
from shared.utils.logger import Log


class UdpUploadCommand(Command):
    _sock: socket.socket

    def __init__(self, sock: socket.socket,
                 address: Tuple[str, int], configuration: dict):
        self._sock = sock
        self._address = address
        self._file_name = configuration['file_name']

        if os.path.exists(self._file_name):
            os.remove(self._file_name)

    def generate_message(self):
        data, address = receive(
            self._sock, self._address, self._file_name)

        print(
            f'\nFile {self._file_name} has been successfully downloaded by server')
        Log.logger.info(
            f'File {self._file_name} has been successfully downloaded by server')

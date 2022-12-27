import os
import pickle as pk
import socket
from time import perf_counter
from typing import Tuple

from client_package.commands.command import Command
from shared.commands import Commands
from shared.consts import BIT_RATE_KBPS
from shared.udp.compose_packets import compose_packets
from shared.udp.udp_transport import receive, send
from shared.utils.bit_rate import bit_rate


class UdpDownloadCommand(Command):
    _connection: socket.socket
    _address: Tuple[str, int]
    _file_name: str

    def __init__(self, params: list, connection: socket.socket):
        temp = tuple(params[0].split(':'))
        self._address = (temp[0], int(temp[1]))
        self._connection = connection
        self._file_name = params[1]

        if os.path.exists(self._file_name):
            os.remove(self._file_name)

    def execute(self):
        command = {
            'command': Commands.UDP_DOWNLOAD.value,
            'file_name': self._file_name}
        message = compose_packets(pk.dumps(command))

        start_time = perf_counter()

        send(self._connection, self._address, message, 1)

        date, address = receive(
            self._connection, self._address, self._file_name)

        end_time = perf_counter()

        file_size = os.path.getsize(filename=self._file_name)

        print(f'File {self._file_name} has been successfully uploaded by client '
              f'Bit rate: {bit_rate(file_size=file_size, time_spent=float(end_time-start_time))}')

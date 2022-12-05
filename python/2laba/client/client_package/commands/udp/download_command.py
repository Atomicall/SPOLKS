from client_package.commands.command import Command
from shared.commands import Commands
from shared.udp.udp_transport import send, receive
from shared.udp.compose_packets import compose_packets
import os
import socket
import pickle as pk
from typing import Tuple
from time import perf_counter
from shared.consts import BIT_RATE_KBPS

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
        command = {'command': Commands.UDP_DOWNLOAD.value, 'file_name': self._file_name}
        message = compose_packets(pk.dumps(command))

        start_time = perf_counter()
        
        send(self._connection, self._address, message, 1)

        date, address = receive(self._connection, self._address, self._file_name)

        end_time = perf_counter()
        
        file_size = os.path.getsize(filename=self._file_name)
        if (end_time - start_time) > 0:
            bit_rate = file_size / float((end_time - start_time))
            
        print(f'File {self._file_name} has been successfully uploaded by client '
              f'Bit rate: {round(bit_rate * BIT_RATE_KBPS, 3)} kBps')
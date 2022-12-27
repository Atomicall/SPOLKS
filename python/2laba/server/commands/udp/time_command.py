import datetime
import pickle as pk
import socket
from typing import Tuple

from server_package.commands.command import Command
from shared.udp.compose_packets import compose_packets
from shared.udp.udp_transport import send


class UdpTimeCommand(Command):
    _sock: socket.socket

    def __init__(self, sock: socket.socket, address: Tuple[str, int]):
        self._sock = sock
        self._address = address

    def generate_message(self):
        date = datetime.datetime.now()

        message = compose_packets(pk.dumps(date))

        send(self._sock, self._address, message)

        print(f'Client requested current date. Date is: {date}')

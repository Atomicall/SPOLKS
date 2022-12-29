import os
import pickle as pk
import socket
from os import path
from time import perf_counter, sleep

from client_package.commands.command import Command
from shared.commands import Commands
from shared.consts import (CLIENT_TIMEOUT, CLIENT_TIMEOUT_COUNT, FILES_FOLDER,
                           MAX_PROBES, TCP_PACKET_SIZE)
from shared.errors.disconnected import DisconnectedException
from shared.utils.bit_rate import bit_rate
from shared.utils.console import progress


class DownloadCommand(Command):
    _file_name: str
    _connection: socket.socket
    _file_size: int

    def __init__(self, params: list, connection: socket.socket):
        self._file_name = params[0]
        self._connection = connection

    def _get_file(self):
        print(f'Downloading File {self._file_name}')

        read_bytes = 0
        probes = 0
        with open(path.join(FILES_FOLDER, self._file_name), 'wb') as file:
            while read_bytes < self._file_size:
                failed = 0
                try:
                    data = self._connection.recv(TCP_PACKET_SIZE)
                    if not data:
                        raise DisconnectedException

                    failed = 0
                    self._connection.send(pk.dumps({'ACK': True}))

                    read_bytes += len(data)

                    progress(
                        read_bytes,
                        self._file_size,
                        self._file_name)

                    file.write(data)
                except socket.timeout:
                    probes += 1

                    if probes > MAX_PROBES:
                        raise socket.timeout

                    print(
                        f'\nConnection timeout. Waiting for {probes} of {MAX_PROBES}')

                    continue
                except DisconnectedException:
                    print(f"Lost connection, trying after timout...")
                    if failed >= CLIENT_TIMEOUT_COUNT:
                        failed += 1
                        sleep(CLIENT_TIMEOUT)
                        continue
                    else:
                        raise DisconnectedException(f"No connection after {failed} tries")

    def _initiate_file_exchange(self):
        data = {
            'command': Commands.DOWNLOAD.value,
            'file_name': self._file_name}

        message = pk.dumps(data)

        self._connection.send(message)

        response = pk.loads(self._connection.recv(TCP_PACKET_SIZE))

        if os.path.exists(self._file_name):
            os.remove(self._file_name)

        self._file_size = response['file_size']

    def execute(self):
        try:

            self._initiate_file_exchange()

            message = pk.dumps({'ACK': True})

            start_time = perf_counter()
            self._connection.send(message)

            self._get_file()

            end_time = perf_counter()

            print(
                f'\nFile {self._file_name} has been successfully downloaded by server,'
                f' Bit rate: {bit_rate(file_size=self._file_size, time_spent=float(end_time-start_time))}'
            )

        except FileNotFoundError:
            print('Such file doesn\'t exist. Try another one')
        except DisconnectedException as e:
            print(f"Connection lost, after timeout {e}. Try to reconnect to the server")

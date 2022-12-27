import pickle as pk
import socket
from select import select
from typing import Dict, List

from server_package.command_builder import build_command, build_udp_command
from server_package.commands.command import Command
from shared.consts import (IS_LOCAL_HOST, KEEP_ALIVE_COUNT,
                           KEEP_ALIVE_INTERVAL, KEEP_ALIVE_TIME,
                           TCP_PACKET_SIZE, TCP_SERVER_PORT,
                           UDP_MAX_PACKET_SIZE, UDP_SERVER_PORT)
from shared.udp.compose_packets import compose_packets
from shared.udp.udp_transport import receive
from shared.utils import ip
from shared.utils import socket as sock_utils
from shared.utils.logger import Log


class Server:
    MAX_ACTIVE_CLIENTS: int = 10
    TCP_PORT: int = TCP_SERVER_PORT
    UDP_PORT: int = UDP_SERVER_PORT

    # general socket used to listen for clients
    _tcp_main_sock: socket.socket
    _udp_sock: socket.socket

    # socket for specific connection
    _inputs: List[socket.socket] = []
    _outputs: List[socket.socket] = []
    _issued_commands: Dict[socket.socket, Command] = {}
    # dict : { connection: ip_address }
    _clients: Dict[socket.socket, str] = {}

    def __init__(self):
        Log.logger.info("Initializing sockets...")
        self._init_sockets()

    def work(self):
        while True:
            try:
                readable, writable, exceptional = select(
                    self._inputs, self._outputs, self._inputs, 1.0)
                for sock in readable:
                    try:
                        # UDP segment
                        if sock is self._udp_sock:
                            message, address = receive(self._udp_sock)
                            Log.logger.info(
                                f"Got UDP message from {address} ;")

                            command: Command = build_udp_command(
                                self._udp_sock, message, address)

                            command.generate_message()
                            continue
                        # TCP segment
                        if sock is self._tcp_main_sock and len(
                                self._inputs) <= self.MAX_ACTIVE_CLIENTS:
                            Log.logger.info(
                                f"Got new TCP connection {sock}")
                            self._initialize_client()

                        else:
                            message = sock.recv(TCP_PACKET_SIZE)

                            if message:

                                if sock not in self._issued_commands:
                                    self._issued_commands[sock] = build_command(
                                        message)
                                else:
                                    self._issued_commands[sock].set_response(
                                        message)

                                if sock not in self._outputs:
                                    self._outputs.append(sock)
                            else:
                                self._free_socket(sock)
                                Log.logger.info(
                                    f'Connection closed by client - {self._clients[sock]}')
                                print(
                                    'Connection closed by client_package. ' +
                                    f'{self._clients[sock]} has disconnected from the server'
                                )

                    except FileNotFoundError as e:
                        print(
                            'Such file doesn\'t exist. Please try another one')
                        Log.logger.error(
                            f'Such file "{e.filename}" does not exist. Please try another one')

                    except socket.error as error:
                        if sock in self._clients:
                            print(self._clients[sock], error)
                            Log.logger.error(
                                f"Error with connection - {self._clients[sock]}; {error}")
                            self._free_socket(sock)

                    except Exception as error:
                        if sock.fileno() == -1:
                            print(
                                f"Client closed connection")
                            Log.logger.info(
                                f"Client closed connection - {sock}")
                            continue
                        else:
                            print(f'Caught error: {error}')
                            Log.logger.error(
                                f"Caught error - {error}")

                for sock in writable:
                    message = next(
                        self._issued_commands[sock].generate_message())
                    sock.send(message)

                    if self._issued_commands[sock].is_finished:
                        Log.logger.info(
                            f"Command complete - {self._issued_commands[sock]};")
                        del self._issued_commands[sock]
                    self._outputs.remove(sock)

                for sock in exceptional:
                    print(f'Exception on {sock.getpeername()}')
                    Log.logger.warning(
                        f'Exception on {sock.getpeername()}')
                    self._free_socket(sock)

            except KeyboardInterrupt as error:
                print(f"Closing server by KeyboardInterrupt....")
                Log.logger.warning(
                    f"Closing server by KeyboardInterrupt....")
                socks = list(self._clients.keys())
                for sock in socks:
                    self._free_socket(sock)
                socks = list(self._issued_commands.keys())
                for sock in socks:
                    self._free_socket(sock)
                for sock in self._inputs:
                    self._free_socket(sock)
                for sock in self._outputs:
                    self._free_socket(sock)
                break
            except Exception as error:
                print(f'Unexpected error caught! {error}')
                Log.logger.critical(
                    f'Unexpected error caught! {error}')
                break

    def _init_sockets(self):
        self._set_tcp_main_socket()
        endpoint = f"{ip.get_local_ip_address(is_local_host=IS_LOCAL_HOST)}"
        print(
            f'TCP Server created on address: {endpoint}:{self.TCP_PORT}')
        self._set_udp_socket()
        print(
            f'UDP Server created on address: {endpoint}:{self.UDP_PORT}')
        Log.logger.info(
            f'TCP Server created on address: {endpoint}:{self.TCP_PORT}')
        Log.logger.info(
            f'UDP Server created on address: {endpoint}:{self.UDP_PORT}')

    def _set_tcp_main_socket(self):
        # creating socket that accepts IPv4 address and works with TCP
        # protocol
        self._tcp_main_sock = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self._tcp_main_sock.bind(
            (ip.get_local_ip_address(
                is_local_host=IS_LOCAL_HOST),
                self.TCP_PORT))
        self._tcp_main_sock.setblocking(False)
        self._tcp_main_sock.listen(self.MAX_ACTIVE_CLIENTS)
        self._inputs.append(self._tcp_main_sock)

    def _set_udp_socket(self):
        self._udp_sock = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM)
        self._udp_sock.bind(
            (ip.get_local_ip_address(
                is_local_host=IS_LOCAL_HOST),
                self.UDP_PORT))
        self._inputs.append(self._udp_sock)

    def _initialize_client(self):
        connection, address = self._tcp_main_sock.accept()
        Log.logger.info(
            f"New connection initialized - {address}; ")

        connection.setblocking(False)
        sock_utils.set_socket_keep_alive(
            connection,
            keep_alive_time=KEEP_ALIVE_TIME,
            keep_alive_interval=KEEP_ALIVE_INTERVAL,
            max_probes=KEEP_ALIVE_COUNT)
        self._inputs.append(connection)
        self._clients[connection] = address

        print(f'Client connected. Address {address}')

    def _free_socket(self, sock: socket.socket):
        Log.logger.info("Clearing resources...")
        if sock in self._inputs:
            self._inputs.remove(sock)
        if sock in self._outputs:
            self._outputs.remove(sock)
        if sock in self._issued_commands:
            del self._issued_commands[sock]
        if sock in self._clients:
            del self._clients[sock]
        Log.logger.info("Clearing resources completed.")

        sock.close()

from server_package.server import Server
from shared.utils.logger import Logger


def main():
    global logger
    logger = Logger("INFO")
    logger.logger.info("Starting server")
    server = Server()
    server.work()


if __name__ == '__main__':
    main()

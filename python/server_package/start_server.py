from server_package.server import Server
from shared.utils.logger import Log


def main():
    Log.logger.info("Starting server..")
    server = Server()
    server.work()


if __name__ == '__main__':
    main()

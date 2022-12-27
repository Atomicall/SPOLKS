import datetime
import pickle as pk

from server_package.commands.command import Command
from shared.utils.logger import Log


class TimeCommand(Command):
    _data = ''
    is_finished = False

    def __init__(self):
        date = datetime.datetime.now()

        self._data = pk.dumps({'payload': date})

        print(f'Client requested current time. Time is {date}')
        Log.logger.info(
            f'Client requested current time. Time is {date}')

    def generate_message(self):
        data = self._data

        self._data = ''

        self.is_finished = True

        yield data

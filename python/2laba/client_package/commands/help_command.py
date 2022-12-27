from client_package.commands.command import Command


class HelpCommand(Command):
    def execute(self):
        print('All the params are marked with \'@\' symbol', '\n')
        print('List of supported commands:')
        print('connect @ip:@port        -- connects to a server_package by a given address through TCP')
        print('disconnect               -- disconnects client_package from the server_package through TCP')
        print('echo @text               -- send @text to server_package through TCP, receive it back and print out')
        print('time                     -- returns current time from the server_package through TCP')
        print('upload @path_to_file     -- upload the given file to a server_package through TCP')
        print('download @path_to_file   -- download the given file from a server_package through TCP')
        print('\n')
        print('udp_echo @ip:@port @text             -- send @text to server_package through UDP, receive it back and print out')
        print('udp_time @ip:@port                   -- returns current time from the server_package through UDP')
        print('udp_upload @ip:@port @path_to_file   -- upload the given file to a server_package through UDP')
        print('udp_download @ip:@port @path_to_file -- download the given file from a server_package through UDP')
        print('\n')

from .command_cmd import command_cmd

def wuauclt(arguments = False):
    if arguments:
        return command_cmd(f'wuauclt {arguments}')
    return command_cmd('wuauclt')
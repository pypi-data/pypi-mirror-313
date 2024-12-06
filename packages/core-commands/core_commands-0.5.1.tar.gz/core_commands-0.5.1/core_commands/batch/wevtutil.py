from .command_cmd import command_cmd

def wevtutil(arguments):
    return command_cmd(f"wevtutil {arguments}")
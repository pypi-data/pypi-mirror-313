from .command_cmd import command_cmd

def wusa(arguments):
    if (arguments):
        command_cmd(f"wusa {arguments}")
    
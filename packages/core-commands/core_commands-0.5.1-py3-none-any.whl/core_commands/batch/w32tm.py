from .command_cmd import command_cmd

def w32tm(arguments):
    return command_cmd(f"w32tm {arguments}")
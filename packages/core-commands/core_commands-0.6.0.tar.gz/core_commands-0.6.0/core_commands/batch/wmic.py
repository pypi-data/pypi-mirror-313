from .command_cmd import command_cmd

def wmic(arguments):
    if arguments:
        return command_cmd(f"wmic {arguments}")
    return command_cmd("wmic")
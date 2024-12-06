from .command_cmd import command_cmd

def winrs(arguments):
    if(arguments):
        return command_cmd(f"winrs {arguments}")
    return command_cmd("winrs")
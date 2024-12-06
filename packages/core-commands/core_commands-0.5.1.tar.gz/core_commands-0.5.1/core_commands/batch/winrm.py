from .command_cmd import command_cmd

def winrm(arguments):
    if arguments:
        return command_cmd(f"winrm {arguments}")
    return command_cmd("winrm")
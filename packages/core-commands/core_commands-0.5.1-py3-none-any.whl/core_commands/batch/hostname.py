from .command_cmd import command_cmd

def hostname(arguments = False):
    if(arguments):
        return command_cmd(f"hostname {arguments}")
    return command_cmd("hostname")

from .command_cmd import command_cmd

def wbadmin(arguments):
    return command_cmd(f"wbadmin {arguments}")
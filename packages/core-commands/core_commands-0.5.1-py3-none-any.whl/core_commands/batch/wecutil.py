from .command_cmd import command_cmd

def wecutil(arguments):
    command_base = f"wecutil"
    return command_cmd(f"{command_base} {arguments}")
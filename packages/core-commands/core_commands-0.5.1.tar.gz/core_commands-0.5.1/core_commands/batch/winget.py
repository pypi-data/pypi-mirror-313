from .command_cmd import command_cmd

def winget(command,options = False):
    if(options):
        return command_cmd(f"winget {command} {options}")
    return command_cmd(f"winget {command}")
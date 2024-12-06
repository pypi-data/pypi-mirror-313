from .command_cmd import command_cmd

def whoami(arguments = False):
    command_base = f"whoami"
    if(arguments):
        return command_cmd(f"{command_base} {arguments}")
    return command_cmd(command_base)
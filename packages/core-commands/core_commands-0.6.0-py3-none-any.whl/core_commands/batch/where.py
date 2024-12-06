from .command_cmd import command_cmd

def where(pathPattern,arguments = False):
    base_command = f"where {pathPattern}"
    if(arguments):
        return command_cmd(f"{base_command} {arguments}")
    return command_cmd(base_command)
from .command_cmd import command_cmd

def bcdedit(arguments = False):
    if arguments:
        return command_cmd(f"bcdedit {arguments}")
    return command_cmd(f"bcdedit")
from .command_cmd import command_cmd

def BREAK(rest = False):
    if rest:
        return command_cmd(f"break {rest}")
    return command_cmd("break")
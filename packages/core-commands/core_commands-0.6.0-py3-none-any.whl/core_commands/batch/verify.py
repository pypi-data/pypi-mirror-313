from .command_cmd import command_cmd

def verify(onOff):
    if (onOff):
        return command_cmd(f"verify {onOff}")
    return command_cmd("verify")

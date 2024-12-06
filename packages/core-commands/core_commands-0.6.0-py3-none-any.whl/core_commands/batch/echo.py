from .command_cmd import command_cmd

def echo(text = False):
    """
    Display messages on screen, turn command-echoing on or off.

    arguments: ON | OFF | /?
    """
    if (text):
        return command_cmd(f'echo {text}')
    return command_cmd("echo")
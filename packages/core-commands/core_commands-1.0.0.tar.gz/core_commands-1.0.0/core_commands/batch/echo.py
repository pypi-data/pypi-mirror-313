from ..bin.baxh import baxh

def echo(text = False):
    """
    Display messages on screen, turn command-echoing on or off.

    arguments: ON | OFF | /?
    """
    arguments=text
    return baxh("echo",arguments)
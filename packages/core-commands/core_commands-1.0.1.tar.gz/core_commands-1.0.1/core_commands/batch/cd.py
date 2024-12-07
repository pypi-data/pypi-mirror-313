from ..bin.baxh import baxh

def cd(arguments=None):
    """
    Change Directory - Select a Folder (and drive)
    """
    return baxh("cd",f'{arguments}')  # type: ignore
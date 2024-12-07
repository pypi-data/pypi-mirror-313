from ..bin.baxh import baxh

def bcdedit(arguments = None):
    return baxh('bcdedit',f"{arguments}")
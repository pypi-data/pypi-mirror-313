from ..bin.baxh import baxh

def attrib(arguments = None):
    """
    Display or change file attributes.
    """
    return baxh('attrib',f"{arguments}")
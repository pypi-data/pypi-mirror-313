from ..bin.baxh import baxh

def w32tm(arguments=None):
    return baxh(f"w32tm {arguments}")
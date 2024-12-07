from ..bin.baxh import baxh

def cacls(arguments = None):
    return baxh("cacls",f"{arguments}")
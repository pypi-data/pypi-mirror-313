from ..bin.baxh import baxh

def netstat(arguments=None):
    return baxh("netstat",arguments)
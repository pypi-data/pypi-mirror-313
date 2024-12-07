from ..bin.baxh import baxh

def copy(source = "",destination = "",sourceArguments = "",destinationArguments = ""):
    arguments = f"{source} {sourceArguments} {destination} {destinationArguments}"
    return baxh("copy",arguments)
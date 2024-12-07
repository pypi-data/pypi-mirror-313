from ..bin.baxh import baxh

def call(arguments=None):
    """
    Call one batch program from another, or call a subroutine.
    """
    return baxh("call",arguments) #pylint: disable=no-member
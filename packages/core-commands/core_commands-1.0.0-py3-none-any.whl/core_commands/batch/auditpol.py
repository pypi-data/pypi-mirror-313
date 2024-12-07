from ..bin.baxh import baxh

def auditpol(arguments = None):
    return baxh(f"auditpol",f"{arguments}")   # auditpol.exe
from .cd import cd

def chdir(arguments = None):
    """
    Change Directory - Select a Folder (and drive)
    """
    return cd(f'{arguments}') # pragma: no cover
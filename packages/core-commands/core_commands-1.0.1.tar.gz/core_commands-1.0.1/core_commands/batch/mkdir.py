if __name__ == "__main__":
    from core_commands.bin.baxh import baxh
else:
    from ..bin.baxh import baxh
from pathlib import PurePath

def mkdir(arguments=None):
    return baxh('mkdir',arguments)

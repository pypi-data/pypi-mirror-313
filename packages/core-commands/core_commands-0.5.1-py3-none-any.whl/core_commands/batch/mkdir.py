if __name__ == "__main__":
    from command_cmd import command_cmd
else:
    from .command_cmd import command_cmd
from pathlib import PurePath

def mkdir(destination = False,arguments = False,options={
    "debug": False
}):
    if (options["debug"]):
        print(destination,arguments)
    if (destination):
        destination = PurePath(destination)
        return command_cmd(f'mkdir {arguments} "{destination}"')

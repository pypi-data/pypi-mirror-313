from .command_cmd import command_cmd

def cd(pathname,arguments = False):
    """
    Change Directory - Select a Folder (and drive)
    """
    command_cmd(f"cd {arguments} {pathname}")
from .command_cmd import command_cmd

def windiff(path1,path2):
    return command_cmd(f"windiff {path1} {path2}")
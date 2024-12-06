from .command_cmd import command_cmd

def xcopy(source,destination,arguments):
    command_base = "xcopy"
    if (arguments):
        return command_cmd(f"{command_base} {source} {destination} {arguments}")
    return command_cmd(f"{command_base} {source} {destination}")
from .command_cmd import command_cmd

def copy(source,destination,sourceArguments = "",destinationArguments = ""):
    command = f"copy {source} {sourceArguments} {destination} {destinationArguments}"
    return command_cmd(command)
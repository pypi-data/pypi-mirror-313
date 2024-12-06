from .command_cmd import command_cmd

# TODO: este comando es mas profundo

def bcdboot(arguments):
    return command_cmd(f"bcdboot {arguments}")
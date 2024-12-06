from .command_cmd import basic_execution

def schtasks(arguments):
    return basic_execution("schtasks",arguments)
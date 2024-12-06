from .command_cmd import basic_execution

def vssadmin(arguments):
    return basic_execution("vssadmin",arguments)
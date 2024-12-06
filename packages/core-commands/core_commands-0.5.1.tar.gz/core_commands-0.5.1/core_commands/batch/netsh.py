from .command_cmd import basic_execution

def netsh(arguments):
    return basic_execution("netsh",arguments)
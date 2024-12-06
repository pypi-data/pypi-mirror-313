from .command_cmd import basic_execution

def netstat(arguments):
    return basic_execution("netstat",arguments)
from .command_cmd import command_cmd

# TODO: como no entiendo el comando y me da flojera, no pude hacer el comando en profundidad.

def arp(arguments):
    return command_cmd(f"arp {arguments}")
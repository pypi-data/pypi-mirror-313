from .command_cmd import command_cmd

def auditpol(commands):
    return command_cmd(f"auditpol {commands}")
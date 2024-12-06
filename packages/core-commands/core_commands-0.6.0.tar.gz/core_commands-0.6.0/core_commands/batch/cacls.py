from .command_cmd import command_cmd

def cacls(pathname,arguments = False):
    if arguments:
        return command_cmd(f"cacls {pathname} {arguments}")
    return command_cmd(f"cacls {pathname}")
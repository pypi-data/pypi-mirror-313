from .command_cmd import command_cmd

def date(arguments,date_today):
    command_base = "date"
    if (date_today):
        return command_cmd(f"{command_base} {date_today}")
    if (arguments):
        return command_cmd(f"{command_base} {arguments}")
    return command_cmd(command_base)
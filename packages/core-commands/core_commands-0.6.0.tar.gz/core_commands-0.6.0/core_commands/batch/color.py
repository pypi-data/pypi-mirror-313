from .command_cmd import command_cmd

def color(background = False,foreground = False):
    """
    Sets the default console foreground and background colours.
0 = Black - 8 = Gray - 1 = Blue - 9 = Light Blue - 2 = Green - A = Light Green - 3 = Aqua - B = Light Aqua - 4 = Red - C = Light Red - 5 = Purple - D = Light Purple - 6 = Yellow - E = Light Yellow - 7 = White - F = Bright White
    """
    if (background and foreground):
        return command_cmd(f"color {background}{foreground}")
    if (background):
        return command_cmd(f"color {background}")
    if (foreground):
        return command_cmd(f"color {foreground}")
    return command_cmd("color")

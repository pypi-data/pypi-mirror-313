from ..bin.baxh import baxh

def color(background = None,foreground = None):
    """
    Sets the default console foreground and background colours.
0 = Black - 8 = Gray - 1 = Blue - 9 = Light Blue - 2 = Green - A = Light Green - 3 = Aqua - B = Light Aqua - 4 = Red - C = Light Red - 5 = Purple - D = Light Purple - 6 = Yellow - E = Light Yellow - 7 = White - F = Bright White
    """
    arguments=None
    if (background):
        foreground="7"
        arguments = f'{background}{foreground}'
        return baxh(f"color",arguments)
    if (foreground):
        background="7"
        arguments = f'{background}{foreground}'
        return baxh(f"color",arguments)
    if ((background == None or background == "None") and (foreground == None or foreground =="None")):
        return baxh("color")
    arguments = f'{background}{foreground}'
    return baxh("color",arguments)

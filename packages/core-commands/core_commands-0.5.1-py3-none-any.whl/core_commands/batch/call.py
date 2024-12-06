from .command_cmd import command_cmd

def call(filepath, parameters):
    """
    Call one batch program from another, or call a subroutine.
    """
    #TODO: call te deja pasar argumentos a un archivo cmd, la cuestion es que puedes pasarle varios, si se usa una string, no podrias pasar un argumento con espacios, por que no abria manera de pasarle las comillas, entonces se podria usar un array y trabajarlo para que quede como una string y cada uno de sus miembros colocarlos en comillas.
    command = ""
    if (filepath):
        command = f"call {filepath} {parameters}"
    return command_cmd(command)
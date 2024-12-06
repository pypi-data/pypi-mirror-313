from .command_cmd import command_cmd

# TODO: verificar que la primera letra de extencion sea un punto.
def assoc(extencion = False):
    if extencion:
        return command_cmd(f"assoc {extencion}")
    return command_cmd("assoc")
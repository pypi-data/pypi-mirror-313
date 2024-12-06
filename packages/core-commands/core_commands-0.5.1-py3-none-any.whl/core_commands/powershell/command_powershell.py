from subprocess import run

def command_powershell(command_):
        #TODO: deberia verificar que si el sistema es windows.
        return run(f'powershell {command_}',shell=True) 
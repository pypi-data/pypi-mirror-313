from subprocess import run

def command_cmd(command_):
        #TODO: deberia verificar que si el sistema es windows.
        return run(f'{command_}',shell=True)  

def basic_execution(command_name,arguments):
        if arguments:
                return command_cmd(f"{command_name} {arguments}")
        return command_cmd(f"{command_name}")  

# TODO: funcion que te permite ejectar multiples comandos, tanto como cmd con & && y powershell que no tengo idea. o mejor para core-scripts
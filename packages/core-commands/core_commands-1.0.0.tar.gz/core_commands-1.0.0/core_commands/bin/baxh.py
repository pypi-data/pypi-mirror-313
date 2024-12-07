from subprocess import run

def baxh(command,arguments = None):
        return run([f'{command}',f'{arguments or ""}'],
                    capture_output=True,
                    text=True,
                    shell=True
                    )
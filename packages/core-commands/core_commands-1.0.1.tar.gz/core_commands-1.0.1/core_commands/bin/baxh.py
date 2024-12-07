from subprocess import run

def baxh(command,arguments = None):
    if arguments == "None":
        return run([command],
                    capture_output=True,
                    text=True,
                    shell=True
                    )
    if arguments == None:
        return run([command],
                    capture_output=True,
                    text=True,
                    shell=True
                    )
    return run([command,arguments],
                    capture_output=True,
                    text=True,
                    shell=True
                    )
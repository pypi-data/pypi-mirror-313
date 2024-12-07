from subprocess import run

def powershell(command,arguments = None):
        full_command = f"{command} {arguments or ''}"
        return run(["powershell", "-Command", full_command],
                    capture_output=True,
                    text=True,
                    shell=True
                    )
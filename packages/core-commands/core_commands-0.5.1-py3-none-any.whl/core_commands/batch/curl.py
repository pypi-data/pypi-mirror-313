from .command_cmd import command_cmd

def curl(arguments,url):
    """
    Transfer data from or to a server, using one of the supported protocols (HTTP, HTTPS, FTP, FTPS, SCP, SFTP, TFTP, DICT, TELNET, LDAP or FILE). 
    """
    command = f"curl {arguments} {url}"
    return command_cmd(command)
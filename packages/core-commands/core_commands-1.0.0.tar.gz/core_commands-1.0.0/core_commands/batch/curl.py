from ..bin.baxh import baxh

def curl(opciones,url):
    """
    Transfer data from or to a server, using one of the supported protocols (HTTP, HTTPS, FTP, FTPS, SCP, SFTP, TFTP, DICT, TELNET, LDAP or FILE). 
    """
    arguments = f"{opciones} {url}"
    return baxh("curl",arguments)
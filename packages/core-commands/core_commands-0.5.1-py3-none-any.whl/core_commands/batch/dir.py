from .command_cmd import command_cmd

def dir(pathname,arguments,options={
    "debug": False
}):
    if(pathname):
        command_cmd(f"dir {pathname} {arguments}")
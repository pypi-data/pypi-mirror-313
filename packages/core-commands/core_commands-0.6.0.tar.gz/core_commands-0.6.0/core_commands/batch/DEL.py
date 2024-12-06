from .command_cmd import command_cmd

def DEL(arguments,file_attributes,files_to_delete):
    command_base = "del"
    if(arguments):
        if(file_attributes):
            return command_cmd(f"{command_base} {arguments} {file_attributes} {files_to_delete}")
        return command_cmd(f"{command_base} {arguments} {files_to_delete}")
    if(file_attributes):
        return command_cmd(f"{command_base} {file_attributes} {files_to_delete}")
    return command_cmd(f"{command_base} {files_to_delete}")

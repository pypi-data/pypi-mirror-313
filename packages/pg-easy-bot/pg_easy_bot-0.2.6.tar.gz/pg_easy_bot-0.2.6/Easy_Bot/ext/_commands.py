import os
import importlib
from ._unauth import unauthorized


def get_commands_data(commands_dir=None) -> list:
    """
    This function is used to get commands data from a directory.

    It will import all python files in the given directory and get the command name and function from it.
    The function will be unauthorized if the author is not '@pamod_madubashana'.

    Args:
        commands_dir (str): The directory where the commands are located.

    Returns:
        list: A list of lists, where the first item in each list is the command name and the second item is the function.
    """
    if commands_dir ==None:return
    commands_data = []

    for file in os.listdir(commands_dir):
        if str(file).endswith('.py'):
            module_name = file[:-3] 
            if module_name == '__init__':continue
            if '/' in str(commands_dir):commands_dir = str(commands_dir).split('/')[-1]
            module_path = f'{commands_dir}.{module_name}'
            module = importlib.import_module(module_path)
            auther = getattr(module, '__author__', None)
            if auther != '@pamod_madubashana':
                function = unauthorized
            else:
                function_name = getattr(module, '__function__', None)
                function = getattr(module, function_name, None)
            command = getattr(module, '__command__', None)
            
            commands_data.append([command,function])
    print(', '.join(command[0] for command in commands_data) ," Ready")
    return commands_data
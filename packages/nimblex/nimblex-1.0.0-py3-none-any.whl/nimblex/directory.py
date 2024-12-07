# nimblex/directory.py

import os

def print_directory_structure(root_dir, level=0):
    """
    Returns the directory structure in a tree format as a string.

    Args:
        root_dir (str): The root directory to traverse.
        level (int): Current depth level for indentation.

    Returns:
        str: Formatted directory structure.
    """
    indent = '    ' * level
    structure = f"{indent}{os.path.basename(root_dir)}/\n"

    try:
        items = os.listdir(root_dir)
    except PermissionError:
        structure += f"{indent}    [Permission Denied]\n"
        return structure

    for index, item in enumerate(sorted(items)):
        item_path = os.path.join(root_dir, item)
        if os.path.isdir(item_path):
            structure += print_directory_structure(item_path, level + 1)
        else:
            structure += f"{indent}    ├── {item}\n"
    return structure

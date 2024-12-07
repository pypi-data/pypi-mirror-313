# nimblex/utils.py

import os
import datetime

def save_output_to_file(file_name, content):
    """
    Save the output content to a text file in the designated folder.

    Args:
        file_name (str): Name of the file.
        content (str): Content to save.

    Returns:
        str: Path to the saved file.
    """
    from pathlib import Path
    base_folder = Path.home() / "Documents" / "nimblexOutputs"
    base_folder.mkdir(parents=True, exist_ok=True)
    save_path = base_folder / file_name
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(content)
    return save_path

def format_output(structure, is_directory=True):
    """
    Formats the output with colors for terminal display.

    Args:
        structure (str): The structure string.
        is_directory (bool): Flag indicating if the structure is a directory.

    Returns:
        str: Colored formatted string.
    """
    from termcolor import colored
    lines = structure.split('\n')
    formatted_lines = []
    for line in lines:
        if not line.strip():
            continue
        if is_directory and line.endswith('/'):
            formatted_lines.append(colored(line, "cyan"))
        elif is_directory:
            formatted_lines.append(colored(line, "green"))
        else:
            if line.startswith("Classes:") or line.startswith("Functions/Methods:"):
                formatted_lines.append(colored(line, "yellow"))
            else:
                formatted_lines.append(colored(line, "cyan"))
    return "\n".join(formatted_lines)

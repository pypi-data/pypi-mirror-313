import os
import argparse
from pathlib import Path
from termcolor import colored
from nimblex.directory import print_directory_structure
from nimblex.extractors import extract_structure

EXCLUDED_DIRS = [
    "__pycache__", ".git", ".svn", ".hg", ".idea", "node_modules", "bin", "obj",
    "dist", "build", ".vscode", "*.egg-info", "target", "out", "debug", "release", "venv"
]

def handle_directory(path):

    structure = print_directory_structure(path)
    return structure


def handle_file(path):
    """
    Handles file structure extraction and formatting.

    Args:
        path (str): Path to the file.

    Returns:
        str: Formatted file structure.
    """
    try:
        classes, methods = extract_structure(path)
        output = []

        if methods:
            output.append(colored("  Functions/Methods:", "cyan"))
            for method in methods:
                output.append(colored(f"  - {method}", "cyan"))

        return "\n".join(output) if output else "  -"
    except ValueError as e:
        return None  # Skip unsupported file


def extract_project_structure(root_path):
    # Extract and display the full directory structure
    directory_structure = handle_directory(root_path)
    print(colored("\nDirectory Structure:\n", "green"))
    print(directory_structure)

    # Prompt user for the main project path
    project_path = input(colored("\nPlease enter the path where the main project files are located: ", "cyan")).strip()

    # Use current directory if input is empty
    if not project_path:
        project_path = os.getcwd()

    if not os.path.isdir(project_path):
        return colored(f"Error: '{project_path}' is not a valid directory.", "red")

    print(colored("\nOK! Processing ...\n", "yellow"))

    # Traverse the selected directory and process files
    output = [directory_structure, "\n"]
    for root, dirs, files in os.walk(project_path):
        # Exclude hidden directories (those starting with a dot) anywhere in the project structure
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, root_path)

            # Process file
            file_output = handle_file(file_path)
            if file_output:  # Only include supported files
                output.append(f"{relative_path} :")
                output.append(file_output)
                output.append("\n")

    return "\n".join(output)








def remove_colors(text):
    """
    Removes ANSI color codes from the text.

    Args:
        text (str): Text with ANSI color codes.

    Returns:
        str: Plain text without color codes.
    """
    import re
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)


def main():
    parser = argparse.ArgumentParser(
        description="nimblex: A CLI tool for viewing and saving project structures."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=os.getcwd(),
        help="Path to the directory or file to analyze (default: current directory)."
    )
    parser.add_argument(
        "-m",
        "--save",
        action="store_true",
        help="Save the structure of a single directory or file."
    )
    parser.add_argument(
        "-x",
        "--extract",
        action="store_true",
        help="Extract the directory structure and classes/methods for an entire project."
    )
    parser.add_argument(
        "-d",
        "--display",
        action="store_true",
        help="Display the directory structure and classes/methods for an entire project in the terminal."
    )
    args = parser.parse_args()

    target_path = os.path.abspath(args.path)

    if args.extract:
        if not os.path.isdir(target_path):
            print(colored("Error: The -x option requires a directory.", "red"))
            return

        # Extract and save the project structure
        output = extract_project_structure(target_path)

        # Save the output to a file
        try:
            base_folder = Path.home() / "Documents" / "nimblexOutputs"
            base_folder.mkdir(parents=True, exist_ok=True)

            target_name = os.path.basename(target_path.rstrip(os.sep))
            file_name = f"{target_name}_project_structure.txt"
            save_path = base_folder / file_name

            with open(save_path, "w", encoding="utf-8") as f:
                f.write(remove_colors(output))

            print(colored(f"\nStructure saved to: {save_path}", "green"))
        except Exception as e:
            print(colored(f"Failed to save the structure: {e}", "red"))

    elif args.save:
        # Handle directory or file for the -m option
        if os.path.isdir(target_path):
            output = handle_directory(target_path)
        elif os.path.isfile(target_path):
            output = handle_file(target_path)
        else:
            print(colored("Error: The specified path is not valid.", "red"))
            return

        # Save the output to a file
        try:
            base_folder = Path.home() / "Documents" / "nimblexOutputs"
            base_folder.mkdir(parents=True, exist_ok=True)

            target_name = os.path.basename(target_path.rstrip(os.sep))
            file_name = f"{target_name}_structure.txt"
            save_path = base_folder / file_name

            with open(save_path, "w", encoding="utf-8") as f:
                f.write(remove_colors(output))

            print(colored(f"\nStructure saved to: {save_path}", "green"))
        except Exception as e:
            print(colored(f"Failed to save the structure: {e}", "red"))

    elif args.display:
        # Display the structure in terminal
        if os.path.isdir(target_path):
            output = extract_project_structure(target_path)
            print(output)
        elif os.path.isfile(target_path):
            output = handle_file(target_path)
            print(output)
        else:
            print(colored("Error: The specified path is not valid.", "red"))

    else:
        print(colored("Error: No valid option provided. Use -x for extraction or -d for display.", "red"))


if __name__ == "__main__":
    main()

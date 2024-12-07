# nimblex/extractors.py

import os
from nimblex.language_extractors import (
    extract_python_structure,
    extract_cpp_structure,
    extract_csharp_structure,
    extract_go_structure,
    extract_java_structure,
    extract_js_structure,
    extract_typescript_structure,
)

# Mapping file extensions to extractor functions
EXTRACTORS = {
    '.py': extract_python_structure,
    '.cpp': extract_cpp_structure,
    '.cs': extract_csharp_structure,
    '.go': extract_go_structure,
    '.java': extract_java_structure,
    '.js': extract_js_structure,
    '.ts': extract_typescript_structure,
}

def extract_structure(file_path):
    """
    Extract the structure of a file based on its extension.

    Args:
        file_path (str): Path to the file.

    Returns:
        tuple: A tuple containing extracted classes and functions/methods.
    """
    _, file_extension = os.path.splitext(file_path)
    extractor = EXTRACTORS.get(file_extension.lower())
    if not extractor:
        raise ValueError(f"Unsupported file extension: {file_extension}")
    return extractor(file_path)

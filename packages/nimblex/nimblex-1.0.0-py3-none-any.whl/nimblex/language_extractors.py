# nimblex/language_extractors.py

import re

def extract_python_structure(file_path):
    """Extract classes and functions from a Python file."""
    classes, functions = [], []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            class_match = re.match(r"^\s*class\s+(\w+)", line)
            if class_match:
                classes.append(class_match.group(1))
            func_match = re.match(r"^\s*def\s+(\w+)", line)
            if func_match:
                functions.append(func_match.group(1))
    return classes, functions

def extract_cpp_structure(file_path):
    """Extract classes and functions from a C++ file."""
    classes, functions = [], []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            class_match = re.match(r"^\s*class\s+(\w+)", line)
            if class_match:
                classes.append(class_match.group(1))
            func_match = re.match(r"^\s*(?:\w+\s+)+(\w+)\s*\(.*\)\s*{", line)
            if func_match:
                functions.append(func_match.group(1))
    return classes, functions



def extract_csharp_structure(file_path):
    classes = []
    methods = []

    # Regular expression for detecting class declarations (e.g., class MyClass)
    class_pattern = re.compile(r'^\s*(public|private|protected|internal|protected\s+internal)?\s*class\s+(\w+)')
    
    # Regular expression for detecting method declarations
    method_pattern = re.compile(r'^\s*(public|private|protected|internal|protected\s+internal)?\s*(async\s+)?\s*(\w+\s+)?(\w+)\s+(\w+)\s*\((.*?)\)\s*{')

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        for line in lines:
            # Match class declarations
            class_match = class_pattern.match(line)
            if class_match:
                classes.append(class_match.group(2))  # Capture class name

            # Match method declarations (including async methods)
            method_match = method_pattern.match(line)
            if method_match:
                methods.append(method_match.group(5))  # Capture method name

    except Exception as e:
        print(f"Error reading file: {e}")

    # Return both classes and methods
    return classes, methods

def handle_file(path):
    try:
        classes, methods = extract_csharp_structure(path)
        output = []

        if classes:
            output.append("Classes:")
            for cls in classes:
                output.append(f"  - {cls}")

        if methods:
            output.append("Methods:")
            for method in methods:
                output.append(f"  - {method}")

        return "\n".join(output)
    
    except ValueError as e:
        return f"Error: {e}"


def extract_go_structure(file_path):
    """Extract functions from a Go file."""
    functions = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            func_match = re.match(r"^\s*func\s+(\w+)\s*\(.*\)", line)
            if func_match:
                functions.append(func_match.group(1))
    return [], functions  # Go does not have classes

def extract_java_structure(file_path):
    """Extract classes and methods from a Java file."""
    classes, methods = [], []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            class_match = re.match(r"^\s*class\s+(\w+)", line)
            if class_match:
                classes.append(class_match.group(1))
            method_match = re.match(r"^\s*(public|private|protected)?\s*(\w+\s+)+(\w+)\s*\(.*\)", line)
            if method_match:
                methods.append(method_match.group(3))
    return classes, methods

def extract_js_structure(file_path):
    """Extract functions from a JavaScript file."""
    functions = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            func_match = re.match(r"^\s*function\s+(\w+)\s*\(.*\)", line)
            if func_match:
                functions.append(func_match.group(1))
            arrow_func_match = re.match(r"^\s*(?:const|let|var)\s+(\w+)\s*=\s*\(?.*\)?\s*=>", line)
            if arrow_func_match:
                functions.append(arrow_func_match.group(1))
    return [], functions  # JavaScript does not have classes in the same way

def extract_typescript_structure(file_path):
    """Extract classes, functions, and methods from a TypeScript file."""
    classes, functions = [], []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            # Match class definitions
            class_match = re.match(r"^\s*class\s+(\w+)", line)
            if class_match:
                classes.append(class_match.group(1))
            # Match standalone functions
            func_match = re.match(r"^\s*function\s+(\w+)\s*\(.*\)", line)
            if func_match:
                functions.append(func_match.group(1))
            # Match arrow functions (e.g., `const name = (args) => { ... }`)
            arrow_func_match = re.match(r"^\s*(?:const|let|var)\s+(\w+)\s*=\s*\(?.*\)?\s*=>", line)
            if arrow_func_match:
                functions.append(arrow_func_match.group(1))
            # Match methods within classes
            method_match = re.match(r"^\s*(public|private|protected|static)?\s*(\w+)\s*\(.*\)", line)
            if method_match and classes:
                functions.append(method_match.group(2))
    return classes, functions

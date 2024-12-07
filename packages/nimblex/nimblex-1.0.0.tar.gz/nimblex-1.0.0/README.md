
# Nimblex

**Nimblex** is a Python CLI tool designed to analyze, extract, and display the structure of directories and Python projects. With Nimblex, you can view directory hierarchies, extract classes and methods, and save the results to files—all with a simple command-line interface.

---

## Features

- **Display Directory Structures**: Quickly view the hierarchy of files and folders in any directory.
- **Extract Python Classes and Methods**: Parse Python files to identify and display classes and methods.
- **Save Results**: Export directory structures and extracted information to files for documentation or sharing.
- **Customizable Ignored Directories**: Automatically exclude unnecessary directories like `__pycache__` and `.git`.

---

## Installation

You can install Nimblex directly from PyPI:

```bash
pip install nimblex
```


## Features

- **Display Directory Structures**: Quickly view the hierarchy of files and folders in any directory.
- **Extract Python Classes and Methods**: Parse Python files to identify and display classes and methods.
- **Save Results**: Export directory structures and extracted information to files for documentation or sharing.
- **Customizable Ignored Directories**: Automatically exclude unnecessary directories like `__pycache__` and `.git`.

---

## Installation

You can install Nimblex directly from PyPI:

```bash
pip install nimblex
```


## Usage

Run the `nimblex` command from your terminal. If no path is specified, the tool operates on the current directory by default.

### Commands and Options
|Command/Option  |Description  |	 
|--|--|
| ‍‍`nimblex -m` | Save the structure of a single directory or file to a file. |
|`nimblex -x`|Extract the directory structure and classes/methods for an entire project and save to a file.|
|`nimblex -d`  | Display the directory structure and classes/methods for an entire project directly in the terminal. |

### Examples

#### Display the directory structure in the terminal:
```bash
nimblex -d
```
Extract and save the project structure to a file:
```bash
nimblex -x /path/to/your/project
```
Save the structure of a single directory:
```bash
nimblex -m /path/to/directory
```
## Configuration

### Ignored Directories and Files

By default, Nimblex excludes the following directories and files during analysis:

-   `__pycache__`
-   `.git`
-   `.svn`
-   `.hg`
-   `.idea`
-   `node_modules`
-   `bin`, `obj`
-   `dist`, `build`
-   `.vscode`
-   `*.egg-info`
-   `target`
-   `venv`

Other items may be added to this list in future updates.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

----------

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/pezhvak98/Nimblex/blob/main/LICENSE) file for more details.
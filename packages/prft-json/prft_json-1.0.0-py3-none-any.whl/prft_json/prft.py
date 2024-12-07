import os
import re
import json
import argparse


def natural_sort_key(name):
    return [int(text) if text.isdigit() else text for text in re.split(r'(\d+)', name)]


def load_gitignore_patterns(root_path) -> dict[str, list]:
    """
    Loads patterns from a .gitignore file in the given directory.

    Args:
        root_path (str): Path to the root directory containing the .gitignore file.

    Returns:
        dict: A dictionary with "dirs" and "files" as keys containing directory and file patterns respectively.
    """
    patterns = {"dirs": [],
                "files": []}
    gitignore_path = os.path.join(root_path, ".gitignore")
    try:
        with open(gitignore_path, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return patterns
    
    raw = [line.strip() for line in lines if line.strip() and not line.startswith("#")]
    for element in raw:
        if element.endswith("/"):
            element = element.replace('/', '')
            patterns["dirs"].append(element)
        else:
            element = element.replace('*', '')
            patterns["files"].append(element)

    return patterns


def dirs_match(name: str, dir_patterns: list[str]) -> bool:
    """
    Checks if a directory name matches any pattern in the provided list.

    Args:
        name (str): The name of the directory.
        dir_patterns (list[str]): List of directory patterns.

    Returns:
        bool: True if the name matches any pattern, False otherwise.
    """
    for pattern in dir_patterns:
        if "*" in pattern:
            pattern = pattern.replace('*', '')
            if name.endswith(pattern):
                return True
    return name in dir_patterns


def match_ignore(root_path, patterns, name: str) -> bool:
    """
    Determines if a file or directory should be ignored based on patterns.

    Args:
        root_path (str): The root directory path.
        patterns (dict): A dictionary containing "dirs" and "files" patterns.
        name (str): Name of the file or directory.

    Returns:
        bool: True if the name matches any pattern and should be ignored, False otherwise.
    """
    if os.path.isdir(os.path.join(root_path, name)):
        res = dirs_match(name, patterns['dirs'])
        return res
    else:
        return any(name.endswith(pattern) for pattern in patterns["files"])


def build_file_tree(dir_name: str, ignore_dot=True, ignore=True, gitignore_spec=None) -> list:
    """
    Recursively builds a file tree structure for a given directory.

    Args:
        dir_name (str): Path to the root directory.
        ignore_dot (bool): Whether to ignore hidden files and directories (starting with '.').
        ignore (bool): Whether to ignore files and directories based on gitignore_spec.
        gitignore_spec (dict): Gitignore patterns to filter files and directories.

    Returns:
        list: A list representing the directory structure with nested dictionaries for subdirectories.
    """
    items = os.listdir(dir_name)
    directories = sorted([name for name in items if os.path.isdir(os.path.join(dir_name, name))], key=natural_sort_key)
    files = sorted([name for name in items if os.path.isfile(os.path.join(dir_name, name))], key=natural_sort_key)

    tree = []

    for name in directories:
        if ignore_dot and name.startswith(".") and name not in ['.gitignore', '.dockerignore', '.env']:
            continue

        path = os.path.join(dir_name, name)

        if ignore and gitignore_spec and match_ignore(dir_name, gitignore_spec, name):
            continue

        tree.append({name: build_file_tree(path, ignore_dot, ignore, gitignore_spec)})

    tree.extend(files)
    return tree


def generate_json(dir_name: str, f_name: str, ignore_dot=True, ignore=True, gitignore_spec=None) -> None:
    """
    Generates a JSON file representing the file tree of a directory.

    Args:
        dir_name (str): Path to the root directory.
        f_name (str): Name of the output JSON file (without extension).
        ignore_dot (bool): Whether to ignore hidden files and directories.
        ignore (bool): Whether to ignore files and directories based on gitignore_spec.
        gitignore_spec (dict): Gitignore patterns to filter files and directories.
    """
    tree = build_file_tree(dir_name, ignore_dot, ignore, gitignore_spec)
    with open(f"{f_name}.json", 'w', encoding='utf-8') as f:
        json.dump(tree, f, ensure_ascii=False, indent=4)


def main() -> None:
    """
    Parses command-line arguments and generates a JSON file tree.

    Command-line options:
        - root_path: The root directory of the project (default: current directory).
        - --no-ignore: Disable ignoring files based on .gitignore.
        - --no-dot: Include dotfiles (hidden files) in the file tree.
        - --output-name: Name of the output JSON file (default: 'result').
    """
    parser = argparse.ArgumentParser(description="Generate a file tree structure of a project.")
    parser.add_argument("root_path", nargs="?", default=".", help="Root directory of the project (default: current directory)")
    parser.add_argument("--no-ignore", action="store_false", help="Do not ignore files from .gitignore")
    parser.add_argument("--no-dot", action="store_false", help="Do not ignore dotfiles (hidden files)")
    parser.add_argument("--output-name", default="result", help="Set output filename")

    args = parser.parse_args()

    root_path = os.path.abspath(args.root_path)
    gitignore_spec = load_gitignore_patterns(root_path) if args.no_ignore else None
    f_name = args.output_name

    generate_json(root_path, f_name, ignore_dot=args.no_dot, ignore=args.no_ignore, gitignore_spec=gitignore_spec)


if __name__ == "__main__":
    main()

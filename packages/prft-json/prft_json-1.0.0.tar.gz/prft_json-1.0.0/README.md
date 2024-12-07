# Project File Tree JSON (prft-json)
Modified version of the [prft](https://github.com/Trum-ok/project-file-tree) for use primarily in the RAG LLM.

## Installation
Install prft-json via pip:
```bash
pip install prft-json
```

## Usage
Use prft in the terminal to display a project’s file structure.

**Basic Command**
```bash
prft-json path_to_project
```

You can also use . to specify the current directory if you are in the project directory:

```bash
prft-json .
```

## Options
- **--no-ignore** Include files and directories that would otherwise be ignored based on patterns in .gitignore. By default, files and directories matching .gitignore patterns are excluded.
- **--no-dot** Include hidden files and directories (those starting with a dot .). By default, dotfiles and dotfolders are excluded unless explicitly listed in the .gitignore file.
- **--prefix** `<string>` Specify a prefix for the tree structure output. This option is primarily for visual representation and formatting purposes. The default is a single space (' ').
- **--output-name** `<filename>` Specify the name of the output JSON file. The default filename is result.json. You do not need to include the .json extension, as it will be added automatically.


**Example:**
```bash
prft-json path_to_project --no-ignore --no-dot
```

### Example Output
```json
[
    {
        "prft_json": [
            "__init__.py",
            "prft.py"
        ]
    },
    ".gitignore",
    "LICENSE",
    "README.md",
    "pyproject.toml"
]
```


## License

This project is licensed under the MIT License.

## Author

Created by [trum-ok](https://github.com/Trum-ok) :p

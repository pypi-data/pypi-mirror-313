# My-Exporter

**A Python tool to export the contents of a folder into a single text file while respecting `.gitignore` patterns and maintaining the hierarchical structure.**

## Table of Contents

- [My-Exporter](#my-exporter)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Command-Line Interface](#command-line-interface)
    - [Programmatic Usage](#programmatic-usage)
  - [Configuration](#configuration)
  - [Contributing](#contributing)
  - [License](#license)
  - [Contact](#contact)

## Features

- **Respect `.gitignore` Patterns:** Automatically excludes files and directories based on your `.gitignore` file.
- **Hierarchical Structure:** Maintains the folder hierarchy in the output by using relative file paths as headers.
- **Customizable Output:** Specify the root directory, output file name, and ignore file.
- **Handles Non-Text Files:** Gracefully handles non-text or unreadable files by indicating their presence without content.

## Installation

You can install `my-exporter` via [PyPI](https://pypi.org/) using `pip`:

```bash
pip install my-exporter
```

Alternatively, you can install it directly from the source:

```bash
git clone https://github.com/RK0429/my-exporter.git
cd my-exporter
pip install .
```

## Usage

### Command-Line Interface

After installation, you can use the `my-exporter` CLI tool to export your folder contents.

**Basic Usage:**

```bash
my-exporter --root-dir path/to/project --output-file exported.txt
```

**Options:**

- `--root-dir`: Specifies the root directory to start exporting from. Defaults to the current directory (`.`).
- `--output-file`: Defines the name of the output text file. Defaults to `output.txt`.
- `--ignore-file`: Specifies a custom ignore file. Defaults to `.gitignore`.

**Example:**

```bash
my-exporter --root-dir ./my_project --output-file project_contents.txt
```

### Programmatic Usage

You can also use `my-exporter` as a library within your Python projects.

**Example:**

```python
from my_exporter import export_folder_contents

export_folder_contents(
    root_dir='path/to/project',
    output_file='exported_contents.txt',
    ignore_file='.gitignore'
)
```

## Configuration

- **`.gitignore` Support:** The tool uses your `.gitignore` file to determine which files and directories to exclude. Ensure that your `.gitignore` is properly configured in the root directory you are exporting.

- **Custom Ignore Files:** If you prefer to use a different ignore file, specify it using the `--ignore-file` option.

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Repository:** Click the "Fork" button on the repository page.
2. **Create a Feature Branch:**  

   ```bash
   git checkout -b feature/my-new-feature
   ```

3. **Commit Your Changes:**  

   ```bash
   git commit -m "Add some feature"
   ```

4. **Push to the Branch:**  

   ```bash
   git push origin feature/my-new-feature
   ```

5. **Open a Pull Request:** Describe your changes and submit the pull request.

Please make sure to update tests as appropriate and adhere to the [PEP 8](https://pep8.org/) style guide.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

**Your Name**  
Email: [s.woods.m.29@gmail.com](mailto:s.woods.m.29@gmail.com)  
GitHub: [https://github.com/RK0429](https://github.com/RK0429)

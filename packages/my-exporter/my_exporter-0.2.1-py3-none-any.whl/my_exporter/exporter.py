import os
from .ignore_handler import load_ignore_patterns


def print_structure(root_dir='.', out=None, prefix='', spec=None):
    """
    Recursively print a "tree" structure of directories and files.
    This function filters out ignored files/directories using the spec.
    """
    entries = sorted(os.listdir(root_dir))
    # Filter out ignored entries
    entries = [
        e for e in entries
        if not spec.match_file(os.path.join(root_dir, e))
    ]

    for i, entry in enumerate(entries):
        path = os.path.join(root_dir, entry)
        # Choose the connector symbol based on position
        connector = '├── ' if i < len(entries)-1 else '└── '

        # Write directory or file name
        out.write(prefix + connector + entry + "\n")

        if os.path.isdir(path):
            # Update prefix for child entries
            if i < len(entries)-1:
                new_prefix = prefix + "│   "
            else:
                new_prefix = prefix + "    "
            print_structure(path, out=out, prefix=new_prefix, spec=spec)


def export_folder_contents(
    root_dir='.',
    output_file='output.txt',
    ignore_file='.gitignore'
):
    spec = load_ignore_patterns(ignore_file)

    with open(output_file, 'w', encoding='utf-8', errors='replace') as out:
        # Print the directory structure header
        out.write("================\n")
        out.write("DIRECTORY STRUCTURE\n")
        out.write("================\n\n")

        # Print the directory structure
        print_structure(root_dir, out=out, spec=spec)

        out.write("\n")

        # Print the file contents header
        out.write("================\n")
        out.write("FILE CONTENTS\n")
        out.write("================\n\n")

        # Now, write the file contents
        for root, dirs, files in os.walk(root_dir):
            # Filter directories according to .gitignore spec
            dirs[:] = [d for d in dirs if not spec.match_file(os.path.join(root, d))]

            for filename in files:
                filepath = os.path.join(root, filename)
                if spec.match_file(filepath):
                    continue
                relpath = os.path.relpath(filepath, start=root_dir)

                # Print the file path with '===' on both sides
                out.write(f"==={relpath}===\n")

                # Write the file content
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                        out.write(f.read())
                except Exception:
                    out.write("[Non-text or unreadable content]")
                out.write("\n\n")

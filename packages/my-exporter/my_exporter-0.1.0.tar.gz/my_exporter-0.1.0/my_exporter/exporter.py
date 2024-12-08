import os
from .ignore_handler import load_ignore_patterns


def export_folder_contents(
    root_dir='.',
    output_file='output.txt',
    ignore_file='.gitignore'
):
    spec = load_ignore_patterns(ignore_file)
    with open(output_file, 'w', encoding='utf-8', errors='replace') as out:
        for root, dirs, files in os.walk(root_dir):
            # Filter directories
            dirs[:] = [d for d in dirs if not spec.match_file(os.path.join(root, d))]
            for filename in files:
                filepath = os.path.join(root, filename)
                if spec.match_file(filepath):
                    continue
                relpath = os.path.relpath(filepath, start=root_dir)
                out.write(f"### {relpath}\n")
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                        out.write(f.read())
                except Exception:
                    out.write("[Non-text or unreadable content]")
                out.write("\n\n")

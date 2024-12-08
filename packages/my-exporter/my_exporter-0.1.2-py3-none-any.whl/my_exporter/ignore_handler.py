from pathspec import PathSpec


def load_ignore_patterns(ignore_file: str = '.gitignore'):
    with open(ignore_file, 'r') as f:
        lines = f.read().splitlines()
    spec = PathSpec.from_lines('gitwildmatch', lines)
    return spec

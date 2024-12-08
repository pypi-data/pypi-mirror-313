import argparse
from .exporter import export_folder_contents


def main():
    parser = argparse.ArgumentParser(description='Export folder contents.')
    parser.add_argument('--root-dir', default='.', help='Root directory to start from')
    parser.add_argument('--output-file', default='output.txt', help='Output file name')
    parser.add_argument('--ignore-file', default='.gitignore', help='Ignore file pattern list')
    args = parser.parse_args()

    export_folder_contents(
        root_dir=args.root_dir,
        output_file=args.output_file,
        ignore_file=args.ignore_file
    )

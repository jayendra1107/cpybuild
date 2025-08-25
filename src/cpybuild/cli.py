
import argparse
import importlib.metadata
from .core import run_task

def main():
    import os
    parser = argparse.ArgumentParser(prog='cpybuild', description='Python-to-C build tool')
    parser.add_argument('--version', action='version', version=f'cpybuild {importlib.metadata.version("cpybuild")}')
    parser.add_argument('command', nargs='?', choices=['init', 'build', 'clean', 'test'], help='Command to run')
    args = parser.parse_args()
    # Ensure we are in the project root (where cpybuild.yaml exists), except for init
    if args.command and args.command != 'init' and not os.path.exists('cpybuild.yaml'):
        print('Error: cpybuild.yaml not found. Please run this command from your project root directory.')
        exit(1)
    if args.command:
        run_task(args.command)

if __name__ == '__main__':
    main()

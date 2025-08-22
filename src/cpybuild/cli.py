import argparse
from .core import run_task

def main():
    import os
    parser = argparse.ArgumentParser(prog='cpybuild', description='Python-to-C build tool')
    parser.add_argument('command', choices=['init', 'build', 'clean', 'test'], help='Command to run')
    args = parser.parse_args()
    # Ensure we are in the project root (where cpybuild.yaml exists), except for init
    if args.command != 'init' and not os.path.exists('cpybuild.yaml'):
        print('Error: cpybuild.yaml not found. Please run this command from your project root directory.')
        exit(1)
    run_task(args.command)

if __name__ == '__main__':
    main()

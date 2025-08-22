import shutil
import os

def run():
    print('Cleaning build artifacts...')
    if os.path.exists('build'):
        shutil.rmtree('build')
        print('Removed build directory.')
    else:
        print('No build directory found.')

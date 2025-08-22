import os
import sys
from .tasks import build, clean, init, test

def run_task(task_name):
    if task_name == 'build':
        build.run()
    elif task_name == 'clean':
        clean.run()
    elif task_name == 'init':
        init.run()
    elif task_name == 'test':
        test.run()
    else:
        print(f'Unknown task: {task_name}')
        sys.exit(1)

def run():
    import os
    import glob
    print('Initializing cpybuild project...')
    config = 'sources:\n  - src/**/*.py\noutput: build/'
    with open('cpybuild.yaml', 'w') as f:
        f.write(config)
    print('Created cpybuild.yaml')

    # Add __init__.py to all package directories under src/
    for dirpath, dirnames, filenames in os.walk('src'):
        if any(fname.endswith('.py') for fname in filenames):
            init_path = os.path.join(dirpath, '__init__.py')
            if not os.path.exists(init_path):
                with open(init_path, 'w') as f:
                    f.write('# Automatically created by cpybuild init\n')
                print(f'Added {init_path}')

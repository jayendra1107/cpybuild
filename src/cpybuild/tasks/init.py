def run():
    print('Initializing cpybuild project...')
    config = 'sources:\n  - src/**/*.py\noutput: build/'
    with open('cpybuild.yaml', 'w') as f:
        f.write(config)
    print('Created cpybuild.yaml')

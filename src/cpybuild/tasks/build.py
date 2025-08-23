def run() -> None:
    """
    Build task: Transpile Python files to C using Cython and setuptools.
    Collects all source files, creates Extension objects, and calls cythonize once.
    """
    import yaml
    import glob
    import os
    from Cython.Build import cythonize
    from setuptools import Extension

    print('Building project (Python to C)...')
    # Load config
    with open('cpybuild.yaml') as f:
        config = yaml.safe_load(f)
    sources: list[str] = []
    for pattern in config.get('sources', []):
        sources.extend(glob.glob(pattern, recursive=True))
    import sys
    output_dir: str = os.environ.get('CPYBUILD_LOC', config.get('output', 'build/'))
    os.makedirs(output_dir, exist_ok=True)
    # Always add output_dir to sys.path and PYTHONPATH for importing built modules
    if output_dir not in sys.path:
        sys.path.insert(0, output_dir)
    # Set PYTHONPATH for subprocesses and user shells
    os.environ['PYTHONPATH'] = output_dir + (':' + os.environ['PYTHONPATH'] if 'PYTHONPATH' in os.environ else '')

    extensions: list[Extension] = []
    for src in sources:
        print(f'Transpiling {src}...')
        module_name = os.path.splitext(os.path.relpath(src, start="src").replace(os.sep, "."))[0]
        extensions.append(Extension(
            name=module_name,
            sources=[src],
        ))

    import yaml
    import glob
    import os
    import sys
    from Cython.Build import cythonize
    from setuptools import Extension, setup
    import shutil
    import tempfile

    print('Building project (Python to C and shared libraries)...')
    # Load config
    with open('cpybuild.yaml') as f:
        config = yaml.safe_load(f)
    sources: list[str] = []
    for pattern in config.get('sources', []):
        sources.extend(glob.glob(pattern, recursive=True))
    output_dir: str = os.environ.get('CPYBUILD_LOC', config.get('output', 'build/'))
    os.makedirs(output_dir, exist_ok=True)
    # Add output_dir to sys.path for importing built modules
    if output_dir not in sys.path:
        sys.path.insert(0, output_dir)

    extensions: list[Extension] = []
    for src in sources:
        print(f'Transpiling {src}...')
        module_name = os.path.splitext(os.path.relpath(src, start="src").replace(os.sep, "."))[0]
        extensions.append(Extension(
            name=module_name,
            sources=[src],
        ))

    if extensions:
        # Use a temporary directory for setuptools build
        with tempfile.TemporaryDirectory() as build_temp:
            setup(
                script_args=["build_ext", f"--build-lib={output_dir}", f"--build-temp={build_temp}"],
                ext_modules=cythonize(
                    extensions,
                    compiler_directives={'language_level': 3},
                    build_dir=output_dir,
                    annotate=False
                ),
                script_name='setup.py',
                name="cpybuild-temp-build",
                version="0.0.0",
            )
        print(f'All sources compiled to shared libraries in {output_dir}')
    else:
        print('No source files found to transpile.')

import yaml
import glob
import os
from Cython.Build import cythonize
from setuptools import Extension, setup
import sys
import re
import tempfile

__all__ = ["run", "is_valid_identifier", "check_module_parts"]

def is_valid_identifier(s: str) -> bool:
    return re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', s) is not None

def check_module_parts(parts):
    invalids = []
    for part in parts:
        if not is_valid_identifier(part):
            invalids.append(part)
    return invalids

def run() -> None:
    """
    Build task: Transpile Python files to C using Cython and setuptools.
    Collects all source files, creates Extension objects, and calls cythonize once.
    """
    print('Building project (Python to C)...')
    # Load config with error handling
    if not os.path.exists('cpybuild.yaml'):
        print('ERROR: cpybuild.yaml not found. Please run this command from your project root directory.')
        return
    try:
        with open('cpybuild.yaml') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        print(f'ERROR: Failed to read cpybuild.yaml: {e}')
        return

    sources: list[str] = []
    for pattern in config.get('sources', []):
        matched = glob.glob(pattern, recursive=True)
        if not matched:
            print(f'WARNING: No files matched pattern: {pattern}')
        sources.extend(matched)

    output_dir: str = os.environ.get('CPYBUILD_LOC', config.get('output', 'build/'))
    try:
        os.makedirs(output_dir, exist_ok=True)
    except Exception as e:
        print(f'ERROR: Could not create output directory {output_dir}: {e}')
        return

    # Always add the parent of output_dir to sys.path for importing built modules
    parent_dir = os.path.abspath(os.path.join(output_dir, os.pardir))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)

    extensions = []
    skipped_files = []

    for src in sources:
        # Derive module name from file path
        rel_path = os.path.relpath(src).replace(os.sep, "/")
        if rel_path.endswith(".py"):
            rel_path = rel_path[:-3]
        parts = rel_path.split("/")
        invalids = check_module_parts(parts)
        if invalids:
            skipped_files.append((src, invalids))
            continue
        module_name = ".".join(parts)
        extensions.append(
            Extension(
                module_name,
                [src],
            )
        )

    if skipped_files:
        print("\nERROR: The following files were skipped due to invalid module/package names:")
        for src, invalids in skipped_files:
            print(f"  - {src}")
            for part in invalids:
                print(f"    Invalid part: '{part}' (must use only letters, numbers, and underscores, and not start with a digit)")
        print("\nPlease rename these files/folders to valid Python identifiers.")

    if extensions:
        try:
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
        except Exception as e:
            print(f'ERROR: Build failed: {e}')
    else:
        print('No source files found to transpile.')
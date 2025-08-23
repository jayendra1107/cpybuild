# cpybuild

**cpybuild** is a Python build tool that transpiles Python code to C using Cython, inspired by tools like Maven and Gulp but designed for Python projects. It automates the build, clean, and test workflow for Python-to-C projects and can be installed as a pip package with a simple CLI.

## Features
- Transpile Python code to C using Cython
- Simple CLI: `cpybuild [init|build|clean|test]`
- Configurable build output location via `CPYBUILD_LOC` environment variable
- Ensures commands are run from the project root
- Easily extensible for custom tasks

## Installation

```sh
pip install cpybuild
```

## Quick Start

1. **Initialize your project:**
	```sh
	cpybuild init
	```
	This creates a `cpybuild.yaml` config file.

2. **Build your project:**
	```sh
	cpybuild build
	```
	This transpiles Python files (as configured in `cpybuild.yaml`) to C in the build directory.

3. **Clean build artifacts:**
	```sh
	cpybuild clean
	```

4. **Run tests:**
	```sh
	cpybuild test
	```

## Configuration

Edit `cpybuild.yaml` to specify source files and output directory:

```yaml
sources:
  - src/**/*.py
output: build/
```

## Environment Variable

Set `CPYBUILD_LOC` to override the build output directory:

```sh
export CPYBUILD_LOC=/custom/build/dir
cpybuild build
```

## License

MIT

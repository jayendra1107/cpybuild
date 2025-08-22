from setuptools import setup, find_packages

setup(
    name="cpybuild",
    version="0.1.0",
    description="A Python build tool to transpile Python code to C using Cython.",
    author="jayendra1107",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pyyaml",
        "cython",
        "setuptools",
        "wheel"
    ],
    entry_points={
        "console_scripts": [
            "cpybuild=cpybuild.cli:main"
        ]
    },
    include_package_data=True,
    python_requires=">=3.7",
)

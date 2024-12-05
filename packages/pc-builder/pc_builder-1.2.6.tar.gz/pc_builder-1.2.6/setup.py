from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pc-builder",
    version="1.2.6",
    description="A CLI application for building and managing PC configurations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="PC Builders Team",
    url="https://github.com/mif-it-se-2024/group-project-pc-builders",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "typer",  # Core CLI framework
    ],
    extras_require={
        "dev": [
            "tox",  # For testing automation
            "pytest",  # For testing purposes
            "pyinstaller",  # For building executables
        ],
    },
    entry_points={
        "console_scripts": [
            "pcbuilder=pc_builder.cli:main",  # Your CLI entry point
        ],
    },
)

"""This submodule provides a command-line interface for the package.
"""

import argparse
import tomllib
import importlib.resources as pkg_resources

# using importlib.resources to load package data
with pkg_resources.open_binary("your_package_name", "pyproject.toml") as f:
    data = tomllib.load(f)


def main():
    parser = argparse.ArgumentParser(description=f"PyOVO: {data["project"]["description"]}")

    parser.add_argument("-v", "--version", action="store_true", help="display the version information")

    # analyze the arguments
    args = parser.parse_args()

    if args.version:
        print(f"current verison: {data["project"]["version"]}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

"""This submodule provides a command-line interface for the package.
"""

import argparse
import tomllib
from pathlib import Path

conf_path = Path(__file__).parents[2] / "pyproject.toml"

with open(conf_path, "rb") as f:
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

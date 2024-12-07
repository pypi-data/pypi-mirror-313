"""This submodule provides a command-line interface for the package.
"""

import argparse
import importlib.metadata

dist = importlib.metadata.distribution("pyovo")


def main():
    parser = argparse.ArgumentParser(description=f"PyOVO: {dist.metadata['summary']}")

    parser.add_argument(
        "-v", "--version", action="store_true", help="display the version information"
    )

    # analyze the arguments
    args = parser.parse_args()

    if args.version:
        print(f"current verison: {dist.metadata['version']}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

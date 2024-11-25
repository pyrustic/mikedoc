import os
import sys
from mikedoc.cli import Cli


__all__ = []


def main():
    cli = Cli(os.getcwd())
    cli.run(*sys.argv[1:])


if __name__ == "__main__":
    main()

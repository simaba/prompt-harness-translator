from __future__ import annotations

import argparse
from .core import translate_file


def main() -> int:
    parser = argparse.ArgumentParser(prog="prompt-harness")
    sub = parser.add_subparsers(dest="command")

    tr = sub.add_parser("translate")
    tr.add_argument("path")
    tr.add_argument("--target", required=True)

    args = parser.parse_args()

    if args.command == "translate":
        print(translate_file(args.path, args.target))
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

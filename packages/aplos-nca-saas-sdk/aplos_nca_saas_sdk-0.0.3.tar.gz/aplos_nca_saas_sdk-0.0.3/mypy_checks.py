"""
Run ``mypy``, ignoring relevant errors.
"""

import subprocess
import sys


def main() -> None:
    """Main entry point to run the mypy checks with some specific ignores"""
    args = ["mypy", "--check-untyped-defs", "./src"]
    ignore_paths = []
    result = subprocess.run(args=args, stdout=subprocess.PIPE, check=False)
    result_lines = result.stdout.decode().strip().split("\n")
    error_lines = [
        line
        for line in result_lines
        if not any(line.startswith(path) for path in ignore_paths)
    ]
    print("\n".join(error_lines))
    sys.exit(int(bool(error_lines)))


if __name__ == "__main__":
    main()

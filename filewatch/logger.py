import sys

RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RESET = "\033[0m"


def error(message):
    print(f"{RED}{message}{RESET}", file=sys.stderr)


def warning(message):
    print(f"{YELLOW}{message}{RESET}", file=sys.stderr)


def info(message):
    print(f"{message}", file=sys.stderr)


def success(message):
    print(f"{GREEN}{message}{RESET}", file=sys.stderr)

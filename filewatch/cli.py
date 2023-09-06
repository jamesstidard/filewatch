"""\
filewatch

Usage:
    filewatch <path>... -- <command>...

Options:
    -h --help       Show this message
    -v --version    Print current version
"""
import os
import sys
import time
import pathlib
import datetime
import subprocess

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


__version__ = "0.0.1"


CLEAR = "clr" if sys.platform.startswith("win") else "clear"


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


class EventHandler(FileSystemEventHandler):
    def __init__(self, cmd):
        self.process = None
        self.cmd = list(cmd)
        self.run()  # run on start, before changes start

    def run(self):
        os.system(CLEAR)
        success(datetime.datetime.now())

        # no command given to run
        if len(self.cmd) == 0:
            return

        # cancel running process and start again
        if self.process:
            self.process.kill()

        try:
            self.process = subprocess.Popen(
                self.cmd,
                stdout=sys.stdout,
                stderr=sys.stderr,
            )
        except FileNotFoundError:
            error(f"Unknown command: {self.cmd[0]}")

    def on_any_event(self, event):
        self.run()


def split_list(predicate, iterable):
    group = []
    for i in iterable:
        if predicate(i):
            yield group
            group = []
            continue

        group.append(i)

    yield group


def main():
    if len(sys.argv) == 2 and sys.argv[1] in {"-h", "--help"}:
        print(__doc__)
        sys.exit(0)

    if len(sys.argv) == 2 and sys.argv[1] in {"-v", "--version"}:
        print(__version__)
        sys.exit(0)

    try:
        paths, command = split_list(lambda i: i == "--", sys.argv[1:])
    except ValueError:
        info(__doc__)
        sys.exit(1)

    event_handler = EventHandler(command)
    observer = Observer()

    for p in paths:
        p = pathlib.Path(p)

        if not p.exists():
            error(f"file/directory does not exist: {p}")
            sys.exit(1)

        observer.schedule(event_handler, p, recursive=True)

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == "__main__":
    main()

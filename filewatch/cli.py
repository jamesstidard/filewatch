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

from filewatch import logger, utils
from filewatch.__version__ import __version__

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


CLEAR = "clr" if sys.platform.startswith("win") else "clear"


class EventHandler(FileSystemEventHandler):
    def __init__(self, cmd):
        self.process = None
        self.cmd = list(cmd)
        self.run()  # run on start, before changes start

    def run(self):
        os.system(CLEAR)
        logger.success(datetime.datetime.now())

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
            logger.error(f"Unknown command: {self.cmd[0]}")

    def on_any_event(self, event):
        self.run()


def main():
    args = sys.argv[1:]

    if len(args) == 1 and args[0] in {"-h", "--help"}:
        print(__doc__)
        sys.exit(0)

    if len(args) == 1 and args[0] in {"-v", "--version"}:
        print(__version__)
        sys.exit(0)

    try:
        paths, command = utils.split_iterable(lambda i: i == "--", args)
    except ValueError:
        logger.info(__doc__)
        sys.exit(1)

    event_handler = EventHandler(command)
    observer = Observer()

    for p in paths:
        p = pathlib.Path(p)

        if not p.exists():
            logger.error(f"file/directory does not exist: {p}")
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

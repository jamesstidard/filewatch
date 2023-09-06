# filewatch
A cli utility to watch files or directories and run a command on any changes.

```
filewatch

Usage:
    filewatch <path>... -- <command>...

Options:
    -h --help       Show this message
    -v --version    Print current version
```

## Usage Examples
```console
# Watch python file in current directory and rerun on changes.
$ filewatch main.py -- python main.py
```

```console
# Watch folder and announce change over speakers (macOS)
$ filewatch /path/to/some/folder -- say "folder changed"
```

```console
# Watch multiple folders / files and announce change over speakers (macOS)
$ filewatch /path/to/some/folder main.py some/other/path -- echo "changed"
```

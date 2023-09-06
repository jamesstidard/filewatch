import re
import sys
import pathlib
import subprocess

from filewatch.utils import logger

HERE = pathlib.Path(__file__)
PYPROJECT_FP = HERE.parent.parent / "pyproject.toml"
__VERSION__FP = HERE.parent.parent / "filewatch" / "__version__.py"

VERSION_RE = re.compile(r"^v?(\d+).(\d+).(\d+)$")


def fmt_version(version, prefix):
    if prefix in (None, False):
        prefix = ""
    elif prefix is True:
        prefix = "v"
    x, y, z = version
    return f"{prefix}{x}.{y}.{z}"


def version(match_):
    return tuple(map(int, match_.group(1, 2, 3)))


try:
    input_ = sys.argv[1]
except IndexError:
    match_ = None
else:
    match_ = VERSION_RE.match(input_)

while not match_:
    input_ = input("version number: ")
    match_ = VERSION_RE.match(input_)


current_version = version(match_)

_ = subprocess.run(["git", "fetch", "--tags"], check=True)
p = subprocess.run(["git", "tag", "--list"], check=True, capture_output=True)

previous_versions = {
    version(m)
    for tag in p.stdout.decode().splitlines()
    if (m := VERSION_RE.match(tag))
}

if current_version in previous_versions:
    logger.error(f"{fmt_version(current_version, prefix=None)} already used")

if previous_versions:
    latest = sorted(previous_versions)[-1]
    if current_version <= latest:
        logger.error(f"version need to be greater then last release: {latest}")


def update_file(fp, pattern, replacement):
    with open(fp, "r") as fp_:
        content = fp_.read()

    if not list(re.findall(pattern, content)):
        logger.error("unable to find pattern, maybe the format has changed?")

    content = re.sub(pattern, replacement, content)

    with open(fp, "w+") as fp_:
        fp_.write(content)


previous = r'version\s*=\s*\"\d+.\d+.\d+\"'
replacement = f'version = "{fmt_version(current_version, prefix=None)}"'
update_file(PYPROJECT_FP, previous, replacement)

previous = r'VERSION\s*=\s*\(\d+,\s*\d+,\s*\d+\,?\)'
x, y, z = current_version
replacement = f'VERSION = ({x}, {y}, {z})'
update_file(__VERSION__FP, previous, replacement)

tag = fmt_version(current_version, prefix="v")

_ = subprocess.run(["git", "commit", "-am", tag], check=True)
_ = subprocess.run(["git", "push"], check=True)

_ = subprocess.run(["git", "tag", tag], check=True)
_ = subprocess.run(["git", "push", "origin", tag], check=True)

logger.success(f"{tag} released!")

import os
import sys
from subprocess import check_output, DEVNULL, CalledProcessError
from pathlib import Path

project_root_dir = Path(__file__).parent.parent

# add project root directory to path in order to import from VERSION.py if needed
path = set(sys.path)
path.add(str(project_root_dir))
sys.path = list(path)

# noinspection PyBroadException
try:
    print("Setting __version__ value in VERSION.py with package version from git tag...")
    git_version = check_output(
        ["git", "describe", "--tag", "--abbrev=0"],
        stderr=DEVNULL
    ).decode("utf-8").strip()
    pypi_version = git_version[1:]

    with open(Path(__file__).parent.parent / "VERSION.py", "w") as vf:
        vf.write(
            f"# DO NOT EDIT - VERSIONING CONTROLLED BY GIT TAGS{os.linesep}"
            f"__version__ = \"{git_version[1:]}\"{os.linesep}"
        )
    print("...updated VERSION.py with latest package version.")

except CalledProcessError as e:
    from VERSION import __version__
    print(f"...no git tag found. Defaulting to existing __version__ value in VERSION.py: v{__version__}")

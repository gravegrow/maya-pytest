# /// script
# dependencies = [
#     "pytest>=7.4.4",
# ]
# ///

import argparse
import os
import subprocess
from pathlib import Path
import pytest


def get_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "tests",
        nargs="?",
        type=Path,
        help="Maya tests file or directory.",
        default=os.getcwd(),
    )

    parser.add_argument(
        "-e",
        "--executable",
        type=Path,
        help="Mayapy executable.",
        default="/usr/autodesk/maya2022/bin/mayapy",
    )

    return parser.parse_known_args()


def run_tests():
    pytest_path = Path(os.path.dirname(pytest.__file__)).parent.absolute()

    args, pytest_args = get_args()
    tests = str(args.tests)
    executable = str(args.executable)
    project = args.tests

    if os.path.isfile(args.tests):
        project = args.tests.parent

    if project.name == "tests":
        project = project.parent

    project = str(project.absolute())

    pytest_args.insert(0, tests)
    if "--rootdir" not in pytest_args:
        pytest_args.append("--rootdir")
        pytest_args.append(project)

    if "--verbose" not in pytest_args or "-v" not in pytest_args:
        pytest_args.append("--verbose")

    os.environ["MAYA_APP_DIR"] = os.path.join("/tmp", "clean_maya_app_dir")
    os.environ["MAYA_MODULE_PATH"] = project
    os.environ["MAYA_SCRIPT_PATH"] = ""

    subprocess.call(
        [
            executable,
            "-c"
            "import maya.standalone;"
            "maya.standalone.initialize('python');"
            "import sys;"
            "sys.path.append('{0}');"
            "import pytest;"
            "pytest.main({1});"
            "maya.standalone.uninitialize();".format(pytest_path, pytest_args),
        ]
    )


if __name__ == "__main__":
    run_tests()

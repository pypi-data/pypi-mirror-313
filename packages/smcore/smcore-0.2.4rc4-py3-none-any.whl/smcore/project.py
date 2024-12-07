import os
import sys
from vyper import v

from pathlib import Path

# I'm in a hurry and I need to match behavior between the Go API
# and the python API. I apologize to all python afficianados
# for doing go style errors.


class Error(str):
    def Error(self) -> str:
        return self


def get_project_dir() -> tuple[str, Error]:
    working_dir = os.getcwd()

    test_path = Path(working_dir)
    while test_path != Path("/"):
        if is_core_project(test_path):
            return (str(test_path), None)

        test_path = test_path.parent

    return "", Error("not a core project (or any parent directories) " + working_dir)


def is_core_project(dirpath: str) -> bool:
    # TODO: clean up this bad mix of os.path.join and Pathlib
    test_path = os.path.join(dirpath, get_core_path())
    p = Path(test_path)
    return p.is_dir()


def get_core_path() -> str:
    return "./.core"


def get_config_filename() -> str:
    return "config.yaml"


def get_config_path() -> tuple[str, Error]:
    (proj_dir, err) = get_project_dir()
    if err is not None:
        return ("", err)

    final_path = os.path.join(proj_dir, get_core_path(), get_config_filename())

    return (final_path, None)


# TODO: exception handling
def read_config(path: str):
    v.set_config_file(path)
    v.automatic_env()
    v.read_in_config()
    return v


def load_config():
    config_path, err = get_config_path()
    if err is not None:
        sys.exit(err)

    project_config = read_config(config_path)
    print("project config loaded from", config_path)
    return project_config

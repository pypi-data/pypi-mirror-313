import os
import unittest
import shutil
from pathlib import Path

from smcore import Error, project


class TestError(unittest.TestCase):
    def test_error(self):
        e = Error("new error")
        self.assertEqual(str(e), "new error")
        self.assertEqual(e, "new error")


# This test requires that a core project be initialized using the core tool
class TestProject(unittest.TestCase):
    dirname = "TESTING"

    def setup(self):
        self.start_dir = os.getcwd()
        self.project_dir = Path(os.getcwd(), self.dirname)
        os.mkdir(self.dirname)
        os.chdir(self.dirname)

    def __del__(self):
        os.chdir(self.start_dir)
        shutil.rmtree(self.dirname)

    def make_project(self):
        os.system("core init")
        os.system("core config set blackboard.addr localhost:9090")

    def test_project_dir(self):
        self.setup()

        # Return false before we've created a directory
        self.assertFalse(project.is_core_project("."))
        self.make_project()
        self.assertTrue(project.is_core_project("."))

        os.mkdir("tmp")
        os.chdir("tmp")

        pd, err = project.get_project_dir()

        self.assertIsNone(err)
        self.assertEqual(Path(pd).resolve(), self.project_dir.resolve())

    def test_read_config(self):
        self.setup()
        self.make_project()

        os.mkdir("tmp")
        os.chdir("tmp")

        (config_path, err) = project.get_config_path()
        self.assertIsNone(err)

        vyper_config = project.read_config(config_path)
        print(vyper_config.get("blackboard.addr"))
        self.assertEqual(vyper_config.get("blackboard.addr"), "localhost:9090")

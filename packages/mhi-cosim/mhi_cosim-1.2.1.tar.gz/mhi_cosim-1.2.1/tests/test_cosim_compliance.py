import ast
import re
import sys
import unittest

from pathlib import Path
from typing import Tuple

if sys.version_info < (3, 9):
    raise unittest.SkipTest("ast.parse(type_comment=, feature_version=)"
                            " requires Python 3.9")


class TestCompliance(unittest.TestCase):

    @staticmethod
    def module_path() -> Path:
        return Path(__file__).parents[1]

    def python_requires(self) -> Tuple[int, int]:

        major, minor = 3, 0

        setup_cfg = self.module_dir / "setup.cfg"
        setup_py = self.module_dir / "setup.py"
        if setup_cfg.is_file():
            m = re.search(r"^\s*python_requires\s*=\s*>=\s*3.(\d+)",
                          setup_cfg.read_text(), re.MULTILINE)
            if m:
                minor = int(m.group(1))
            else:
                raise ValueError("Unable to find 'python_requires = >= 3.#'"
                                 " in setup.cfg")
        elif setup_py.is_file():
            m = re.search(r'''\bpython_requires=['"]>=3\.(\d+)['"]''',
                          setup_py.read_text())
            if m:
                minor = int(m.group(1))
            else:
                raise ValueError("""Unable to find 'python_requires=">=3.#"'"""
                                 " in setup.py")

        if minor < 4:
            raise ValueError("Python requires must be at least 3.4")

        return (major, minor)


    def setUp(self):
        self.module_dir = self.module_path()
        self.version = self.python_requires()

    def test_compliance(self):
        module_name = self.module_dir.name
        src_root = self.module_dir / "src" / "mhi" / module_name

        for file in src_root.rglob("*.py"):
            with self.subTest(file.name):
                self.check_compliance(file)

    def check_compliance(self, file):
        source = file.read_text(encoding='utf-8')
        try:
            ast.parse(source, file, type_comments=True,
                      feature_version=self.version)
        except SyntaxError as err:
            raise AssertionError(str(err)) from None



if __name__ == '__main__':
    unittest.main()

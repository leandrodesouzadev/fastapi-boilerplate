import argparse
import importlib
import shutil
from typing import List

from main.management.exc import CommandError


class StartAppCommand:

    parser: argparse.ArgumentParser

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog="startapp facility",
            description="Creates an template directory",
        )
        self.parser.add_argument("name", type=str)

    def handle(self, argv: List[str]):
        print("Handling", argv)
        self.args = self.parser.parse_args(argv)
        self._check_name()

    def _check_name(self):
        self.args.name = str(self.args.name).lower()
        if not self.args.name.isidentifier():
            raise CommandError(
                (
                    "'{}' its not an valid python identifier."
                    " Please select another name"
                ).format(self.args.name)
            )
        try:
            importlib.import_module(self.args.name)
        except ImportError:
            pass
        else:
            raise CommandError(
                (
                    "There is already an module with this name '{}'"
                    " Please select another name"
                ).format(self.args.name)
            )

    def execute(self):
        app_name: str = self.args.name
        base_path = "src/{}".format(app_name)

        shutil.copytree("src/main/management/template", base_path)

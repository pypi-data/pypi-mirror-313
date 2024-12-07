#!/usr/bin/python3
# -*- coding: utf-8 -*-


from slpkg.configs import Configs
from slpkg.utilities import Utilities
from slpkg.views.views import View


class Cleanings(Configs):  # pylint: disable=[R0903]
    """Cleans the logs from packages."""

    def __init__(self):
        super(Configs, self).__init__()

        self.view = View()
        self.utils = Utilities()

    def tmp(self) -> None:
        """Delete files and folders in /tmp/slpkg/ folder."""
        print('Deleting of local data:\n')

        for file in self.tmp_slpkg.rglob('*'):
            print(f"  {self.bred}>{self.endc} {file}")

        print(f"\n{self.prog_name}: {self.bold}{self.bred}WARNING{self.endc}: All the files and "
              f"folders will delete!")

        self.view.question()

        self.utils.remove_folder_if_exists(self.tmp_slpkg)
        self.utils.create_directory(self.build_path)
        print('Successfully cleared!\n')

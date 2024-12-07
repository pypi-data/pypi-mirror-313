#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os

from slpkg.configs import Configs
from slpkg.utilities import Utilities
from slpkg.dialog_box import DialogBox


class Choose(Configs):  # pylint: disable=[R0902]
    """Choose packages with dialog utility and -S, --search flag."""

    def __init__(self, repository: str):
        super(Configs, self).__init__()
        self.repository: str = repository

        self.utils = Utilities()
        self.dialogbox = DialogBox()

        self.choices: list = []
        self.height: int = 10
        self.width: int = 70
        self.list_height: int = 0
        self.ordered: bool = True

    def packages(self, data: dict, packages: list, method: str, ordered: bool = True) -> list:
        """Call methods to choosing packages via dialog tool.

        Args:
            data (dict): Repository data.
            packages (list): List of packages.
            method (str): Type of method.

        Returns:
            list: Name of packages.

        Raises:
            SystemExit: Exit code 0.
        """
        self.ordered: bool = ordered
        if self.dialog:
            title: str = f' Choose packages you want to {method} '

            if method in ('remove', 'find'):
                self.choose_from_installed(packages)
            elif method == 'upgrade':
                title: str = f' Choose packages you want to {method} or add '
                self.choose_for_upgraded(data, packages)
            else:
                self.choose_for_others(data, packages)

            if not self.choices:
                return packages

            text: str = f'There are {len(self.choices)} packages:'
            code, packages = self.dialogbox.checklist(text, title, self.height, self.width,
                                                      self.list_height, self.choices)
            if code == 'cancel' or not packages:
                os.system('clear')
                raise SystemExit(0)

            os.system('clear')

        return packages

    def choose_from_installed(self, packages: list) -> None:
        """Choose installed packages for remove or find."""
        for name, package in self.utils.all_installed().items():
            version: str = self.utils.split_package(package)['version']

            for pkg in sorted(packages):
                if pkg in name or pkg == '*':
                    self.choices.extend([(name, version, False, f'Package: {package}')])

    def choose_for_upgraded(self, data: dict, packages: list) -> None:
        """Choose packages that they will going to upgrade."""
        if self.ordered:
            packages: list = sorted(packages)

        for package in packages:

            inst_package: str = self.utils.is_package_installed(package)
            inst_package_version: str = self.utils.split_package(inst_package)['version']
            inst_package_build: str = self.utils.split_package(inst_package)['build']

            repo_ver: str = data[package]['version']
            repo_build_tag: str = data[package]['build']

            if not inst_package:
                self.choices.extend(
                    [(package, f'None -> {repo_ver}', True,
                        f'Installed: None -> Available: {repo_ver} Build: {repo_build_tag}')])
            else:
                self.choices.extend(
                    [(package, f'{inst_package_version} -> {repo_ver}', True,
                        f'Installed: {package}-{inst_package_version} Build: {inst_package_build} -> '
                        f'Available: {repo_ver} Build: {repo_build_tag}')])

    def choose_for_others(self, data: dict, packages: list) -> None:
        """Choose packages for others methods like install, tracking etc."""
        if self.repository == '*':
            for pkg in sorted(packages):
                for repo_name, repo_data in data.items():
                    for package in repo_data.keys():
                        if pkg in package or pkg == '*':
                            version: str = repo_data[package]['version']
                            self.choices.extend([(package, version, False, f'Package: {package}-{version} '
                                                                           f'> {repo_name}')])

        else:
            for pkg in sorted(packages):
                for package in data.keys():
                    if pkg in package or pkg == '*':
                        version: str = data[package]['version']
                        self.choices.extend([(package, version, False, f'Package: {package}-{version} '
                                                                       f'> {self.repository}')])

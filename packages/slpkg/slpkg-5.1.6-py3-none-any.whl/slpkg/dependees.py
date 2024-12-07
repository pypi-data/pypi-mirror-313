#!/usr/bin/python3
# -*- coding: utf-8 -*-


from typing import Generator
from slpkg.configs import Configs
from slpkg.utilities import Utilities
from slpkg.views.asciibox import AsciiBox


class Dependees(Configs):  # pylint: disable=[R0902]
    """Prints the packages that depend on."""

    def __init__(self, data: dict, packages: list, flags: list):
        super(Configs, self).__init__()
        self.data: dict = data
        self.packages: list = packages
        self.flags: list = flags

        self.ascii = AsciiBox()
        self.utils = Utilities()

        self.llc: str = self.ascii.lower_left_corner
        self.hl: str = self.ascii.horizontal_line
        self.var: str = self.ascii.vertical_and_right
        self.package_version: str = ''

        self.option_for_full_reverse: bool = self.utils.is_option(
            ('-E', '--full-reverse'), flags)

        self.option_for_pkg_version: bool = self.utils.is_option(
            ('-p', '--pkg-version'), flags)

    def find(self) -> None:
        """Call the methods."""
        print('The list below shows the packages that dependees on:\n')
        self.packages: list = self.utils.apply_package_pattern(self.data, self.packages)

        for package in self.packages:
            dependees: dict = dict(self.find_requires(package))
            self.view_the_main_package(package)
            self.view_no_dependees(dependees)
            self.view_dependees(dependees)
            self.view_summary_of_dependees(dependees, package)

    def set_the_package_version(self, package: str) -> None:
        """Set the version of the package.

        Args:
            package (str): Package name.
        """
        self.package_version: str = self.data[package]['version']

    def find_requires(self, package: str) -> Generator:
        """Find requires that package dependees.

        Args:
            package (str): Package name.

        Yields:
            Generator: List of names with requires.
        """
        for name, data in self.data.items():
            if package in data['requires']:
                yield name, data['requires']

    def view_no_dependees(self, dependees: dict) -> None:
        """Print for no dependees.

        Args:
            dependees (dict): Packages data.
        """
        if not dependees:
            print(f"{'':>1}{self.cyan}No dependees{self.endc}")

    def view_the_main_package(self, package: str) -> None:
        """Print the main package.

        Args:
            package (str): Package name.
        """
        print(f'{self.byellow}{package}{self.endc}')
        print(f"{'':>1}{self.llc}{self.hl}", end='')

    @staticmethod
    def view_dependency_line(n: int, dependency: str) -> None:
        """Print the dependency line.

        Args:
            n (int): Line number.
            dependency (str): Name of dependency.
        """
        str_dependency: str = f"{'':>4}{dependency}"
        if n == 1:
            str_dependency: str = f"{'':>1}{dependency}"
        print(str_dependency)

    def view_dependees(self, dependees: dict) -> None:
        """View packages that depend on.

        Args:
            dependees (dict): Packages data.
        """
        name_length: int = 0
        if dependees:
            name_length: int = max(len(name) for name in dependees.keys())
        for n, (name, requires) in enumerate(dependees.items(), start=1):
            dependency: str = f'{self.cyan}{name}{self.endc}'
            if self.option_for_pkg_version:
                self.set_the_package_version(name)
                dependency: str = (f'{self.cyan}{name:<{name_length}}{self.endc} {self.yellow}'
                                   f'{self.package_version}{self.endc}')

            self.view_dependency_line(n, dependency)

            if self.option_for_full_reverse:
                self.view_full_reverse(n, dependees, requires)

    def view_full_reverse(self, n: int, dependees: dict, requires: str) -> None:
        """Print all packages.

        Args:
            n (int): Number of line.
            dependees (dict): Packages data.
            requires (str): Package requires.
        """
        line_requires: str = f"{'':>5}{self.var}{self.hl} {self.violet}{','.join(requires)}{self.endc}"
        if n == len(dependees):
            line_requires: str = f"{'':>5}{self.llc}{self.hl} {self.violet}{','.join(requires)}{self.endc}"
        print(line_requires)

    def view_summary_of_dependees(self, dependees: dict, package: str) -> None:
        """Print the summary.

        Args:
            dependees (dict): Packages data.
            package (str): Package name.
        """
        print(f'\n{self.grey}{len(dependees)} dependees for {package}{self.endc}\n')

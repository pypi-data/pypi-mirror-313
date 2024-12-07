#!/usr/bin/python3
# -*- coding: utf-8 -*-


from slpkg.configs import Configs
from slpkg.utilities import Utilities
from slpkg.views.asciibox import AsciiBox
from slpkg.repositories import Repositories
from slpkg.sbos.dependencies import Requires
from slpkg.binaries.required import Required


class Tracking(Configs):  # pylint: disable=[R0902]
    """Tracking of the package dependencies."""

    def __init__(self, data: dict, packages: list, flags: list, repository: str):
        super(Configs, self).__init__()
        self.data: dict = data
        self.packages: list = packages
        self.flags: list = flags
        self.repository: str = repository

        self.ascii = AsciiBox()
        self.utils = Utilities()
        self.repos = Repositories()

        self.llc: str = self.ascii.lower_left_corner
        self.hl: str = self.ascii.horizontal_line
        self.package_version: str = ''
        self.package_dependency_version: str = ''
        self.package_requires: list = []
        self.package_line: str = ''
        self.require_line: str = ''
        self.count_requires: int = 0
        self.require_length: int = 0

        self.option_for_pkg_version: bool = self.utils.is_option(
            ('-p', '--pkg-version'), flags)

    def package(self) -> None:
        """Call methods and prints the results."""
        self.view_the_title()

        for package in self.packages:
            self.count_requires: int = 0

            self.set_the_package_line(package)
            self.set_package_requires(package)
            self.view_the_main_package()
            self.view_no_dependencies()

            for require in self.package_requires:
                self.count_requires += 1

                self.set_the_package_require_line(require)
                self.view_requires()

            self.view_summary_of_tracking(package)

    def view_the_title(self) -> None:
        """Print the title."""
        print("The list below shows the packages with dependencies:\n")
        self.packages: list = self.utils.apply_package_pattern(self.data, self.packages)

    def view_the_main_package(self) -> None:
        """Print the main package."""
        print(self.package_line)
        print(f"{'':>1}{self.llc}{self.hl}", end='')

    def view_requires(self) -> None:
        """Print the requires."""
        if self.count_requires == 1:
            print(f"{'':>1}{self.require_line}")
        else:
            print(f"{'':>4}{self.require_line}")

    def view_no_dependencies(self) -> None:
        """Print the message 'No dependencies'."""
        if not self.package_requires:
            print(f"{'':>1}{self.cyan}No dependencies{self.endc}")

    def set_the_package_line(self, package: str) -> None:
        """Set for package line.

        Args:
            package (str): Package name.
        """
        self.package_line: str = f'{self.yellow}{package}{self.endc}'
        if self.option_for_pkg_version:
            self.set_package_version(package)
            self.package_line: str = f'{self.yellow}{package} {self.package_version}{self.endc}'

    def set_the_package_require_line(self, require: str) -> None:
        """Set the requires.

        Args:
            require (str): Require name.
        """
        color: str = self.cyan
        if require not in self.data:
            color: str = self.red

        self.require_line: str = f'{color}{require}{self.endc}'

        if self.option_for_pkg_version:
            self.set_package_dependency_version(require)
            self.require_line: str = (f'{color}{require:<{self.require_length}}{self.endc}'
                                      f'{self.package_dependency_version}')

    def set_package_dependency_version(self, require: str) -> None:
        """Set the dependency version.

        Args:
            require (str): Description
        """
        self.package_dependency_version: str = f"{'':>1}(not included)"
        if self.data.get(require):
            self.package_dependency_version: str = (
                f"{'':>1}{self.yellow}{self.data[require]['version']}{self.endc}"
            )

    def set_package_version(self, package: str) -> None:
        """Set the main package version.

        Args:
            package (str): Package name.
        """
        self.package_version: str = self.data[package]['version']

    def set_package_requires(self, package: str) -> None:
        """Set for the package require.

        Args:
            package (str): Package name.
        """
        if self.repository not in [self.repos.sbo_repo_name, self.repos.ponce_repo_name]:
            self.package_requires: list = list(Required(self.data, package, self.flags).resolve())
        else:
            self.package_requires: list = list(Requires(self.data, package, self.flags).resolve())

        if self.package_requires:
            if self.view_missing_deps:
                requires: list = self.data[package]['requires']
                for req in requires:
                    if req not in self.data:
                        self.package_requires.append(req)
            self.require_length: int = max(len(name) for name in self.package_requires)

    def view_summary_of_tracking(self, package: str) -> None:
        """Print the summary.

        Args:
            package (str): Package name.
        """
        print(f'\n{self.grey}{self.count_requires} dependencies for {package}{self.endc}\n')

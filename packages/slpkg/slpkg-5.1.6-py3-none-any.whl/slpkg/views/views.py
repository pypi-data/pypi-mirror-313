#!/usr/bin/python3
# -*- coding: utf-8 -*-


import shutil
from pathlib import Path

from slpkg.configs import Configs
from slpkg.upgrade import Upgrade
from slpkg.utilities import Utilities
from slpkg.views.asciibox import AsciiBox
from slpkg.repositories import Repositories


class View(Configs):  # pylint: disable=[R0902]
    """Views packages for build, install, remove or download."""

    def __init__(self, flags: list = None, repository: str = None, data: dict = None):
        super(Configs, self).__init__()

        if flags is None:
            flags: list = []

        self.flags: list = flags
        self.repository: str = repository
        self.data: dict = data

        self.repos = Repositories()
        self.utils = Utilities()
        self.ascii = AsciiBox()
        self.upgrade = Upgrade(repository, data)

        self.sum_install = 0
        self.sum_upgrade = 0
        self.sum_remove = 0
        self.sum_size_comp = 0
        self.sum_size_uncomp = 0
        self.sum_size_remove = 0
        self.columns, self.rows = shutil.get_terminal_size()

        self.download_only = None
        self.summary_message: str = ''
        self.mode = None

        self.option_for_reinstall: bool = self.utils.is_option(
            ('-r', '--reinstall'), flags)

        self.option_for_yes: bool = self.utils.is_option(
            ('-y', '--yes'), flags)

    def build_packages(self, slackbuilds: list, dependencies: list) -> None:
        """View packages for build method.

        Args:
            slackbuilds (list): Slackbuilds for build.
            dependencies (list): Dependencies for build.
        """
        self.mode: str = 'build'
        self.ascii.draw_package_title('The following packages will be build:',
                                      'slpkg build packages')

        for slackbuild in slackbuilds:
            self.draw_build_package(slackbuild)
            self.summary(slackbuild)

        if dependencies:
            self.ascii.draw_middle_line()
            self.ascii.draw_dependency_line()

            for dependency in dependencies:
                self.draw_build_package(dependency)
                self.summary(dependency)

        self.ascii.draw_bottom_line()
        self.set_summary_for_build(slackbuilds + dependencies)
        print(self.summary_message)

    def install_upgrade_packages(self, packages: list, dependencies: list, mode: str) -> None:
        """View packages for install or upgrade.

        Args:
            packages (list): Packages for install.
            dependencies (list): Dependencies for install.
            mode (str): Type of mode.
        """
        self.mode: str = mode
        title: str = 'slpkg install packages'
        if mode == 'upgrade':
            title: str = 'slpkg upgrade packages'
        self.ascii.draw_package_title('The following packages will be installed or upgraded:', title)

        for package in packages:
            self.draw_install_upgrade_package(package)
            self.summary(package)

        if dependencies:
            self.ascii.draw_middle_line()
            self.ascii.draw_dependency_line()

            for dependency in dependencies:
                self.draw_install_upgrade_package(dependency)
                self.summary(dependency)

        self.ascii.draw_bottom_line()
        self.set_summary_for_install_and_upgrade(self.sum_install, self.sum_upgrade,
                                                 self.sum_size_comp, self.sum_size_uncomp)
        print(self.summary_message)

    def download_packages(self, packages: list, directory: Path) -> None:
        """View packages for download method.

        Args:
            packages (list): Packages name for download.
            directory (Path): Path to download.
        """
        self.mode: str = 'download'
        self.download_only: Path = directory
        self.ascii.draw_package_title('The following packages will be downloaded:',
                                      'slpkg download packages')

        for package in packages:
            self.draw_download_package(package)
            self.summary(package)

        self.ascii.draw_bottom_line()
        self.set_summary_for_download(packages, self.sum_size_comp)
        print(self.summary_message)

    def remove_packages(self, packages: list, dependencies: list) -> None:
        """View packages for remove.

        Args:
            packages (list): List of packages.
            dependencies (list): List of dependencies.
        """
        self.mode: str = 'remove'
        self.ascii.draw_package_title('The following packages will be removed:',
                                      'slpkg remove packages')
        for package in packages:
            self.draw_remove_package(package)
            self.summary(package)

        if dependencies:
            self.ascii.draw_middle_line()
            self.ascii.draw_dependency_line()

            for dependency in dependencies:
                self.draw_remove_package(dependency)
                self.summary(dependency)

        self.ascii.draw_bottom_line()
        self.set_summary_for_remove(self.sum_remove, self.sum_size_remove)
        print(self.summary_message)

    def draw_build_package(self, package: str) -> None:
        """Draw line for build package method.

        Args:
            package (str): Package name.
        """
        size: str = ''
        color: str = self.yellow
        version: str = self.data[package]['version']

        self.ascii.draw_package_line(package, version, size, color, self.repository)

    def draw_install_upgrade_package(self, package: str) -> None:
        """Draw line for install or upgrade package method.

        Args:
            package (str): Package name.
        """
        size: str = ''
        color: str = self.cyan
        version: str = self.data[package]['version']
        installed: str = self.utils.is_package_installed(package)
        upgradable: bool = self.upgrade.is_package_upgradeable(installed)

        if self.repository not in [self.repos.sbo_repo_name, self.repos.ponce_repo_name]:
            size_comp: float = float(self.data[package]['size_comp']) * 1024
            size: str = self.utils.convert_file_sizes(size_comp)

        if installed:
            color: str = self.grey

        if upgradable:
            color: str = self.violet
            package: str = self.build_package_and_version(package)

        if installed and self.option_for_reinstall and not upgradable:
            color: str = self.violet
            package: str = self.build_package_and_version(package)

        self.ascii.draw_package_line(package, version, size, color, self.repository)

    def draw_download_package(self, package: str) -> None:
        """Draw package for download method.

        Args:
            package (str): Package name.
        """
        size: str = ''
        color: str = self.cyan
        version: str = self.data[package]['version']

        if self.repository not in [self.repos.sbo_repo_name, self.repos.ponce_repo_name]:
            size_comp: float = float(self.data[package]['size_comp']) * 1024
            size: str = self.utils.convert_file_sizes(size_comp)

        self.ascii.draw_package_line(package, version, size, color, self.repository)

    def draw_remove_package(self, package: str) -> None:
        """Draw package for remove method.

        Args:
            package (str): Package name.
        """
        count_size: int = self.utils.count_file_size(package)
        installed: str = self.utils.is_package_installed(package)
        version: str = self.utils.split_package(installed)['version']
        repo_tag: str = self.utils.split_package(installed)['tag']
        size: str = self.utils.convert_file_sizes(count_size)
        repository: str = repo_tag.lower().replace('_', '')

        self.ascii.draw_package_line(package, version, size, self.red, repository)

    def summary(self, package: str) -> None:
        """Count packages per method.

        Args:
            package (str): Package name.
            method (str): Type of method.
        """
        installed: str = self.utils.is_package_installed(package)

        if self.repository not in list(self.repos.repositories)[:2] and self.repository is not None:
            self.sum_size_comp += float(self.data[package]['size_comp']) * 1024
            self.sum_size_uncomp += float(self.data[package]['size_uncomp']) * 1024

        if installed and self.mode == 'remove':
            self.sum_size_remove += self.utils.count_file_size(package)

        upgradeable: bool = False
        if self.mode != 'remove':
            upgradeable: bool = self.upgrade.is_package_upgradeable(installed)

        if not installed:
            self.sum_install += 1
        elif installed and self.option_for_reinstall:
            self.sum_upgrade += 1
        elif upgradeable:
            self.sum_upgrade += 1
        elif installed and self.mode == 'remove':
            self.sum_remove += 1

    def set_summary_for_build(self, packages: list) -> None:
        """Set summary message for build.

        Args:
            packages (list): List of packages.
        """
        self.summary_message: str = (
            f'{self.grey}Total {len(packages)} packages '
            f'will be build in {self.tmp_path} folder.{self.endc}')

    def set_summary_for_install_and_upgrade(self, install: int, upgrade: int, size_comp: int, size_uncomp: int) -> None:
        """Set summary for install or upgrade.

        Args:
            install (int): Counts for installs.
            upgrade (int): Counts for upgrades.
            size_comp (int): Counts of compressed sizes.
            size_uncomp (int): Counts of uncompressed sizes.
        """
        upgrade_message: str = ''
        split_message: str = '\n'
        if self.columns > 80:
            split_message: str = ''
        total_packages: str = (f'{self.grey}Total {install} packages will be installed and {upgrade} '
                               f'will be upgraded, while a total ')
        total_sizes: str = (f'{self.utils.convert_file_sizes(size_comp)} will be downloaded and '
                            f'{self.utils.convert_file_sizes(size_uncomp)} will be installed.{self.endc}')
        if self.mode == 'upgrade' and not self.package_method:
            if self.upgrade_log_file.is_file():
                upgrade_message: str = (f'\n{self.red}Some versions failed, '
                                        f'check the /var/log/slpkg/upgrade.log file.{self.endc}')
            else:
                upgrade_message: str = (f'\n{self.grey}Note: Packages with custom versions may not '
                                        f'compare correctly.{self.endc}')
        self.summary_message: str = f'{total_packages}{split_message}{total_sizes}{upgrade_message}'

    def set_summary_for_remove(self, remove: int, size_rmv: int) -> None:
        """Set summary for removes.

        Args:
            remove (int): Counts of removes.
            size_rmv (int): Size of removes.
        """
        self.summary_message: str = (
            f'{self.grey}Total {remove} packages '
            f'will be removed and {self.utils.convert_file_sizes(size_rmv)} '
            f'of space will be freed up.{self.endc}')

    def set_summary_for_download(self, packages: list, size_comp: int) -> None:
        """Set summary for downloads.

        Args:
            packages (list): List of packages.
            size_comp (int): Size of downloads.
        """
        self.summary_message: str = (
            f'{self.grey}Total {len(packages)} packages and {self.utils.convert_file_sizes(size_comp)} '
            f'will be downloaded in {self.download_only} folder.{self.endc}')

    def build_package_and_version(self, package: str) -> str:
        """Build package and version.

        Args:
            package (str): Package name.

        Returns:
            str: Package with the version.
        """
        installed_package: str = self.utils.is_package_installed(package)
        version: str = self.utils.split_package(installed_package)['version']
        return f'{package}-{version}'

    def skipping_packages(self, packages: list) -> None:
        """View skipped packages.

        Args:
            packages (list): List of packages.
        """
        if packages:
            print('Packages skipped by the user:\n')
            for name in packages:
                failed: str = f'{self.red}{self.ascii.skipped}{self.endc}'
                print(f"\r{'':>2}{self.bred}{self.ascii.bullet}{self.endc} "
                      f"{self.data[name]['package']} {failed}{' ' * 17}")
            print()

    def missing_dependencies(self, packages: list) -> None:
        """View for missing dependencies."""
        if self.view_missing_deps:
            missing_deps: dict = {}
            for package in packages:
                requires: list = self.data[package]['requires']
                for req in requires:
                    if req not in self.data:
                        missing_deps[package] = [req for req in requires if req not in self.data]
            if missing_deps:
                print('\nPackages with missing dependencies:')
                for pkg, deps in missing_deps.items():
                    if deps and deps != ['']:
                        print(f"> {self.cyan}{pkg}{self.endc}: Requires "
                              f"({len(deps)}) -> {self.red}{', '.join(deps)}{self.endc}")

    def question(self, message: str = 'Do you want to continue?') -> None:
        """View a question.

        Args:
            message (str, optional): Message of question.

        Raises:
            SystemExit: Raise a exit code 0.
        """
        if not self.option_for_yes and self.ask_question:
            answer: str = input(f'\n{message} [y/N] ')
            if answer not in ['Y', 'y']:
                raise SystemExit(0)
        print()

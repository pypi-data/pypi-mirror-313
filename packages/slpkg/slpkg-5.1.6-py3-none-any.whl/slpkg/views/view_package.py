#!/usr/bin/python3
# -*- coding: utf-8 -*-


from pathlib import Path

from slpkg.configs import Configs
from slpkg.utilities import Utilities
from slpkg.repositories import Repositories


class ViewPackage(Configs):  # pylint: disable=[R0902]
    """View the packages information."""

    def __init__(self, flags: list, repository: str):
        super(Configs, self).__init__()

        self.flags: list = flags
        self.repository: str = repository

        self.utils = Utilities()
        self.repos = Repositories()

        self.repository_packages: tuple = ()
        self.readme: list = []
        self.info_file: list = []
        self.repo_build_tag: str = ''
        self.mirror: str = ''
        self.homepage: str = ''
        self.maintainer: str = ''
        self.email: str = ''
        self.dependencies: str = ''
        self.repo_tar_suffix: str = ''

        self.option_for_pkg_version: bool = self.utils.is_option(
            ('-p', '--pkg-version'), flags)

    def slackbuild(self, data: dict, slackbuilds: list) -> None:
        """View slackbuilds information.

        Args:
            data (dict): Repository data.
            slackbuilds (list): List of slackbuilds.
        """
        print()
        repo: dict = {
            self.repos.sbo_repo_name: self.repos.sbo_repo_tar_suffix,
            self.repos.ponce_repo_name: ''
        }
        git_mirror: dict = {
            self.repos.sbo_repo_name: self.repos.sbo_git_mirror,
            self.repos.ponce_repo_name: self.repos.ponce_git_mirror
        }

        self.repo_tar_suffix: str = repo[self.repository]

        self.mirror: str = self.repos.repositories[self.repository]['mirror_packages']
        if '.git' in git_mirror[self.repository]:
            repo_path: str = self.utils.get_git_branch(self.repos.repositories[self.repository]['path'])
            self.mirror: str = git_mirror[self.repository].replace('.git', f'/tree/{repo_path}/')
            self.repo_tar_suffix: str = '/'

        self.repository_packages: tuple = tuple(data.keys())

        for sbo in slackbuilds:
            for name, item in data.items():

                if sbo in [name, '*']:
                    path_file: Path = Path(self.repos.repositories[self.repository]['path'],
                                           item['location'], name, 'README')
                    path_info: Path = Path(self.repos.repositories[self.repository]['path'],
                                           item['location'], name, f'{name}.info')

                    self.read_the_readme_file(path_file)
                    self.read_the_info_file(path_info)
                    self.repo_build_tag: str = data[name]['build']
                    self.assign_the_info_file_variables()
                    self.assign_dependencies(item)
                    self.assign_dependencies_with_version(item, data)
                    self.view_slackbuild_package(name, item)

    def read_the_readme_file(self, path_file: Path) -> None:
        """Read the README file.

        Args:
            path_file (Path): Path to the file.
        """
        self.readme: list = self.utils.read_text_file(path_file)

    def read_the_info_file(self, path_info: Path) -> None:
        """Read the .info file.

        Args:
            path_info (Path): Path to the file.
        """
        self.info_file: list = self.utils.read_text_file(path_info)

    def assign_the_info_file_variables(self) -> None:
        """Assign data from the .info file."""
        for line in self.info_file:
            if line.startswith('HOMEPAGE'):
                self.homepage: str = line[10:-2].strip()
            if line.startswith('MAINTAINER'):
                self.maintainer: str = line[12:-2].strip()
            if line.startswith('EMAIL'):
                self.email: str = line[7:-2].strip()

    def assign_dependencies(self, item: dict) -> None:
        """Assign the package dependencies.

        Args:
            item (dict): Data value.
        """
        self.dependencies: str = ', '.join([f'{self.cyan}{pkg}' for pkg in item['requires']])

    def assign_dependencies_with_version(self, item: dict, data: dict) -> None:
        """Assign dependencies with version.

        Args:
            item (dict): Data value.
            data (dict): Repository data.
        """
        if self.option_for_pkg_version:
            self.dependencies: str = (', '.join(
                [f"{self.cyan}{pkg}{self.endc}-{self.yellow}{data[pkg]['version']}"
                 f"{self.green}" for pkg in item['requires']
                 if pkg in self.repository_packages]))

    def view_slackbuild_package(self, name: str, item: dict) -> None:
        """Print slackbuild information.

        Args:
            name (str): Slackbuild name.
            item (dict): Data value.
        """
        space_align: str = ''
        print(f"{'Repository':<15}: {self.green}{self.repository}{self.endc}\n"
              f"{'Name':<15}: {self.green}{name}{self.endc}\n"
              f"{'Version':<15}: {self.green}{item['version']}{self.endc}\n"
              f"{'Build':<15}: {self.green}{self.repo_build_tag}{self.endc}\n"
              f"{'Homepage':<15}: {self.blue}{self.homepage}{self.endc}\n"
              f"{'Download SBo':<15}: {self.blue}{self.mirror}"
              f"{item['location']}/{name}{self.repo_tar_suffix}{self.endc}\n"
              f"{'Sources':<15}: {self.blue}{' '.join(item['download'])}{self.endc}\n"
              f"{'Md5sum':<15}: {self.yellow}{' '.join(item['md5sum'])}{self.endc}\n"
              f"{'Sources x86_64':<15}: {self.blue}{' '.join(item['download64'])}{self.endc}\n"
              f"{'Md5sum x86_64':<15}: {self.yellow}{' '.join(item['md5sum64'])}{self.endc}\n"
              f"{'Files':<15}: {self.green}{' '.join(item['files'])}{self.endc}\n"
              f"{'Category':<15}: {self.red}{item['location']}{self.endc}\n"
              f"{'SBo url':<15}: {self.blue}{self.mirror}{item['location']}/{name}/{self.endc}\n"
              f"{'Maintainer':<15}: {self.yellow}{self.maintainer}{self.endc}\n"
              f"{'Email':<15}: {self.yellow}{self.email}{self.endc}\n"
              f"{'Requires':<15}: {self.green}{self.dependencies}{self.endc}\n"
              f"{'Description':<15}: {self.green}{item['description']}{self.endc}\n"
              f"{'README':<15}: {self.cyan}{f'{space_align:>17}'.join(self.readme)}{self.endc}")

    def package(self, data: dict, packages: list) -> None:
        """View binary packages information.

        Args:
            data (dict): Repository data.
            packages (list): List of packages.
        """
        print()
        self.repository_packages: tuple = tuple(data.keys())
        for package in packages:
            for name, item in data.items():
                if package in [name, '*']:

                    self.assign_dependencies(item)
                    self.assign_dependencies_with_version(item, data)
                    self.view_binary_package(name, item)

    def view_binary_package(self, name: str, item: dict) -> None:
        """Print binary packages information.

        Args:
            name (str): Package name.
            item (dict): Data values.
        """
        print(f"{'Repository':<15}: {self.green}{self.repository}{self.endc}\n"
              f"{'Name':<15}: {self.green}{name}{self.endc}\n"
              f"{'Version':<15}: {self.green}{item['version']}{self.endc}\n"
              f"{'Build':<15}: {self.green}{item['build']}{self.endc}\n"
              f"{'Package':<15}: {self.cyan}{item['package']}{self.endc}\n"
              f"{'Download':<15}: {self.blue}{item['mirror']}{item['location']}/{item['package']}{self.endc}\n"
              f"{'Md5sum':<15}: {item['checksum']}\n"
              f"{'Mirror':<15}: {self.blue}{item['mirror']}{self.endc}\n"
              f"{'Location':<15}: {self.red}{item['location']}{self.endc}\n"
              f"{'Size Comp':<15}: {self.yellow}{item['size_comp']} KB{self.endc}\n"
              f"{'Size Uncomp':<15}: {self.yellow}{item['size_uncomp']} KB{self.endc}\n"
              f"{'Requires':<15}: {self.green}{self.dependencies}{self.endc}\n"
              f"{'Conflicts':<15}: {item['conflicts']}\n"
              f"{'Suggests':<15}: {item['suggests']}\n"
              f"{'Description':<15}: {item['description']}\n")

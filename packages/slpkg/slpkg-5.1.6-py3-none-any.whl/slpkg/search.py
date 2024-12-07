#!/usr/bin/python3
# -*- coding: utf-8 -*-


from slpkg.configs import Configs
from slpkg.utilities import Utilities
from slpkg.repositories import Repositories
from slpkg.views.view_process import ViewProcess


class SearchPackage(Configs):  # pylint: disable=[R0902]
    """Search packages from the repositories."""

    def __init__(self, flags: list, packages: list, data: dict, repository: str):
        super(Configs, self).__init__()
        self.packages: list = packages
        self.data: dict = data
        self.repository: str = repository

        self.utils = Utilities()
        self.repos = Repositories()
        self.view_process = ViewProcess()

        self.matching: int = 0
        self.data_dict: dict = {}
        self.repo_data: dict = {}
        self.all_data: dict = {}

        self.option_for_no_case: bool = self.utils.is_option(
            ('-m', '--no-case'), flags)

        self.option_for_pkg_version: bool = self.utils.is_option(
            ('-p', '--pkg-version'), flags)

    def search(self) -> None:
        """Choose between all and one repository."""
        self.view_process.message('Please wait for the results')
        if self.repository == '*':
            self.search_to_all_repositories()
        else:
            self.repo_data: dict = self.data
            self.search_for_the_packages(self.repository)

        self.view_process.done()
        print()
        self.summary_of_searching()

    def search_to_all_repositories(self) -> None:
        """Search package name to all enabled repositories."""
        self.all_data: dict = self.data
        for name, repo in self.all_data.items():
            self.repo_data: dict = repo
            self.search_for_the_packages(name)

    def search_for_the_packages(self, repo: str) -> None:
        """Search for packages and save in a dictionary.

        Args:
            repo (str): repository name.
        """
        for package in self.packages:
            for name, data_pkg in sorted(self.repo_data.items()):

                if package in name or package == '*' or self.is_not_case_sensitive(package, name):
                    self.matching += 1
                    installed: str = f'{self.endc}'
                    is_installed: str = self.utils.is_package_installed(name)

                    if self.repository == '*':
                        if is_installed == self.all_data[repo][name]['package'][:-4]:
                            installed: str = f' {self.endc}(installed)'
                    elif is_installed == self.data[name]['package'][:-4]:
                        installed: str = f' {self.endc}(installed)'

                    self.data_dict[self.matching] = {
                        'repository': repo,
                        'name': name,
                        'version': data_pkg['version'],
                        'installed': installed
                    }

    def summary_of_searching(self) -> None:
        """Print the result."""
        try:
            repo_length: int = max(len(repo['repository']) for repo in self.data_dict.values())
        except ValueError:
            repo_length: int = 1

        try:
            name_length: int = max(len(name['name']) + len(name['installed']) for name in self.data_dict.values())
        except ValueError:
            name_length: int = 1

        if self.matching:
            version: str = ''
            repository: str = ''
            for item in self.data_dict.values():
                package_name: str = f"{item['name']}{item['installed']}"

                if self.option_for_pkg_version:
                    version: str = item['version']
                if self.repository == '*':
                    repository: str = f"{item['repository']:<{repo_length}} : "

                print(f"{repository}{self.cyan}{package_name:<{name_length}}{self.endc} "
                      f"{self.yellow}{version}{self.endc}")

            print(f'\n{self.grey}Total found {self.matching} packages.{self.endc}')
        else:
            print('\nDoes not match any package.\n')

    def is_not_case_sensitive(self, package: str, name: str) -> bool:
        """Check for case sensitive.

        Args:
            package (str): Package file.
            name (str): Package name.

        Returns:
            bool: True or False.
        """
        if self.option_for_no_case:
            return package.lower() in name.lower()
        return False

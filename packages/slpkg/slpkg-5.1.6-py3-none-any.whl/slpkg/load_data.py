#!/usr/bin/python3
# -*- coding: utf-8 -*-


import json
from pathlib import Path

from slpkg.configs import Configs
from slpkg.utilities import Utilities
from slpkg.blacklist import Blacklist
from slpkg.views.asciibox import AsciiBox
from slpkg.repositories import Repositories
from slpkg.views.view_process import ViewProcess


class LoadData(Configs):
    """Reads data form json file and load to dictionary."""

    def __init__(self, flags: list = None):
        super(Configs, self).__init__()

        if flags is None:
            flags = []

        self.repos = Repositories()
        self.utils = Utilities()
        self.black = Blacklist()
        self.ascii = AsciiBox()
        self.view_process = ViewProcess()

    def load(self, repository: str, message: bool = True) -> dict:
        """Load data to the dictionary.

        Args:
            repository (str): Repository name.
            message (bool, optional): Prints or not progress message.

        Returns:
            dict: Dictionary data.
        """
        if message:
            self.view_process.message('Database loading')

        data: dict = {}
        if repository == '*':
            for repo, value in self.repos.repositories.items():
                if value['enable']:  # Check if the repository is enabled
                    json_data_file: Path = Path(value['path'], self.repos.data_json)
                    data[repo] = self.read_data_file(json_data_file)
        else:
            json_data_file: Path = Path(self.repos.repositories[repository]['path'], self.repos.data_json)

            data: dict = self.read_data_file(json_data_file)

        blacklist: tuple = self.black.packages()
        if blacklist:
            if repository == '*':
                self._remove_blacklist_from_all_repos(data)
            else:
                self._remove_blacklist_from_a_repo(data)

        if message:
            self.view_process.done()

        return data

    def read_data_file(self, file: Path) -> dict:
        """Read JSON data from the file.

        Args:
            file: Path file for reading.
        Returns:
            Dictionary with data.
        """
        json_data: dict = {}
        try:
            json_data: dict = json.loads(file.read_text(encoding='utf-8'))
        except FileNotFoundError as e:
            print(f'{self.bred}{self.ascii.failed}{self.endc}')
            print(f'\nFile {file} not found!')
            print('\nNeed to update the database first, please run:\n')
            print(f"{'':>2} $ {self.green}slpkg update{self.endc}\n")
            raise SystemExit(1) from e
        except json.decoder.JSONDecodeError:
            pass
        return json_data

    def _remove_blacklist_from_all_repos(self, data: dict) -> dict:
        """Remove blacklist packages from all repositories.

        Args:
            data: Repository data.
        Returns:
            Repository data without the blackpackages.
        """
        # Remove blacklist packages from keys.
        for name, repo in data.items():
            blacklist_packages: list = self.utils.ignore_packages(list(data[name].keys()))
            for pkg in blacklist_packages:
                if pkg in data[name].keys():
                    del data[name][pkg]

        # Remove blacklist packages from dependencies (values).
        for name, repo in data.items():
            blacklist_packages: list = self.utils.ignore_packages(list(data[name].keys()))
            for pkg, dep in repo.items():
                deps: list = dep['requires']
                for blk in blacklist_packages:
                    if blk in deps:
                        deps.remove(blk)
                        data[name][pkg]['requires'] = deps
        return data

    def _remove_blacklist_from_a_repo(self, data: dict) -> dict:
        """Remove blacklist from a repository.

        Args:
            data: Repository data.
        Returns:
            Repositories data without the blackpackages.
        """
        blacklist_packages: list = self.utils.ignore_packages(list(data.keys()))
        # Remove blacklist packages from keys.
        for pkg in blacklist_packages:
            if pkg in data.keys():
                del data[pkg]

        # Remove blacklist packages from dependencies (values).
        for pkg, dep in data.items():
            deps: list = dep['requires']
            for blk in blacklist_packages:
                if blk in deps:
                    deps.remove(blk)
                    data[pkg]['requires'] = deps
        return data

#!/usr/bin/python3
# -*- coding: utf-8 -*-


from __future__ import annotations

import os
import re
import time
import json
import shutil
import subprocess
from pathlib import Path
from typing import Generator

from slpkg.configs import Configs
from slpkg.blacklist import Blacklist
from slpkg.error_messages import Errors


class Utilities(Configs):
    """List of utilities."""

    def __init__(self):
        super(Configs, self).__init__()

        self.black = Blacklist()
        self.errors = Errors()

    def is_package_installed(self, name: str) -> str:
        """Return the installed package binary.

        Args:
            name (str): Package name.

        Returns:
            str: Full package name.
        """
        installed_package: Generator = self.log_packages.glob(f'{name}*')

        for installed in installed_package:
            inst_name: str = self.split_package(installed.name)['name']
            if inst_name == name and inst_name not in self.ignore_packages([inst_name]):
                return installed.name
        return ''

    def all_installed(self) -> dict:
        """Return all installed packages from /val/log/packages folder.

        Returns:
            dict: All installed packages and names.
        """
        installed_packages: dict = {}

        for file in self.log_packages.glob('*'):
            name: str = self.split_package(file.name)['name']

            if not name.startswith('.'):
                installed_packages[name] = file.name

        blacklist_packages: list = self.ignore_packages(list(installed_packages.keys()))
        if blacklist_packages:
            for black in blacklist_packages:
                del installed_packages[black]

        return installed_packages

    @staticmethod
    def remove_file_if_exists(path: Path, file: str) -> None:
        """Remove the old files.

        Args:
            path (Path): Path to the file.
            file (str): File name.
        """
        archive: Path = Path(path, file)
        if archive.is_file():
            archive.unlink()

    @staticmethod
    def remove_folder_if_exists(folder: Path) -> None:
        """Remove the folder if exist.

        Args:
            folder (Path): Path to the folder.
        """
        if folder.exists():
            shutil.rmtree(folder)

    @staticmethod
    def create_directory(directory: Path) -> None:
        """Create folder like mkdir -p.

        Args:
            directory (Path): Path to folder.
        """
        if not directory.is_dir():
            directory.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def split_package(package: str) -> dict:
        """Split the binary package name in name, version, arch, build and tag.

        Args:
            package (str): Full package name for spliting.

        Returns:
            dict: Splitted package by name, version, arch, build and package tag.
        """
        name: str = '-'.join(package.split('-')[:-3])
        version: str = ''.join(package[len(name):].split('-')[:-2])
        arch: str = ''.join(package[len(name + version) + 2:].split('-')[:-1])
        build_tag: str = package.split('-')[-1]
        build: str = ''.join(re.findall(r'\d+', build_tag[:2]))
        pkg_tag: str = build_tag[len(build):]

        return {
            'name': name,
            'version': version,
            'arch': arch,
            'build': build,
            'tag': pkg_tag
        }

    @staticmethod
    def finished_time(elapsed_time: float) -> None:
        """Print the elapsed time.

        Args:
            elapsed_time (float): Unformatted time.
        """
        print('\nFinished:', time.strftime('%H:%M:%S', time.gmtime(elapsed_time)))

    @staticmethod
    def is_option(options: tuple, flags: list) -> bool:
        """Return True if option applied.

        Args:
            options (tuple): Options for checking.
            flags (list): The flags applied by the user.

        Returns:
            bool: True if match or False, if not matched.
        """
        for option in options:
            if option in flags:
                return True
        return False

    def read_packages_from_file(self, file: Path) -> Generator:
        """Read packages from file.

        Args:
            file (Path): Path to the file.

        Yields:
            Generator: Package names.
        """
        try:
            with open(file, 'r', encoding='utf-8') as pkgs:
                packages: list = pkgs.read().splitlines()

            for package in packages:
                if package and not package.startswith('#'):
                    if '#' in package:
                        package: str = package.split('#')[0].strip()
                    yield package
        except FileNotFoundError:
            self.errors.raise_error_message(f"No such file or directory: '{file}'", exit_status=20)

    def read_text_file(self, file: Path) -> list:
        """Read a text file.

        Args:
            file (Path): Path to the file.

        Returns:
            list: The lines in the list.
        """
        try:
            with open(file, 'r', encoding='utf-8', errors='replace') as text_file:
                return text_file.readlines()
        except FileNotFoundError:
            self.errors.raise_error_message(f"No such file or directory: '{file}'", exit_status=20)
        return []

    def count_file_size(self, name: str) -> int:
        """Count the file size.

        Read the contents files from the package file list
        and count the total installation file size in bytes.
        Args:
            name: The name of the package.

        Returns:
            The total package installation file size.
        """
        count_files: int = 0
        installed: Path = Path(self.log_packages, self.is_package_installed(name))
        if installed:
            file_installed: list = installed.read_text(encoding="utf-8").splitlines()
            for line in file_installed:
                file: Path = Path('/', line)
                if file.is_file():
                    count_files += file.stat().st_size
        return count_files

    @staticmethod
    def convert_file_sizes(byte_size: float) -> str:
        """Convert bytes to kb, mb and gb.

        Args:
            byte_size: The file size in bytes.
        Returns:
            The size converted.
        """
        kb_size: float = byte_size / 1024
        mb_size: float = kb_size / 1024
        gb_size: float = mb_size / 1024

        if gb_size >= 1:
            return f"{gb_size:.0f} GB"
        if mb_size >= 1:
            return f"{mb_size:.0f} MB"
        if kb_size >= 1:
            return f"{kb_size:.0f} KB"

        return f"{byte_size} B"

    @staticmethod
    def apply_package_pattern(data: dict, packages: list) -> list:
        """If the '*' applied returns all the package names.

        Args:
            data (dict): The repository data.
            packages (list): The packages that applied.

        Returns:
            list: Package names.
        """
        for pkg in packages:
            if pkg == '*':
                packages.remove('*')
                packages.extend(list(data.keys()))
        return packages

    @staticmethod
    def change_owner_privileges(folder: Path) -> None:
        """Change the owner privileges.

        Args:
            folder (Path): Path to the folder.
        """
        os.chown(folder, 0, 0)
        for file in os.listdir(folder):
            os.chown(Path(folder, file), 0, 0)

    def case_insensitive_pattern_matching(self, packages: list, data: dict, flags: list) -> list:
        """Case-insensitive pattern matching packages.

        Args:
            packages (list): List of packages.
            data (dict): Repository data.
            flags (list): User options.

        Returns:
            list: Matched packages.
        """
        if self.is_option(('-m', '--no-case'), flags):
            repo_packages: tuple = tuple(data.keys())
            for package in packages:
                for pkg in repo_packages:
                    if package.lower() == pkg.lower():
                        packages.append(pkg)
                        packages.remove(package)
                        break
        return packages

    def read_json_file(self, file: Path) -> dict:
        """Read JSON data from the file.

        Args:
            file: Path file for reading.
        Returns:
            Dictionary with data.
        """
        json_data: dict = {}
        try:
            json_data: dict = json.loads(file.read_text(encoding='utf-8'))
        except FileNotFoundError:
            self.errors.raise_error_message(f'{file} not found.', exit_status=1)
        except json.decoder.JSONDecodeError:
            pass
        return json_data

    def ignore_packages(self, packages: list) -> list:
        """Match packages using regular expression.

        Args:
            packages: The packages to apply the pattern.
        Returns:
            The matching packages.
        """
        matching_packages: list = []
        blacklist: tuple = self.black.packages()
        if blacklist:
            pattern: str = '|'.join(blacklist)
            matching_packages: list = [pkg for pkg in packages if re.search(pattern, pkg)]
        return matching_packages

    def get_git_branch(self, repo_path: Path) -> str:
        """Get the branch name of the git repository.

        Returns:
            str: Git branch name.
        """
        try:
            # Run the git command to get the current branch name
            branch = subprocess.check_output(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                stderr=subprocess.STDOUT, cwd=repo_path
            ).strip().decode('utf-8')
            return branch
        except subprocess.CalledProcessError as e:
            print("Error:", e.output.decode('utf-8'))
            return None

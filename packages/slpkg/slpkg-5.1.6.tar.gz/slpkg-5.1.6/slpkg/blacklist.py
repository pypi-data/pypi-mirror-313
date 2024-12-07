#!/usr/bin/python3
# -*- coding: utf-8 -*-


from pathlib import Path
import tomlkit

from slpkg.configs import Configs
from slpkg.toml_errors import TomlErrors


class Blacklist(Configs):  # pylint: disable=[R0903]
    """Reads and returns the blacklist."""

    def __init__(self) -> None:
        super(Configs, self).__init__()

        self.toml_errors = TomlErrors()
        self.blacklist_file_toml: Path = Path(self.etc_path, 'blacklist.toml')

    def packages(self) -> list:
        """Read the blacklist file."""
        packages: list = []
        if self.blacklist_file_toml.is_file():
            try:
                with open(self.blacklist_file_toml, 'r', encoding='utf-8') as file:
                    black: dict = tomlkit.parse(file.read())
                    packages: list = black['PACKAGES']
            except (KeyError, tomlkit.exceptions.TOMLKitError) as error:
                print()
                self.toml_errors.raise_toml_error_message(error, self.blacklist_file_toml)

        return packages

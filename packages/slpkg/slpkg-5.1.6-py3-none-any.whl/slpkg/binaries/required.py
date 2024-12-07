#!/usr/bin/python3
# -*- coding: utf-8 -*-


from slpkg.utilities import Utilities
from slpkg.repositories import Repositories


class Required:
    """Create a tuple of dependencies with the right order to install."""

    __slots__ = ('data', 'name', 'flags', 'repos', 'utils',
                 'full_requires', 'repository_packages',
                 'option_for_resolve_off')

    def __init__(self, data: dict, name: str, flags: list):
        self.data: dict = data
        self.name: str = name
        self.utils = Utilities()
        self.repos = Repositories()

        # Reads about how requires are listed, full listed is True
        # and normal listed is false.
        self.full_requires: bool = False
        if self.repos.repos_information.is_file():
            info: dict = self.utils.read_json_file(self.repos.repos_information)
            repo_name: str = data[name]['repo']
            if info.get(repo_name):
                self.full_requires: bool = info[repo_name].get('full_requires', False)

        self.option_for_resolve_off: bool = self.utils.is_option(
            ('-O', '--resolve-off'), flags)

    def resolve(self) -> tuple:
        """Resolve the dependencies."""
        dependencies: tuple = ()
        if not self.option_for_resolve_off:
            requires: list[str] = self.remove_deps(self.data[self.name]['requires'])

            # Resolve dependencies for some special repos.
            if not self.full_requires:
                for require in requires:

                    sub_requires: list[str] = self.remove_deps(self.data[require]['requires'])
                    for sub in sub_requires:
                        if sub not in requires:
                            requires.append(sub)

            requires.reverse()
            dependencies: tuple = tuple(dict.fromkeys(requires))

        return dependencies

    def remove_deps(self, requires: list) -> list:
        """Remove requirements that not in the repository.

        Args:
            requires (list): List of requires.

        Returns:
            list: List of packages name.
        """
        return [req for req in requires if req in self.data]

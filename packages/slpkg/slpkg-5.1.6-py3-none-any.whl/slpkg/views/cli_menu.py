#!/usr/bin/python3
# -*- coding: utf-8 -*-


from typing import NoReturn
from slpkg.configs import Configs
from slpkg.views.version import Version


class Usage(Configs):
    """CLI Usage menu."""

    def __init__(self):
        super(Configs, self).__init__()

    def help_minimal(self, message: str) -> NoReturn:
        """Print the minimal help menu.

        Args:
            message (str): Message of error.

        Raises:
            SystemExit: Raises an exit code 1.
        """
        print(message)
        args: str = (
            f'Usage: {self.prog_name} [{self.cyan}COMMAND{self.endc}] [{self.yellow}OPTIONS{self.endc}] '
            f'<packages>\n'
            f"\nTry '{self.prog_name} --help' for more options.")

        print(args)
        raise SystemExit(1)

    def help_short(self, status: int) -> NoReturn:
        """Print the short menu.

        Args:
            status (int): Status exit code.

        Raises:
            SystemExit: Raises the status code.
        """
        args: str = (
            f'USAGE: {self.prog_name} [{self.cyan}COMMAND{self.endc}] [{self.yellow}OPTIONS{self.endc}] '
            f'<packages>\n'
            f'\n  slpkg [{self.cyan}COMMAND{self.endc}] [-u, update, -U, upgrade]\n'
            f'  slpkg [{self.cyan}COMMAND{self.endc}] [-I, repo-info, -g, configs, -T, clean-tmp]\n'
            f'  slpkg [{self.cyan}COMMAND{self.endc}] [-b, build, -i, install, -R, remove <packages>]\n'
            f'  slpkg [{self.cyan}COMMAND{self.endc}] [-d, download, -f, find, -w, view <packages>]\n'
            f'  slpkg [{self.cyan}COMMAND{self.endc}] [-s, search, -e, dependees, -t, tracking  <packages>]\n'
            f'  slpkg [{self.yellow}OPTIONS{self.endc}] [-y, --yes, -c, --check, -O, --resolve-off]\n'
            f'  slpkg [{self.yellow}OPTIONS{self.endc}] [-r, --reinstall, -k, --skip-installed, -F, --fetch]\n'
            f'  slpkg [{self.yellow}OPTIONS{self.endc}] [-E, --full-reverse, -S, --search, -B, --progress-bar]\n'
            f'  slpkg [{self.yellow}OPTIONS{self.endc}] [-p, --pkg-version, -P, --parallel, -m, --no-case]\n'
            f'  slpkg [{self.yellow}OPTIONS{self.endc}] [-o, --repository=NAME, -z, --directory=PATH]\n'
            "  \nIf you need more information please try 'slpkg --help'.")

        print(args)
        raise SystemExit(status)

    def help(self, status: int) -> NoReturn:
        """Print the main menu.

        Args:
            status (int): Status exit code

        Raises:
            SystemExit: Raises the status code.
        """
        args: str = (
            f'{self.prog_name} - version {Version().version}\n\n'
            f'{self.bold}USAGE:{self.endc}\n  {self.prog_name} [{self.cyan}COMMAND{self.endc}] '
            f'[{self.yellow}OPTIONS{self.endc}] <packages>\n'
            f'\n{self.bold}DESCRIPTION:{self.endc}\n  Package manager utility for Slackware.\n'
            f'\n{self.bold}COMMANDS:{self.endc}\n'
            f'  {self.red}-u, update{self.endc}                Synchronizes the repositories database\n'
            f'{"":>28}with your local database.\n'
            f'  {self.cyan}-U, upgrade{self.endc}               Upgrade the installed packages with\n'
            f'{"":>28}dependencies.\n'
            f'  {self.cyan}-I, repo-info{self.endc}             Display the repositories information.\n'
            f'  {self.cyan}-g, configs{self.endc}               Edit the configuration file with dialog\n'
            f'{"":>28}utility.\n'
            f'  {self.cyan}-T, clean-tmp{self.endc}             Remove old downloaded packages and scripts.\n'
            f'  {self.cyan}-b, build{self.endc} <packages>      Build SBo scripts with dependencies without\n'
            f'{"":>28}install it.\n'
            f'  {self.cyan}-i, install{self.endc} <packages>    Build SBo scripts and install it with their\n'
            f'{"":>28}dependencies or install binary packages.\n'
            f'  {self.cyan}-R, remove{self.endc} <packages>     Remove installed packages with dependencies.\n'
            f'  {self.cyan}-d, download{self.endc} <packages>   Download only the packages without build\n'
            f'{"":>28}or install.\n'
            f'  {self.cyan}-f, find{self.endc} <packages>       Find and display the installed packages.\n'
            f'  {self.cyan}-w, view{self.endc} <packages>       Display package information by the repository.\n'
            f'  {self.cyan}-s, search{self.endc} <packages>     This will match each package by the repository.\n'
            f'  {self.cyan}-e, dependees{self.endc} <packages>  Display packages that depend on other packages.\n'
            f'  {self.cyan}-t, tracking{self.endc} <packages>   Display and tracking the packages dependencies.\n'
            f'\n{self.bold}OPTIONS:{self.endc}\n'
            f'  {self.yellow}-y, --yes{self.endc}                 Answer Yes to all questions.\n'
            f'  {self.yellow}-c, --check{self.endc}               Check a procedure before you run it, to be\n'
            f'{"":>28}used with update or upgrade commands.\n'
            f'  {self.yellow}-O, --resolve-off{self.endc}         Turns off dependency resolving.\n'
            f'  {self.yellow}-r, --reinstall{self.endc}           Upgrade packages of the same version.\n'
            f'  {self.yellow}-k, --skip-installed{self.endc}      Skip installed packages during the building\n'
            f'{"":>28}or installation progress.\n'
            f'  {self.yellow}-F, --fetch{self.endc}               Fetch the fastest and slower mirror.\n'
            f'{"":>28}To be used with repo-info command.\n'
            f'  {self.yellow}-E, --full-reverse{self.endc}        Display the full reverse dependency.\n'
            f'  {self.yellow}-S, --search{self.endc}              Search and load packages using the dialog.\n'
            f'  {self.yellow}-B, --progress-bar{self.endc}        Display static progress bar instead of\n'
            f'{"":>28}process execute.\n'
            f'  {self.yellow}-p, --pkg-version{self.endc}         Print the repository package version.\n'
            f'  {self.yellow}-P, --parallel{self.endc}            Enable download files in parallel.\n'
            f'  {self.yellow}-m, --no-case{self.endc}             Case-insensitive pattern matching.\n'
            f'  {self.yellow}-o, --repository={self.endc}NAME     Change repository you want to work.\n'
            f'  {self.yellow}-z, --directory={self.endc}PATH      Download files to a specific path.\n'
            '\n  -h, --help                Show this message and exit.\n'
            '  -v, --version             Print version and exit.\n'
            "\nIf you need more information try to use slpkg manpage.\n"
            "Edit the config file in the /etc/slpkg/slpkg.toml or 'slpkg configs'.")

        print(args)
        raise SystemExit(status)

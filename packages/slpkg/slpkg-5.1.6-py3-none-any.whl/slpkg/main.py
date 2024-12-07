#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os
import sys
import time
import logging
from pathlib import Path
from signal import signal, SIGPIPE, SIG_DFL

from slpkg.checks import Check
from slpkg.upgrade import Upgrade
from slpkg.configs import Configs
from slpkg.tracking import Tracking
from slpkg.load_data import LoadData
from slpkg.repo_info import RepoInfo
from slpkg.dependees import Dependees
from slpkg.utilities import Utilities
from slpkg.cleanings import Cleanings
from slpkg.search import SearchPackage
from slpkg.views.cli_menu import Usage
from slpkg.error_messages import Errors
from slpkg.views.version import Version
from slpkg.choose_packages import Choose
from slpkg.repositories import Repositories
from slpkg.binaries.install import Packages
from slpkg.dialog_configs import FormConfigs
from slpkg.check_updates import CheckUpdates
from slpkg.download_only import DownloadOnly
from slpkg.sbos.slackbuild import Slackbuilds
from slpkg.find_installed import FindInstalled
from slpkg.views.view_package import ViewPackage
from slpkg.remove_packages import RemovePackages
from slpkg.update_repositories import UpdateRepositories

signal(SIGPIPE, SIG_DFL)


class Menu(Configs):  # pylint: disable=[R0902]
    """Control cli options."""

    def __init__(self, args: list):  # pylint: disable=[R0915]
        super(Configs, self).__init__()

        self.args: list = args
        self.flags: list = []
        self.directory: str = str(self.tmp_slpkg)

        self.utils = Utilities()
        self.usage = Usage()
        self.repos = Repositories()

        self.repository: str = self.repos.default_repository

        self.data: dict = {}
        self.flag_yes: str = '--yes'
        self.flag_short_yes: str = '-y'
        self.flag_check: str = '-c'
        self.flag_short_check: str = '--check'
        self.flag_resolve_off: str = '--resolve-off'
        self.flag_short_resolve_off: str = '-O'
        self.flag_reinstall: str = '--reinstall'
        self.flag_short_reinstall: str = '-r'
        self.flag_skip_installed: str = '--skip-installed'
        self.flag_short_skip_installed: str = '-k'
        self.flag_full_reverse: str = '--full-reverse'
        self.flag_short_full_reverse: str = '-E'
        self.flag_search: str = '--search'
        self.flag_short_search: str = '-S'
        self.flag_for_progress_bar: str = '--progress-bar'
        self.flag_short_for_progress_bar: str = '-B'
        self.flag_pkg_version: str = '--pkg-version'
        self.flag_short_pkg_version: str = '-p'
        self.flag_parallel: str = '--parallel'
        self.flag_short_parallel: str = '-P'
        self.flag_no_case: str = '--no-case'
        self.flag_short_no_case: str = '-m'
        self.flag_repository: str = '--repository'
        self.flag_short_repository: str = '-o'
        self.flag_directory: str = '--directory'
        self.flag_short_directory: str = '-z'
        self.flag_fetch: str = '--fetch'
        self.flag_short_fetch: str = '-F'

        self.flag_searches: tuple = (
            self.flag_short_search,
            self.flag_search
        )

        self.options: tuple = (
            self.flag_yes,
            self.flag_short_yes,
            self.flag_check,
            self.flag_short_check,
            self.flag_resolve_off,
            self.flag_short_resolve_off,
            self.flag_reinstall,
            self.flag_short_reinstall,
            self.flag_skip_installed,
            self.flag_short_skip_installed,
            self.flag_full_reverse,
            self.flag_short_full_reverse,
            self.flag_search,
            self.flag_short_search,
            self.flag_for_progress_bar,
            self.flag_short_for_progress_bar,
            self.flag_pkg_version,
            self.flag_short_pkg_version,
            self.flag_parallel,
            self.flag_short_parallel,
            self.flag_no_case,
            self.flag_short_no_case,
            self.flag_repository,
            self.flag_short_repository,
            self.flag_directory,
            self.flag_short_directory,
            self.flag_fetch,
            self.flag_short_fetch
        )

        self.commands: dict = {
            '--help': [],
            '--version': [],
            'help': [],
            'update': [
                self.flag_yes,
                self.flag_short_yes,
                self.flag_check,
                self.flag_short_check,
                self.flag_repository,
                self.flag_short_repository,
                self.flag_parallel,
                self.flag_short_parallel
            ],
            'upgrade': [
                self.flag_yes,
                self.flag_short_yes,
                self.flag_check,
                self.flag_short_check,
                self.flag_resolve_off,
                self.flag_short_resolve_off,
                self.flag_reinstall,
                self.flag_short_reinstall,
                self.flag_for_progress_bar,
                self.flag_short_for_progress_bar,
                self.flag_repository,
                self.flag_short_repository,
                self.flag_parallel,
                self.flag_short_parallel
            ],
            'repo-info': [
                self.flag_repository,
                self.flag_short_repository,
                self.flag_fetch,
                self.flag_short_fetch
            ],
            'configs': [],
            'clean-tmp': [],
            'build': [
                self.flag_yes,
                self.flag_short_yes,
                self.flag_resolve_off,
                self.flag_short_resolve_off,
                self.flag_search,
                self.flag_short_search,
                self.flag_for_progress_bar,
                self.flag_short_for_progress_bar,
                self.flag_repository,
                self.flag_short_repository,
                self.flag_parallel,
                self.flag_short_parallel,
                self.flag_no_case,
                self.flag_short_no_case
            ],
            'install': [
                self.flag_yes,
                self.flag_short_yes,
                self.flag_resolve_off,
                self.flag_short_resolve_off,
                self.flag_reinstall,
                self.flag_short_reinstall,
                self.flag_skip_installed,
                self.flag_short_skip_installed,
                self.flag_search,
                self.flag_short_search,
                self.flag_for_progress_bar,
                self.flag_short_for_progress_bar,
                self.flag_repository,
                self.flag_short_repository,
                self.flag_parallel,
                self.flag_short_parallel,
                self.flag_no_case,
                self.flag_short_no_case
            ],
            'download': [
                self.flag_yes,
                self.flag_short_yes,
                self.flag_search,
                self.flag_short_search,
                self.flag_directory,
                self.flag_short_directory,
                self.flag_repository,
                self.flag_short_repository,
                self.flag_parallel,
                self.flag_short_parallel,
                self.flag_no_case,
                self.flag_short_no_case,
            ],
            'remove': [
                self.flag_yes,
                self.flag_short_yes,
                self.flag_resolve_off,
                self.flag_short_resolve_off,
                self.flag_search,
                self.flag_short_search,
                self.flag_for_progress_bar,
                self.flag_short_for_progress_bar
            ],
            'find': [
                self.flag_search,
                self.flag_short_search,
                self.flag_no_case,
                self.flag_short_no_case
            ],
            'view': [
                self.flag_search,
                self.flag_short_search,
                self.flag_repository,
                self.flag_short_repository,
                self.flag_pkg_version,
                self.flag_short_pkg_version,
                self.flag_no_case,
                self.flag_short_no_case
            ],
            'search': [
                self.flag_search,
                self.flag_short_search,
                self.flag_repository,
                self.flag_short_repository,
                self.flag_pkg_version,
                self.flag_short_pkg_version,
                self.flag_no_case,
                self.flag_short_no_case
            ],
            'dependees': [
                self.flag_full_reverse,
                self.flag_short_full_reverse,
                self.flag_search,
                self.flag_short_search,
                self.flag_repository,
                self.flag_short_repository,
                self.flag_pkg_version,
                self.flag_short_pkg_version,
                self.flag_no_case,
                self.flag_short_no_case
            ],
            'tracking': [
                self.flag_search,
                self.flag_short_search,
                self.flag_pkg_version,
                self.flag_short_pkg_version,
                self.flag_repository,
                self.flag_short_repository,
                self.flag_no_case,
                self.flag_short_no_case,
                self.flag_resolve_off,
                self.flag_short_resolve_off
            ]
        }

        self.commands['-h'] = self.commands['--help']
        self.commands['-v'] = self.commands['--version']
        self.commands['-u'] = self.commands['update']
        self.commands['-U'] = self.commands['upgrade']
        self.commands['-I'] = self.commands['repo-info']
        self.commands['-g'] = self.commands['configs']
        self.commands['-T'] = self.commands['clean-tmp']
        self.commands['-b'] = self.commands['build']
        self.commands['-i'] = self.commands['install']
        self.commands['-d'] = self.commands['download']
        self.commands['-R'] = self.commands['remove']
        self.commands['-f'] = self.commands['find']
        self.commands['-w'] = self.commands['view']
        self.commands['-s'] = self.commands['search']
        self.commands['-e'] = self.commands['dependees']
        self.commands['-t'] = self.commands['tracking']

        self.split_options()
        self.split_options_from_args()
        self.move_options()
        self.invalid_options()
        self.check_for_repositories()
        self.load_data = LoadData(self.flags)

        self.check = Check(self.repository)
        self.choose = Choose(self.repository)

    def check_for_repositories(self) -> None:
        """Check a combination for binaries use repositories only and if repository exists."""
        except_options: tuple = (
            '-s', 'search',
            '-U', 'upgrade'
        )
        if self.repository == '*' and not self.utils.is_option(except_options, self.args):
            self.usage.help_minimal(f"{self.prog_name}: invalid repository '{self.repository}'")

        elif self.repository not in self.repos.repositories and self.repository != '*':
            self.usage.help_minimal(f"{self.prog_name}: invalid repository '{self.repository}'")

        if self.repository != '*':
            if not self.repos.repositories[self.repository]['enable']:
                self.usage.help_minimal(f"{self.prog_name}: repository '{self.repository}' is disabled")

    def invalid_options(self) -> None:
        """Check for invalid options."""
        invalid, commands, repeat = [], [], []

        for arg in self.args:
            if arg[0] == '-' and arg in self.commands:
                commands.append(arg)
            elif arg[0] == '-' and arg not in self.options:
                invalid.append(arg)

        # Counts the recurring options.
        for opt in self.flags:
            if self.flags.count(opt) > 1:
                repeat.append(opt)

        # Fixed for recurring options.
        if repeat:
            self.usage.help_minimal(f"{self.prog_name}: invalid recurring options '{', '.join(repeat)}'")

        # Fixed for an invalid commands combination.
        if len(commands) > 1:
            self.usage.help_minimal(f"{self.prog_name}: invalid commands combination '{', '.join(commands)}'")

        # Fixed for correct options by command.
        try:
            options: list = self.commands[self.args[0]]
            for opt in self.flags:
                if opt not in options:
                    invalid.append(opt)
        except (KeyError, IndexError):
            self.usage.help_short(1)

        # Prints error for invalid options.
        if invalid:
            self.usage.help_minimal(f"{self.prog_name}: invalid options '{','.join(invalid)}'")

    def split_options(self) -> None:
        """Split options and commands.

        Put the command first and options after.
        """
        for args in self.args:
            if args[0] == '-' and args[:2] != '--' and len(args) >= 3 and '=' not in args:
                self.args.remove(args)

                for opt in map(lambda x: f'-{x}', list(args[1:])):
                    if opt in self.commands:
                        self.args.insert(0, opt)
                        continue

                    self.args.append(opt)

    def split_options_from_args(self) -> None:
        """Split options from arguments.

        slpkg -d package --directory=/path/to/download
        Split the option ['--directory'] and ['/path/to/download/'].
        """
        remove_args: list = []

        for arg in self.args:
            split_arg: list = arg.split('=')

            if len(split_arg) > 1:

                if split_arg[0] == self.flag_directory:
                    self.directory: str = split_arg[1]
                    remove_args.append(arg)
                    self.args.append(self.flag_directory)

                if split_arg[0] == self.flag_repository:
                    self.repository = split_arg[1]
                    remove_args.append(arg)
                    self.args.append(self.flag_repository)

            try:
                if arg == self.flag_short_directory:
                    self.directory: str = self.args[self.args.index(arg) + 1]
                    remove_args.append(self.directory)
            except IndexError:
                self.directory: str = ''

            try:
                if arg == self.flag_short_repository:
                    self.repository: str = self.args[self.args.index(arg) + 1]
                    remove_args.append(self.repository)
            except IndexError:
                self.repository: str = ''

        for arg in remove_args:
            if arg in self.args:
                self.args.remove(arg)

    def move_options(self) -> None:
        """Move options to the flags and removes from the arguments."""
        new_args: list = []

        for arg in self.args:
            if arg in self.options:
                self.flags.append(arg)
            else:
                new_args.append(arg)

        self.args: list = new_args

    def is_file_list_packages(self) -> list:
        """Check if the arg is filelist.pkgs."""
        if self.args[1].endswith(self.file_list_suffix):
            file = Path(self.args[1])
            packages: list = list(self.utils.read_packages_from_file(file))
        else:
            packages: list = list(set(self.args[1:]))

        return packages

    def update(self) -> None:
        """Update the local repositories.

        Raises:
            SystemExit: Exit code 0.
        """
        if len(self.args) == 1:
            if self.utils.is_option((self.flag_check, self.flag_short_check), self.flags):
                check = CheckUpdates(self.flags, self.repository)
                check.updates()
            else:
                start: float = time.time()
                update = UpdateRepositories(self.flags, self.repository)
                update.repositories()
                elapsed_time: float = time.time() - start
                self.utils.finished_time(elapsed_time)
            raise SystemExit(0)
        self.usage.help_short(1)

    def upgrade(self) -> None:  # pylint: disable=[R0912]
        """Upgrade the installed packages.

        Raises:
            SystemExit: Exit code 0.
        """
        command: str = Menu.upgrade.__name__
        removed: list = []
        added: list = []
        ordered: bool = True
        kernel_generic_current_package: str = self.utils.is_package_installed('kernel-generic')

        if len(self.args) == 1:

            if self.utils.is_option((self.flag_check, self.flag_short_check), self.flags):
                self.data: dict = self.load_data.load(self.repository)
                upgrade = Upgrade(self.repository, self.data)
                upgrade.check_packages()

            elif self.repository != '*':
                self.data: dict = self.load_data.load(self.repository)
                upgrade = Upgrade(self.repository, self.data)
                packages: list = list(upgrade.packages())

                for package in packages:
                    if package.endswith('_Removed.'):
                        removed.append(package.replace('_Removed.', ''))
                    if package.endswith('_Added.'):
                        added.append(package.replace('_Added.', ''))

                # Remove packages that not exists in the repository.
                if removed:
                    packages = [pkg for pkg in packages if not pkg.endswith('_Removed.')]
                    remove = RemovePackages(removed, self.flags)
                    remove.remove(upgrade=True)

                # If new packages are added to the repository, the sorted list will be disabled
                # and the new packages will be pushed to the front of the list to be installed first.
                if added:
                    packages = [pkg for pkg in packages if not pkg.endswith('_Added.')]
                    packages: list = added + packages
                    ordered: bool = False

                packages: list = self.choose.packages(self.data, packages, command, ordered)

                if not packages:
                    print('\nEverything is up-to-date!\n')
                    raise SystemExit(0)

                if self.repository not in [self.repos.sbo_repo_name, self.repos.ponce_repo_name]:
                    install_bin = Packages(
                        self.repository, self.data, packages, self.flags, mode=command)
                    install_bin.execute()
                else:
                    install_sbo = Slackbuilds(
                        self.repository, self.data, packages, self.flags, mode=command)
                    install_sbo.execute()
            else:
                self.usage.help_minimal(f"{self.prog_name}: invalid repository '{self.repository}'")

            self._is_kernel_upgrade(kernel_generic_current_package)

            raise SystemExit(0)
        self.usage.help_short(1)

    def _is_kernel_upgrade(self, kernel_generic_current_package: str) -> None:
        """Compare current and installed kernel package.

        Args:
            kernel_generic_current_package (str): Kernel-generic package
        """
        kernel_generic_new_package: str = self.utils.is_package_installed('kernel-generic')
        if kernel_generic_current_package != kernel_generic_new_package:
            self._kernel_image_message()

    def _kernel_image_message(self) -> None:
        """Print a warning kernel upgrade message.
        """
        print(f"\n{self.bred}Warning!{self.endc} Your kernel image looks like to have been upgraded!\n"
              "Please update the bootloader with the new parameters of the upgraded kernel.\n"
              "See: lilo, eliloconfig or grub-mkconfig -o /boot/grub/grub.cfg,\n"
              "depending on how you have your system configured.\n")

    def repo_info(self) -> None:
        """Print repositories information.

        Raises:
            SystemExit: Exit code 0.
        """
        if len(self.args) == 1:
            repo = RepoInfo(self.flags, self.repository)
            repo.info()
            raise SystemExit(0)
        self.usage.help_short(1)

    def build(self) -> None:
        """Build slackbuilds with dependencies without install.

        Raises:
            SystemExit: Exit code 0.
        """
        command: str = Menu.build.__name__

        if len(self.args) >= 2:
            self.data: dict = self.load_data.load(self.repository)
            packages: list = self.is_file_list_packages()
            packages: list = self.utils.case_insensitive_pattern_matching(packages, self.data, self.flags)

            if self.utils.is_option(self.flag_searches, self.flags):
                packages: list = self.choose.packages(self.data, packages, command)

            self.check.package_exists_in_the_database(packages, self.data)

            if self.repository in list(self.repos.repositories)[:2]:
                build = Slackbuilds(
                    self.repository, self.data, packages, self.flags, mode=command
                )
                build.execute()
            else:
                self.usage.help_minimal(f"{self.prog_name}: invalid repository '{self.repository}'")

            raise SystemExit(0)
        self.usage.help_short(1)

    def install(self) -> None:
        """Build and install packages with dependencies.

        Raises:
            SystemExit: Exit code 0.
        """
        command: str = Menu.install.__name__
        kernel_generic_current_package: str = self.utils.is_package_installed('kernel-generic')

        if len(self.args) >= 2:
            self.data: dict = self.load_data.load(self.repository)
            packages: list = self.is_file_list_packages()
            packages: list = self.utils.case_insensitive_pattern_matching(packages, self.data, self.flags)

            if self.utils.is_option(self.flag_searches, self.flags):
                packages: list = self.choose.packages(self.data, packages, command)

            self.check.package_exists_in_the_database(packages, self.data)

            if self.repository not in [self.repos.sbo_repo_name, self.repos.ponce_repo_name]:
                install_bin = Packages(self.repository, self.data, packages, self.flags, mode=command)
                install_bin.execute()
            else:
                install_sbo = Slackbuilds(self.repository, self.data, packages, self.flags, mode=command)
                install_sbo.execute()

            self._is_kernel_upgrade(kernel_generic_current_package)

            raise SystemExit(0)
        self.usage.help_short(1)

    def download(self) -> None:
        """Download only packages.

        Raises:
            SystemExit: Exit code 0.
        """
        command: str = Menu.download.__name__

        if len(self.args) >= 2:
            self.data: dict = self.load_data.load(self.repository)
            packages: list = self.is_file_list_packages()
            packages: list = self.utils.case_insensitive_pattern_matching(packages, self.data, self.flags)

            if self.utils.is_option(self.flag_searches, self.flags):
                packages: list = self.choose.packages(self.data, packages, command)

            self.check.package_exists_in_the_database(packages, self.data)
            down_only = DownloadOnly(self.directory, self.flags, self.data, self.repository)
            down_only.packages(packages)
            raise SystemExit(0)
        self.usage.help_short(1)

    def remove(self) -> None:
        """Remove packages with dependencies.

        Raises:
            SystemExit: Exit code 0.
        """
        command: str = Menu.remove.__name__

        if len(self.args) >= 2:
            packages: list = self.is_file_list_packages()

            if self.utils.is_option(self.flag_searches, self.flags):
                packages: list = self.choose.packages(self.data, packages, command)

            self.check.is_package_installed(packages)

            remove = RemovePackages(packages, self.flags)
            remove.remove()
            raise SystemExit(0)
        self.usage.help_short(1)

    def find(self) -> None:
        """Find installed packages.

        Raises:
            SystemExit: Exit code 0.
        """
        command: str = Menu.find.__name__

        if len(self.args) >= 2:
            packages: list = self.is_file_list_packages()
            self.data: dict = self.load_data.load(self.repository)
            packages: list = self.utils.case_insensitive_pattern_matching(packages, self.data, self.flags)

            if self.utils.is_option(self.flag_searches, self.flags):
                packages: list = self.choose.packages(self.data, packages, command)

            find = FindInstalled(self.flags, packages)
            find.find()
            raise SystemExit(0)
        self.usage.help_short(1)

    def view(self) -> None:
        """View package information.

        Raises:
            SystemExit: Exit code 0.
        """
        command: str = Menu.view.__name__

        if len(self.args) >= 2:
            self.data: dict = self.load_data.load(self.repository)
            packages: list = self.is_file_list_packages()
            packages: list = self.utils.case_insensitive_pattern_matching(packages, self.data, self.flags)

            if self.utils.is_option(self.flag_searches, self.flags):
                packages: list = self.choose.packages(self.data, packages, command)

            self.check.package_exists_in_the_database(packages, self.data)

            view = ViewPackage(self.flags, self.repository)

            if self.repository not in [self.repos.sbo_repo_name, self.repos.ponce_repo_name]:
                view.package(self.data, packages)
            else:
                view.slackbuild(self.data, packages)
            raise SystemExit(0)
        self.usage.help_short(1)

    def search(self) -> None:
        """Search packages from the repositories.

        Raises:
            SystemExit: Exit code 0.
        """
        command: str = Menu.search.__name__
        self.data: dict = self.load_data.load(self.repository)

        if len(self.args) >= 2:
            packages: list = self.is_file_list_packages()

            if self.utils.is_option(self.flag_searches, self.flags):
                packages: list = self.choose.packages(self.data, packages, command)

            pkgs = SearchPackage(self.flags, packages, self.data, self.repository)
            pkgs.search()
            raise SystemExit(0)
        self.usage.help_short(1)

    def dependees(self) -> None:
        """View packages that depend on other packages.

        Raises:
            SystemExit: Exit code 0.
        """
        command: str = Menu.dependees.__name__

        if len(self.args) >= 2:
            self.data: dict = self.load_data.load(self.repository)
            packages: list = self.is_file_list_packages()
            packages: list = self.utils.case_insensitive_pattern_matching(packages, self.data, self.flags)

            if self.utils.is_option(self.flag_searches, self.flags):
                packages: list = self.choose.packages(self.data, packages, command)

            self.check.package_exists_in_the_database(packages, self.data)

            dependees = Dependees(self.data, packages, self.flags)
            dependees.find()
            raise SystemExit(0)
        self.usage.help_short(1)

    def tracking(self) -> None:
        """Tracking package dependencies.

        Raises:
            SystemExit: Exit code 0.
        """
        command: str = Menu.tracking.__name__

        if len(self.args) >= 2:
            self.data: dict = self.load_data.load(self.repository)
            packages: list = self.is_file_list_packages()
            packages: list = self.utils.case_insensitive_pattern_matching(packages, self.data, self.flags)

            if self.utils.is_option(self.flag_searches, self.flags):
                packages: list = self.choose.packages(self.data, packages, command)

            self.check.package_exists_in_the_database(packages, self.data)

            tracking = Tracking(self.data, packages, self.flags, self.repository)
            tracking.package()
            raise SystemExit(0)
        self.usage.help_short(1)


class SubMenu:
    """Submenu that separate from the main menu.

    Because of have no options to manage here.
    """

    def __init__(self, args: list):
        self.args: list = args
        self.usage = Usage()
        self.form_configs = FormConfigs()
        self.clean = Cleanings()

    def help(self) -> None:
        """Print help menu and exit."""
        if len(self.args) == 1:
            self.usage.help(0)
        self.usage.help_short(1)

    def version(self) -> None:
        """Print program version and exit.

        Raises:
            SystemExit: Exit code 0.
        """
        if len(self.args) == 1:
            version = Version()
            version.view()
            raise SystemExit(0)
        self.usage.help_short(1)

    def edit_configs(self) -> None:
        """Edit configurations via dialog box.

        Raises:
            SystemExit: Exit code 0.
        """
        if len(self.args) == 1:
            self.form_configs.edit()
            raise SystemExit(0)
        self.usage.help_short(1)

    def clean_tmp(self) -> None:
        """Remove all files and directories from tmp.

        Raises:
            SystemExit: Exit code 0.
        """
        if len(self.args) == 1:
            self.clean.tmp()
            raise SystemExit(0)
        self.usage.help_short(1)


def main() -> None:
    """Call options and commands.

    Raises:
        SystemExit: Exit code 0.
    """
    error = Errors()

    if not os.geteuid() == 0:
        error.raise_error_message(message='Must run as root.', exit_status=1)

    # Configure logging
    if Configs.error_log_file.is_file():
        Configs.error_log_file.unlink()

    logging.basicConfig(filename=Configs.error_log_file,
                        level=logging.ERROR,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    args: list = sys.argv
    args.pop(0)
    usage = Usage()

    if len(args) == 0 or '' in args:
        usage.help_short(1)

    sub_menu = SubMenu(args)
    arguments_no_options: dict = {
        '-h': sub_menu.help,
        '--help': sub_menu.help,
        '-v': sub_menu.version,
        '--version': sub_menu.version,
        'configs': sub_menu.edit_configs,
        '-g': sub_menu.edit_configs,
        'clean-tmp': sub_menu.clean_tmp,
        '-T': sub_menu.clean_tmp
    }

    try:
        arguments_no_options[args[0]]()
    except (KeyError, IndexError):
        pass
    except KeyboardInterrupt as e:
        raise SystemExit(1) from e

    menu = Menu(args)
    arguments: dict = {
        'update': menu.update,
        '-u': menu.update,
        'upgrade': menu.upgrade,
        '-U': menu.upgrade,
        'repo-info': menu.repo_info,
        '-I': menu.repo_info,
        'build': menu.build,
        '-b': menu.build,
        'install': menu.install,
        '-i': menu.install,
        'download': menu.download,
        '-d': menu.download,
        'remove': menu.remove,
        '-R': menu.remove,
        'view': menu.view,
        '-w': menu.view,
        'find': menu.find,
        '-f': menu.find,
        'search': menu.search,
        '-s': menu.search,
        'dependees': menu.dependees,
        '-e': menu.dependees,
        'tracking': menu.tracking,
        '-t': menu.tracking
    }

    try:
        arguments[args[0]]()
    except KeyError:
        logging.error("Exception occurred", exc_info=True)
        error.raise_error_message(message='Something went wrong, check the log file.', exit_status=1)
    except IndexError:
        usage.help_short(1)
    except KeyboardInterrupt as e:
        raise SystemExit(1) from e


if __name__ == '__main__':
    main()

#!/usr/bin/python3
# -*- coding: utf-8 -*-


import re
import subprocess
from pathlib import Path

from slpkg.configs import Configs
from slpkg.views.views import View
from slpkg.utilities import Utilities
from slpkg.downloader import Downloader
from slpkg.install_data import InstallData
from slpkg.repositories import Repositories
from slpkg.multi_process import MultiProcess
from slpkg.check_updates import CheckUpdates
from slpkg.sbos.sbo_generate import SBoGenerate


class UpdateRepositories(Configs):  # pylint: disable=[R0902]
    """Update the local repositories."""

    def __init__(self, flags: list, repository: str):
        super(Configs, self).__init__()

        self.view = View(flags)
        self.multi_process = MultiProcess(flags)
        self.repos = Repositories()
        self.utils = Utilities()
        self.data = InstallData()
        self.generate = SBoGenerate()
        self.check_updates = CheckUpdates(flags, repository)
        self.download = Downloader(flags)

        self.repos_for_update: dict = {}

        self.option_for_yes: bool = self.utils.is_option(
            ('-y', '--yes'), flags)

    def repositories(self) -> None:
        """Check and call the repositories for update."""
        self.repos_for_update: dict = self.check_updates.updates()

        if not any(list(self.repos_for_update.values())):
            self.view.question(message='Do you want to force update?')
            # Force update the repositories.
            for repo in self.repos_for_update:
                self.repos_for_update[repo] = True

        self.run_update()

    def import_gpg_key(self, repo: str) -> None:
        """Import the GPG KEY.

        Args:
            mirror (str): Repository GPG mirror key.
        """
        if self.gpg_verification:
            mirror: str = self.repos.repositories[repo]['mirror_changelog']

            if repo == self.repos.sbo_repo_name:
                mirror: str = 'https://www.slackbuilds.org/'

            gpg_key: str = f'{mirror}GPG-KEY'
            gpg_command: str = 'gpg --fetch-key'
            process: str = ''

            try:
                process = subprocess.run(f'{gpg_command} {gpg_key}', shell=True, stdout=subprocess.PIPE,
                                         stderr=subprocess.STDOUT, encoding='utf-8', text=True, check=True)
            except subprocess.CalledProcessError:
                mirror: str = self.repos.repositories[repo]['mirror_packages']
                gpg_key: str = f'{mirror}GPG-KEY'

                try:
                    process = subprocess.run(f'{gpg_command} {gpg_key}', shell=True, stdout=subprocess.PIPE,
                                             stderr=subprocess.STDOUT, encoding='utf-8', text=True, check=True)
                except subprocess.CalledProcessError:
                    print(f'Getting GPG key: {self.bred}Failed{self.endc}')
                    if not self.option_for_yes and self.ask_question:
                        self.view.question()
                        return

            output: str = re.split(r"/|\s", process.stdout)
            if process.returncode == 0 and 'imported:' in output:
                print(f'Getting GPG key from: {mirror}\n')

    def run_update(self) -> None:
        """Update the repositories by category."""
        for repo, update in self.repos_for_update.items():
            if update:

                self.view_downloading_message(repo)
                if repo in [self.repos.sbo_repo_name, self.repos.ponce_repo_name]:
                    self.update_slackbuild_repos(repo)
                else:
                    self.update_binary_repos(repo)

    def view_downloading_message(self, repo: str) -> None:
        """Print the syncing message.

        Args:
            repo (str): Repository name.
        """
        print(f"Syncing with the repository '{self.green}{repo}{self.endc}', please wait...\n")

    def update_binary_repos(self, repo: str) -> None:
        """Update the binary repositories.

        Args:
            repo (str): Repository name.
        """
        urls: dict = {}

        self.import_gpg_key(repo)

        changelog: str = (f"{self.repos.repositories[repo]['mirror_changelog']}"
                          f"{self.repos.repositories[repo]['changelog_txt']}")
        packages: str = (f"{self.repos.repositories[repo]['mirror_packages']}"
                         f"{self.repos.repositories[repo]['packages_txt']}")
        checksums: str = (f"{self.repos.repositories[repo]['mirror_packages']}"
                          f"{self.repos.repositories[repo]['checksums_md5']}")

        urls[repo] = ((changelog, packages, checksums), self.repos.repositories[repo]['path'])

        self.utils.remove_file_if_exists(self.repos.repositories[repo]['path'],
                                         self.repos.repositories[repo]['changelog_txt'])
        self.utils.remove_file_if_exists(self.repos.repositories[repo]['path'],
                                         self.repos.repositories[repo]['packages_txt'])
        self.utils.remove_file_if_exists(self.repos.repositories[repo]['path'],
                                         self.repos.repositories[repo]['checksums_md5'])

        self.utils.create_directory(self.repos.repositories[repo]['path'])

        self.download.download(urls)

        self.data.install_binary_data(repo)

    def update_slackbuild_repos(self, repo: str) -> None:
        """Update the slackbuild repositories.

        Args:
            repo (str): Repository name.
        """
        self.import_gpg_key(repo)

        mirror: str = self.repos.repositories[repo]['mirror_packages']

        git_mirror: dict = {
            self.repos.sbo_repo_name: self.repos.sbo_git_mirror,
            self.repos.ponce_repo_name: self.repos.ponce_git_mirror
        }

        repo_path: Path = self.repos.repositories[repo]['path']

        if '.git' in git_mirror[repo]:
            self.utils.remove_folder_if_exists(repo_path)
            syncing_command: str = f"{self.git_clone} {git_mirror[repo]} {repo_path}"
        else:
            self.utils.remove_file_if_exists(repo_path, self.repos.repositories[repo]['slackbuilds_txt'])
            self.utils.remove_file_if_exists(repo_path, self.repos.repositories[repo]['changelog_txt'])
            self.utils.create_directory(repo_path)
            syncing_command: str = f"lftp {self.lftp_mirror_options} {mirror} {repo_path}"

        self.multi_process.process(syncing_command)

        # It checks if there is a SLACKBUILDS.TXT file, otherwise it's going to create one.
        if not Path(self.repos.repositories[repo]['path'],
                    self.repos.repositories[repo]['slackbuilds_txt']).is_file():
            if '.git' in git_mirror[repo]:
                print()
            self.generate.slackbuild_file(self.repos.repositories[repo]['path'],
                                          self.repos.repositories[repo]['slackbuilds_txt'])

        self.data.install_sbo_data(repo)

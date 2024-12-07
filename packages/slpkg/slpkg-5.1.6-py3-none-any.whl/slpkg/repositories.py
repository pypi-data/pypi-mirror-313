#!/usr/bin/python3
# -*- coding: utf-8 -*-


from pathlib import Path
from typing import ClassVar
from dataclasses import dataclass
from urllib.parse import urlparse
import tomlkit

from slpkg.configs import Configs
from slpkg.utilities import Utilities
from slpkg.toml_errors import TomlErrors


@dataclass
class Repositories:  # pylint: disable=[R0902]
    """Repositories configurations."""

    toml_errors = TomlErrors()
    utils = Utilities()

    repositories_toml_file: Path = Path(Configs.etc_path, 'repositories.toml')
    repositories_path: Path = Path(Configs.lib_path, 'repos')

    repos_config = {}
    repositories = {}
    repos_toml = {}

    data_json: str = 'data.json'
    repos_information: Path = Path(repositories_path, 'repos_information.json')
    default_repository: str = 'sbo'

    slackbuilds_txt: str = 'SLACKBUILDS.TXT'
    packages_txt: str = 'PACKAGES.TXT'
    checksums_md5: str = 'CHECKSUMS.md5'
    changelog_txt: str = 'ChangeLog.txt'

    sbo_repo: bool = True
    sbo_repo_name: str = 'sbo'
    sbo_repo_path: Path = Path(repositories_path, sbo_repo_name)
    sbo_repo_mirror: str = ''
    sbo_repo_tag: str = '_SBo'
    sbo_repo_tar_suffix: str = '.tar.gz'

    ponce_repo: bool = False
    ponce_repo_name: str = 'ponce'
    ponce_repo_path: Path = Path(repositories_path, ponce_repo_name)
    ponce_repo_mirror: str = ''
    ponce_repo_tag: str = '_SBo'
    ponce_repo_tar_suffix: str = '.tar.gz'

    slack_repo: bool = False
    slack_repo_name: str = 'slack'
    slack_repo_path: Path = Path(repositories_path, slack_repo_name)
    slack_repo_mirror: str = ''
    slack_repo_tag: str = ''

    slack_extra_repo: bool = False
    slack_extra_repo_name: str = 'slack_extra'
    slack_extra_repo_path: Path = Path(repositories_path, slack_extra_repo_name)
    slack_extra_repo_mirror_packages: str = ''
    slack_extra_repo_mirror_changelog: str = ''
    slack_extra_repo_tag: str = ''

    slack_patches_repo: bool = False
    slack_patches_repo_name: str = 'slack_patches'
    slack_patches_repo_path: Path = Path(repositories_path, slack_patches_repo_name)
    slack_patches_repo_mirror_packages: str = ''
    slack_patches_repo_mirror_changelog: str = ''
    slack_patches_repo_tag: str = ''

    alien_repo: bool = False
    alien_repo_name: str = 'alien'
    alien_repo_path: Path = Path(repositories_path, alien_repo_name)
    alien_repo_mirror_packages: str = ''
    alien_repo_mirror_changelog: str = ''
    alien_repo_tag: str = 'alien'

    multilib_repo: bool = False
    multilib_repo_name: str = 'multilib'
    multilib_repo_path: Path = Path(repositories_path, multilib_repo_name)
    multilib_repo_mirror_packages: str = ''
    multilib_repo_mirror_changelog: str = ''
    multilib_repo_tag: str = 'alien'

    restricted_repo: bool = False
    restricted_repo_name: str = 'restricted'
    restricted_repo_path: Path = Path(repositories_path, restricted_repo_name)
    restricted_repo_mirror_packages: str = ''
    restricted_repo_mirror_changelog: str = ''
    restricted_repo_tag: str = 'alien'

    gnome_repo: bool = False
    gnome_repo_name: str = 'gnome'
    gnome_repo_path: Path = Path(repositories_path, gnome_repo_name)
    gnome_repo_mirror: str = ''
    gnome_repo_tag: str = 'gfs'

    msb_repo: bool = False
    msb_repo_name: str = 'msb'
    msb_repo_path: Path = Path(repositories_path, msb_repo_name)
    msb_repo_mirror_packages: str = ''
    msb_repo_mirror_changelog: str = ''
    msb_repo_tag: str = 'msb'

    csb_repo: bool = False
    csb_repo_name: str = 'csb'
    csb_repo_path: Path = Path(repositories_path, csb_repo_name)
    csb_repo_mirror: str = ''
    csb_repo_tag: str = 'csb'

    conraid_repo: bool = False
    conraid_repo_name: str = 'conraid'
    conraid_repo_path: Path = Path(repositories_path, conraid_repo_name)
    conraid_repo_mirror: str = ''
    conraid_repo_tag: str = 'cf'

    slackonly_repo: bool = False
    slackonly_repo_name: str = 'slackonly'
    slackonly_repo_path: Path = Path(repositories_path, slackonly_repo_name)
    slackonly_repo_mirror: str = ''
    slackonly_repo_tag: str = 'slonly'

    salix_repo: bool = False
    salix_repo_name: str = 'salix'
    salix_repo_path: Path = Path(repositories_path, salix_repo_name)
    salix_repo_mirror: str = ''
    salix_repo_tag: str = ''

    salix_extra_repo: bool = False
    salix_extra_repo_name: str = 'salix_extra'
    salix_extra_repo_path: Path = Path(repositories_path, salix_extra_repo_name)
    salix_extra_repo_mirror: str = ''
    salix_extra_repo_tag: str = ''

    slackel_repo: bool = False
    slackel_repo_name: str = 'slackel'
    slackel_repo_path: Path = Path(repositories_path, slackel_repo_name)
    slackel_repo_mirror: str = ''
    slackel_repo_tag: str = 'dj'

    slint_repo: bool = False
    slint_repo_name: str = 'slint'
    slint_repo_path: Path = Path(repositories_path, slint_repo_name)
    slint_repo_mirror: str = ''
    slint_repo_tag: str = 'slint'

    pprkut_repo: bool = False
    pprkut_repo_name: str = 'pprkut'
    pprkut_repo_path: Path = Path(repositories_path, pprkut_repo_name)
    pprkut_repo_mirror: str = ''
    pprkut_repo_tag: str = 'pprkut'

    try:
        if repositories_toml_file.is_file():
            with open(repositories_toml_file, 'r', encoding='utf-8') as file:
                repos_config = tomlkit.parse(file.read())

            default_repository: str = repos_config['DEFAULT']['REPOSITORY'].lower()

            new_packages = repos_config['NEW_PACKAGES']['REPOSITORIES']
            remove_packages = repos_config['REMOVE_PACKAGES']['REPOSITORIES']

            sbo_repo: bool = repos_config['SBO']['ENABLE']
            sbo_repo_mirror: str = repos_config['SBO']['MIRROR']
            sbo_git_mirror: str = sbo_repo_mirror
            if sbo_repo_mirror.endswith('.git'):
                # https://raw.githubusercontent.com/{owner}/{repository}/{branch}/{path_to_file}
                # https://gitlab.com/{owner}/{repository}/-/raw/{branch}/{path_to_file}
                parsed_url = urlparse(sbo_git_mirror)
                path_parts = parsed_url.path.strip("/").split("/")
                owner = path_parts[0]
                repository_name: str = path_parts[1].replace('.git', '')
                if 'github.com' in sbo_git_mirror and Path(sbo_repo_path, '.git/').is_dir():
                    branch: str = utils.get_git_branch(sbo_repo_path)
                    sbo_repo_mirror: str = f'https://raw.githubusercontent.com/{owner}/{repository_name}/{branch}/'

                if 'gitlab.com' in sbo_git_mirror and Path(sbo_repo_path, '.git/').is_dir():
                    branch: str = utils.get_git_branch(sbo_repo_path)
                    sbo_repo_mirror: str = f'https://gitlab.com/{owner}/{repository_name}/-/raw/{branch}/'

            ponce_repo: bool = repos_config['PONCE']['ENABLE']
            ponce_repo_mirror: str = repos_config['PONCE']['MIRROR']
            ponce_git_mirror: str = ponce_repo_mirror
            if ponce_repo_mirror.endswith('.git'):
                # https://raw.githubusercontent.com/{owner}/{repository}/{branch}/{path_to_file}
                # https://gitlab.com/{owner}/{repository}/-/raw/{branch}/{path_to_file}
                parsed_url = urlparse(ponce_git_mirror)
                path_parts = parsed_url.path.strip("/").split("/")
                owner = path_parts[0]
                repository_name: str = path_parts[1].replace('.git', '')

                if 'github.com' in ponce_git_mirror and Path(ponce_repo_path, '.git/').is_dir():
                    branch: str = utils.get_git_branch(ponce_repo_path)
                    ponce_repo_mirror: str = f'https://raw.githubusercontent.com/{owner}/{repository_name}/{branch}/'

                if 'gitlab.com' in ponce_git_mirror and Path(ponce_repo_path, '.git/').is_dir():
                    branch: str = utils.get_git_branch(ponce_repo_path)
                    ponce_repo_mirror: str = f'https://gitlab.com/{owner}/{repository_name}/-/raw/{branch}/'

            slack_repo: bool = repos_config['SLACK']['ENABLE']
            slack_repo_mirror: str = repos_config['SLACK']['MIRROR']

            slack_extra_repo: bool = repos_config['SLACK_EXTRA']['ENABLE']
            slack_extra_repo_url: str = repos_config['SLACK_EXTRA']['MIRROR']
            slack_extra_repo_mirror_packages: str = slack_extra_repo_url
            slack_extra_repo_mirror_changelog: str = f"{'/'.join(slack_extra_repo_url.split('/')[:-2])}/"

            slack_patches_repo: bool = repos_config['SLACK_PATCHES']['ENABLE']
            slack_patches_repo_url: str = repos_config['SLACK_PATCHES']['MIRROR']
            slack_patches_repo_mirror_packages: str = slack_patches_repo_url
            slack_patches_repo_mirror_changelog: str = f"{'/'.join(slack_patches_repo_url.split('/')[:-2])}/"

            alien_repo: bool = repos_config['ALIEN']['ENABLE']
            alien_repo_url: str = repos_config['ALIEN']['MIRROR']
            alien_repo_mirror_packages: str = alien_repo_url
            alien_repo_mirror_changelog: str = f"{'/'.join(alien_repo_url.split('/')[:-3])}/"

            multilib_repo: bool = repos_config['MULTILIB']['ENABLE']
            multilib_repo_url: str = repos_config['MULTILIB']['MIRROR']
            multilib_repo_mirror_packages: str = multilib_repo_url
            multilib_repo_mirror_changelog: str = f"{'/'.join(multilib_repo_url.split('/')[:-2])}/"

            restricted_repo: bool = repos_config['RESTRICTED']['ENABLE']
            restricted_repo_url: str = repos_config['RESTRICTED']['MIRROR']
            restricted_repo_mirror_packages: str = restricted_repo_url
            restricted_repo_mirror_changelog: str = f"{'/'.join(restricted_repo_url.split('/')[:-3])}/"

            gnome_repo: bool = repos_config['GNOME']['ENABLE']
            gnome_repo_mirror: str = repos_config['GNOME']['MIRROR']

            msb_repo: bool = repos_config['MSB']['ENABLE']
            msb_repo_url: str = repos_config['MSB']['MIRROR']
            msb_repo_mirror_packages: str = msb_repo_url
            msb_repo_mirror_changelog: str = f"{'/'.join(msb_repo_url.split('/')[:-4])}/"

            csb_repo: bool = repos_config['CSB']['ENABLE']
            csb_repo_mirror: str = repos_config['CSB']['MIRROR']

            conraid_repo: bool = repos_config['CONRAID']['ENABLE']
            conraid_repo_mirror: str = repos_config['CONRAID']['MIRROR']

            slackonly_repo: bool = repos_config['SLACKONLY']['ENABLE']
            slackonly_repo_mirror: str = repos_config['SLACKONLY']['MIRROR']

            salix_repo: bool = repos_config['SALIX']['ENABLE']
            salix_repo_mirror: str = repos_config['SALIX']['MIRROR']

            salix_extra_repo: bool = repos_config['SALIX_EXTRA']['ENABLE']
            salix_extra_repo_mirror: str = repos_config['SALIX_EXTRA']['MIRROR']

            slackel_repo: bool = repos_config['SLACKEL']['ENABLE']
            slackel_repo_mirror: str = repos_config['SLACKEL']['MIRROR']

            slint_repo: bool = repos_config['SLINT']['ENABLE']
            slint_repo_mirror: str = repos_config['SLINT']['MIRROR']

            pprkut_repo: bool = repos_config['PPRKUT']['ENABLE']
            pprkut_repo_mirror: str = repos_config['PPRKUT']['MIRROR']
    except (KeyError, tomlkit.exceptions.TOMLKitError) as error:
        toml_errors.raise_toml_error_message(error, repositories_toml_file)

    # Dictionary configurations of repositories.
    repositories: ClassVar[list[str]] = {
        sbo_repo_name: {
            'enable': sbo_repo,
            'path': sbo_repo_path,
            'mirror_packages': sbo_repo_mirror,
            'mirror_changelog': sbo_repo_mirror,
            'slackbuilds_txt': slackbuilds_txt,
            'changelog_txt': changelog_txt,
            'repo_tag': sbo_repo_tag,
            'tar_suffix': sbo_repo_tar_suffix},

        ponce_repo_name: {
            'enable': ponce_repo,
            'path': ponce_repo_path,
            'mirror_packages': ponce_repo_mirror,
            'mirror_changelog': ponce_repo_mirror,
            'slackbuilds_txt': slackbuilds_txt,
            'changelog_txt': changelog_txt,
            'repo_tag': ponce_repo_tag,
            'tar_suffix': ponce_repo_tar_suffix},

        slack_repo_name: {
            'enable': slack_repo,
            'path': slack_repo_path,
            'mirror_packages': slack_repo_mirror,
            'mirror_changelog': slack_repo_mirror,
            'packages_txt': packages_txt,
            'checksums_md5': checksums_md5,
            'changelog_txt': changelog_txt,
            'repo_tag': slack_repo_tag},

        slack_extra_repo_name: {
            'enable': slack_extra_repo,
            'path': slack_extra_repo_path,
            'mirror_packages': slack_extra_repo_mirror_packages,
            'mirror_changelog': slack_extra_repo_mirror_changelog,
            'packages_txt': packages_txt,
            'checksums_md5': checksums_md5,
            'changelog_txt': changelog_txt,
            'repo_tag': slack_extra_repo_tag},

        slack_patches_repo_name: {
            'enable': slack_patches_repo,
            'path': slack_patches_repo_path,
            'mirror_packages': slack_patches_repo_mirror_packages,
            'mirror_changelog': slack_patches_repo_mirror_changelog,
            'packages_txt': packages_txt,
            'checksums_md5': checksums_md5,
            'changelog_txt': changelog_txt,
            'repo_tag': slack_patches_repo_tag},

        alien_repo_name: {
            'enable': alien_repo,
            'path': alien_repo_path,
            'mirror_packages': alien_repo_mirror_packages,
            'mirror_changelog': alien_repo_mirror_changelog,
            'packages_txt': packages_txt,
            'checksums_md5': checksums_md5,
            'changelog_txt': changelog_txt,
            'repo_tag': alien_repo_tag},

        multilib_repo_name: {
            'enable': multilib_repo,
            'path': multilib_repo_path,
            'mirror_packages': multilib_repo_mirror_packages,
            'mirror_changelog': multilib_repo_mirror_changelog,
            'packages_txt': packages_txt,
            'checksums_md5': checksums_md5,
            'changelog_txt': changelog_txt,
            'repo_tag': multilib_repo_tag},

        restricted_repo_name: {
            'enable': restricted_repo,
            'path': restricted_repo_path,
            'mirror_packages': restricted_repo_mirror_packages,
            'mirror_changelog': restricted_repo_mirror_changelog,
            'packages_txt': packages_txt,
            'checksums_md5': checksums_md5,
            'changelog_txt': changelog_txt,
            'repo_tag': restricted_repo_tag},

        gnome_repo_name: {
            'enable': gnome_repo,
            'path': gnome_repo_path,
            'mirror_packages': gnome_repo_mirror,
            'mirror_changelog': gnome_repo_mirror,
            'packages_txt': packages_txt,
            'checksums_md5': checksums_md5,
            'changelog_txt': changelog_txt,
            'repo_tag': gnome_repo_tag},

        msb_repo_name: {
            'enable': msb_repo,
            'path': msb_repo_path,
            'mirror_packages': msb_repo_mirror_packages,
            'mirror_changelog': msb_repo_mirror_changelog,
            'packages_txt': packages_txt,
            'checksums_md5': checksums_md5,
            'changelog_txt': changelog_txt,
            'repo_tag': msb_repo_tag},

        csb_repo_name: {
            'enable': csb_repo,
            'path': csb_repo_path,
            'mirror_packages': csb_repo_mirror,
            'mirror_changelog': csb_repo_mirror,
            'packages_txt': packages_txt,
            'checksums_md5': checksums_md5,
            'changelog_txt': changelog_txt,
            'repo_tag': csb_repo_tag},

        conraid_repo_name: {
            'enable': conraid_repo,
            'path': conraid_repo_path,
            'mirror_packages': conraid_repo_mirror,
            'mirror_changelog': conraid_repo_mirror,
            'packages_txt': packages_txt,
            'checksums_md5': checksums_md5,
            'changelog_txt': changelog_txt,
            'repo_tag': conraid_repo_tag},

        slackonly_repo_name: {
            'enable': slackonly_repo,
            'path': slackonly_repo_path,
            'mirror_packages': slackonly_repo_mirror,
            'mirror_changelog': slackonly_repo_mirror,
            'packages_txt': packages_txt,
            'checksums_md5': checksums_md5,
            'changelog_txt': changelog_txt,
            'repo_tag': slackonly_repo_tag},

        salix_repo_name: {
            'enable': salix_repo,
            'path': salix_repo_path,
            'mirror_packages': salix_repo_mirror,
            'mirror_changelog': salix_repo_mirror,
            'packages_txt': packages_txt,
            'checksums_md5': checksums_md5,
            'changelog_txt': changelog_txt,
            'repo_tag': salix_repo_tag},

        salix_extra_repo_name: {
            'enable': salix_extra_repo,
            'path': salix_extra_repo_path,
            'mirror_packages': salix_extra_repo_mirror,
            'mirror_changelog': salix_extra_repo_mirror,
            'packages_txt': packages_txt,
            'checksums_md5': checksums_md5,
            'changelog_txt': changelog_txt,
            'repo_tag': salix_extra_repo_tag},

        slackel_repo_name: {
            'enable': slackel_repo,
            'path': slackel_repo_path,
            'mirror_packages': slackel_repo_mirror,
            'mirror_changelog': slackel_repo_mirror,
            'packages_txt': packages_txt,
            'checksums_md5': checksums_md5,
            'changelog_txt': changelog_txt,
            'repo_tag': slackel_repo_tag},

        slint_repo_name: {
            'enable': slint_repo,
            'path': slint_repo_path,
            'mirror_packages': slint_repo_mirror,
            'mirror_changelog': slint_repo_mirror,
            'packages_txt': packages_txt,
            'checksums_md5': checksums_md5,
            'changelog_txt': changelog_txt,
            'repo_tag': slint_repo_tag},

        pprkut_repo_name: {
            'enable': pprkut_repo,
            'path': pprkut_repo_path,
            'mirror_packages': pprkut_repo_mirror,
            'mirror_changelog': pprkut_repo_mirror,
            'packages_txt': packages_txt,
            'checksums_md5': checksums_md5,
            'changelog_txt': changelog_txt,
            'repo_tag': pprkut_repo_tag}
    }

    all_repos = [name.lower() for name in repos_config.keys()]
    defaults_repos = list(repositories.keys())

    diff_repos = list(set(all_repos) - set(defaults_repos))
    items_to_remove = ('default', 'new_packages', 'remove_packages')
    for item in items_to_remove:
        diff_repos.remove(item)

    diff_repos = [name.upper() for name in diff_repos]

    if diff_repos:
        for repo, data in repos_config.items():

            if repo in diff_repos:
                mirror_packages: str = data.get('MIRROR', '')
                mirror_changelog: str = mirror_packages
                if data.get('CHANGELOG'):
                    mirror_changelog: str = data.get('CHANGELOG', '')

                values = {
                    'enable': data.get('ENABLE'),
                    'path': Path(repositories_path, str(repo.lower())),
                    'mirror_packages': mirror_packages,
                    'mirror_changelog': mirror_changelog,
                    'packages_txt': packages_txt,
                    'checksums_md5': checksums_md5,
                    'changelog_txt': changelog_txt,
                    'repo_tag': data.get('tag', '')
                }
                repositories[str(repo.lower())] = values

#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os
import threading
from pathlib import Path
from multiprocessing import Process
from urllib.parse import unquote, urlparse

from slpkg.configs import Configs
from slpkg.utilities import Utilities
from slpkg.error_messages import Errors
from slpkg.multi_process import MultiProcess
from slpkg.views.views import View


class Downloader(Configs):  # pylint: disable=[R0902]
    """Download the sources using external tools."""

    def __init__(self, flags: list):
        super(Configs, self).__init__()
        self.flags: list = flags

        self.errors = Errors()
        self.utils = Utilities()
        self.multi_process = MultiProcess(flags)
        self.views = View(flags)

        self.filename: str = ''
        self.downloader_command: str = ''
        self.downloader_tools: dict = {
            'wget': self.set_wget_downloader,
            'wget2': self.set_wget_downloader,
            'curl': self.set_curl_downloader,
            'lftp': self.set_lftp_downloader
        }

        # Semaphore to control the number of concurrent threads
        self.semaphore = threading.BoundedSemaphore(int(self.maximum_parallel))

        self.option_for_parallel: bool = self.utils.is_option(
            ('-P', '--parallel'), flags)

    def download(self, sources: dict) -> None:
        """Start the process for downloading."""
        if self.parallel_downloads or self.option_for_parallel:
            self.parallel_download(sources)
        else:
            self.normal_download(sources)

    def parallel_download(self, sources: dict) -> None:
        """Download sources with parallel mode."""
        processes: list = []
        for urls, path in sources.values():
            with self.semaphore:
                for url in urls:
                    proc = Process(target=self.tools, args=(url, path))
                    processes.append(proc)
                    proc.start()

        for process in processes:
            process.join()

    def normal_download(self, sources: dict) -> None:
        """Download sources with normal mode."""
        for urls, path in sources.values():
            for url in urls:
                self.tools(url, path)

    def tools(self, url: str, path: Path) -> None:
        """Run the tool to downloading.

        Args:
            url (str): The URL link.
            path (Path): Path to save.
        """
        url_parse: str = urlparse(url).path
        self.filename: str = unquote(Path(url_parse).name)

        try:
            self.downloader_tools[self.downloader](url, path)
        except KeyError:
            self.errors.raise_error_message(f"Downloader '{self.downloader}' not supported", exit_status=1)

        self.multi_process.process(self.downloader_command)
        self.check_if_downloaded(url, path)

    def set_wget_downloader(self, url: str, path: Path) -> None:
        """Set for wget tool.

        Args:
            url (str): URL link.
            path (Path): Path to save.
        """
        self.downloader_command: str = f'{self.downloader} {self.wget_options} --directory-prefix={path} "{url}"'

    def set_curl_downloader(self, url: str, path: Path) -> None:
        """Set for curl tool.

        Args:
            url (str): URL link.
            path (Path): Path to save.
        """
        self.downloader_command: str = (f'{self.downloader} {self.curl_options} "{url}" '
                                        f'--output {path}/{self.filename}')

    def set_lftp_downloader(self, url: str, path: Path) -> None:
        """Set for lftp tool.

        Args:
            url (str): URL link.
            path (Path): Path to save.
        """
        self.downloader_command: str = f'{self.downloader} {self.lftp_get_options} {url} -o {path}'

    def check_if_downloaded(self, url: str, path: Path) -> None:
        """Check for downloaded.

        Args:
            url (str): URL link.
            path (Path): Path to check the file.
        """
        path_file: Path = Path(path, self.filename)
        if not path_file.exists():
            parsed_url = urlparse(url)
            filename: str = os.path.basename(parsed_url.path)
            print(f"{self.red}>{self.endc} Failed to download the file: '{filename}'")
            self.views.question()

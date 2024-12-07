#!/usr/bin/python3
# -*- coding: utf-8 -*-


from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Union
from urllib.parse import unquote

from slpkg.configs import Configs
from slpkg.views.views import View
from slpkg.error_messages import Errors
from slpkg.views.asciibox import AsciiBox


class Md5sum(Configs):
    """Checksum the file sources."""

    def __init__(self, flags: list):
        super(Configs, self).__init__()

        self.ascii = AsciiBox()
        self.errors = Errors()
        self.view = View(flags)

    def md5sum(self, path: Union[str, Path], source: str, checksum: str) -> None:
        """Checksum the source file.

        Args:
            path (Union[str, Path]): Path to source file.
            source (str): Source file.
            checksum (str): Expected checksum.
        """
        if self.checksum_md5:
            source_file = unquote(source)
            filename = source_file.split('/')[-1]
            source_path = Path(path, filename)

            md5: bytes = self.read_binary_file(source_path)
            file_check: str = hashlib.md5(md5).hexdigest()
            checksum: str = "".join(checksum)

            if file_check != checksum:
                self.ascii.draw_checksum_error_box(filename, checksum, file_check)
                self.view.question()

    def read_binary_file(self, filename: Union[str, Path]) -> bytes | None:
        """Read the file source.

        Args:
            filename (Union[str, Path]): File name.

        Returns:
            bytes: Binary bytes.
        """
        try:
            with open(filename, 'rb') as file:
                return file.read()
        except FileNotFoundError:
            self.errors.raise_error_message(f"No such file or directory: '{filename}'", exit_status=20)
        return None

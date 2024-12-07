#!/usr/bin/python3
# -*- coding: utf-8 -*-


import locale
from pathlib import Path
from typing import Union, Tuple
from dialog import Dialog

from slpkg.configs import Configs
from slpkg.views.version import Version

locale.setlocale(locale.LC_ALL, '')


class DialogBox(Configs):
    """Class for dialog box."""

    def __init__(self):
        super(Configs).__init__()
        self.more_kwargs: dict = {}

        self.d = Dialog(dialog="dialog")
        self.d.add_persistent_args(["--colors"])
        self.d.set_background_title(f'{self.prog_name} {Version().version} - Software Package Manager')

    def checklist(self, text: str, title: str, height: int, width: int,  # pylint: disable=[R0913]
                  list_height: int, choices: list) -> Tuple[bool, list]:
        """Display a checklist box."""
        self.more_kwargs.update(
            {"item_help": True}
        )

        code, tags = self.d.checklist(text=text, choices=choices, title=title, height=height, width=width,  # pylint: disable=[R0913]
                                      list_height=list_height, help_status=True, **self.more_kwargs)

        return code, tags

    def mixedform(self, text: str, title: str, elements: list, height: int, width: int,  # pylint: disable=[R0913]
                  form_height: int) -> Tuple[bool, list]:
        """Display a mixedform box."""
        self.more_kwargs.update(
            {"item_help": True,
             "help_tags": True}
        )
        code, tags = self.d.mixedform(text=text, title=title, elements=elements,  # type: ignore
                                      height=height, width=width, form_height=form_height, help_button=True,
                                      help_status=True, **self.more_kwargs)

        return code, tags

    def msgbox(self, text: str, height: int, width: int) -> None:
        """Display a message box."""
        self.d.msgbox(text, height, width)

    def textbox(self, text: Union[str, Path], height: int, width: int) -> None:
        """Display a text box."""
        self.d.textbox(text, height, width)

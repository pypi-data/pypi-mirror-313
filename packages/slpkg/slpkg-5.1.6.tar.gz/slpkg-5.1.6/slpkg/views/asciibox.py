#!/usr/bin/python3
# -*- coding: utf-8 -*-


import shutil

from slpkg.configs import Configs


class AsciiBox(Configs):  # pylint: disable=[R0902]
    """Managing the ASCII characters."""

    def __init__(self):
        super(Configs, self).__init__()
        self.columns, self.rows = shutil.get_terminal_size()
        self.package_alignment: int = self.columns - 56
        self.version_alignment: int = 29
        self.size_alignment: int = 9
        self.repo_alignment: int = 14

        self.package_alignment = max(self.package_alignment, 1)

        self.bd_color: str = self.endc
        self.border_colors: dict = {}
        self.assign_border_color()

        self.bullet: str = '-'
        self.done: str = 'Done'
        self.failed: str = 'Failed'
        self.skipped: str = 'Skipped'

        self.vertical_line: str = '|'
        self.horizontal_line: str = '='
        self.horizontal_vertical: str = '+'
        self.upper_right_corner: str = '+'
        self.lower_left_corner: str = '+'
        self.lower_right_corner: str = '+'
        self.upper_left_corner: str = '+'
        self.horizontal_and_up: str = '+'
        self.horizontal_and_down: str = '+'
        self.vertical_and_right: str = '+'
        self.vertical_and_left: str = '+'

        if self.ascii_characters:
            self.bullet: str = '•'
            self.done: str = '✔'
            self.failed: str = '✖'
            self.skipped: str = '↪'
            self.vertical_line: str = '│'
            self.horizontal_line: str = '─'
            self.horizontal_vertical: str = '┼'
            self.upper_right_corner: str = '┐'
            self.lower_left_corner: str = '└'
            self.lower_right_corner: str = '┘'
            self.upper_left_corner: str = '┌'
            self.horizontal_and_up: str = '┴'
            self.horizontal_and_down: str = '┬'
            self.vertical_and_right: str = '├'
            self.vertical_and_left: str = '┤'

    def assign_border_color(self) -> None:
        """Assign the colors."""
        self.border_colors: dict = {
            'red': self.red,
            'blue': self.blue,
            'cyan': self.cyan,
            'white': self.endc,
            'green': self.green,
            'yellow': self.yellow,
            'bold_red': self.bred,
            'bold_blue': self.bblue,
            'bold_cyan': self.bcyan,
            'bold_green': self.bgreen,
            'bold_yellow': self.byellow
        }
        try:
            self.bd_color: str = self.border_colors[self.border_color]
        except KeyError:
            self.bd_color: str = self.endc

    def draw_package_title(self, message: str, title: str) -> None:
        """Draw the package title.

        Args:
            message (str): Message about the action.
            title (str): Slpkg title.
        """
        title = title.title()
        print(f"{self.bd_color}{self.upper_left_corner}{self.horizontal_line * (self.columns - 2)}"
              f"{self.upper_right_corner}")
        print(f"{self.vertical_line}{title.center(self.columns - 2, ' ')}{self.vertical_line}")
        self.draw_middle_line()
        print(f"{self.vertical_line} {self.endc}{message.ljust(self.columns - 3, ' ')}"
              f"{self.bd_color}{self.vertical_line}")
        self.draw_middle_line()
        print(f"{self.bd_color}{self.vertical_line}{self.endc} {'Package:':<{self.package_alignment}}"
              f"{'Version:':<{self.version_alignment}}{'Size:':<{self.size_alignment}}{'Repo:':>{self.repo_alignment}} "
              f"{self.bd_color}{self.vertical_line}{self.endc}")

    def draw_package_line(self, package: str, version: str, size: str, color: str, repo: str) -> None:  # pylint: disable=[R0913]
        """Draw the package line.

        Args:
            package (str): Package name.
            version (str): Package version.
            size (str): Package size.
            color (str): Package highlight.
            repo (str): Repository name.
        """
        if len(version) >= (self.version_alignment - 5):
            version: str = f'{version[:self.version_alignment - 5]}...'
        if len(package) >= (self.package_alignment - 4):
            package: str = f'{package[:self.package_alignment - 4]}...'

        print(f"{self.bd_color}{self.vertical_line} {self.bold}{color}{package:<{self.package_alignment}}{self.endc}"
              f"{self.bd_color}{version:<{self.version_alignment}}{self.endc}{size:<{self.size_alignment}}{self.blue}"
              f"{repo:>{self.repo_alignment}}{self.bd_color} {self.vertical_line}{self.endc}")

    def draw_middle_line(self) -> None:
        """Draw the middle line."""
        print(f"{self.bd_color}{self.vertical_and_right}{self.horizontal_line * (self.columns - 2)}"
              f"{self.vertical_and_left}")

    def draw_dependency_line(self) -> None:
        """Draw the dependency line."""
        print(f"{self.bd_color}{self.vertical_line}{self.endc} Dependencies:{' ' * (self.columns - 16)}"
              f"{self.bd_color}{self.vertical_line}{self.endc}")

    def draw_bottom_line(self) -> None:
        """Draw the bottom line."""
        print(f"{self.bd_color}{self.lower_left_corner}{self.horizontal_line * (self.columns - 2)}"
              f"{self.lower_right_corner}{self.endc}")

    def draw_checksum_error_box(self, name: str, checksum: str, file_check: str) -> None:
        """Draw a checksum error box.

        Args:
            name (str): Package name.
            checksum (str): Expected checksum.
            file_check (str): Found checksum.
        """
        print(f"{self.bred}{self.upper_left_corner}{self.horizontal_line * (self.columns - 2)}"
              f"{self.upper_right_corner}")
        print(f"{self.bred}{self.vertical_line}{self.bred} FAILED:{self.endc} MD5SUM check for "
              f"'{self.cyan}{name}'{' ' * (self.columns - len(name) - 30)}{self.red}{self.vertical_line}")
        print(f"{self.bred}{self.vertical_and_right}{self.horizontal_line * (self.columns - 2)}"
              f"{self.vertical_and_left}")
        print(f"{self.bred}{self.vertical_line}{self.yellow} Expected:{self.endc} {checksum}{self.bred}"
              f"{' ' * (self.columns - (len(checksum)) - 13)}{self.vertical_line}")
        print(f"{self.bred}{self.vertical_line}{self.violet} Found:{self.endc} {file_check}{self.bred}"
              f"{' ' * (self.columns - (len(file_check)) - 10)}{self.vertical_line}")
        print(f"{self.bred}{self.lower_left_corner}{self.horizontal_line * (self.columns - 2)}"
              f"{self.lower_right_corner}{self.endc}")

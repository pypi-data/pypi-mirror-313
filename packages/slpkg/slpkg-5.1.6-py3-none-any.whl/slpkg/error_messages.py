#!/usr/bin/python3
# -*- coding: utf-8 -*-


from slpkg.configs import Configs


class Errors(Configs):  # pylint: disable=[R0903]
    """Raise an error message."""

    def __init__(self):
        super(Configs, self).__init__()

    def raise_error_message(self, message: str, exit_status: int) -> None:
        """General method to raise an error message and exit.

        Args:
            message (str): Str message.
            exit_status (int): Exit status code.

        Raises:
            SystemExit: Description
        """
        print(f"\n{self.prog_name}: {self.bred}Error{self.endc}: {message}\n")
        raise SystemExit(exit_status)

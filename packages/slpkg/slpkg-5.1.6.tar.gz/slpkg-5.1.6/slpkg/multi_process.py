#!/usr/bin/python3
# -*- coding: utf-8 -*-


import shutil
import subprocess
from datetime import datetime
from multiprocessing import Process

from slpkg.configs import Configs
from slpkg.utilities import Utilities
from slpkg.error_messages import Errors
from slpkg.views.asciibox import AsciiBox
from slpkg.progress_bar import ProgressBar


class MultiProcess(Configs):  # pylint: disable=[R0902]
    """Create parallel process between progress bar and process."""

    def __init__(self, flags: list = None):
        super(Configs, self).__init__()

        self.utils = Utilities()
        self.progress = ProgressBar()
        self.ascii = AsciiBox()
        self.errors = Errors()

        self.columns, self.rows = shutil.get_terminal_size()
        self.timestamp: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.head_message: str = f'Timestamp: {self.timestamp}'
        self.bottom_message: str = 'EOF - End of log file'

        if flags is not None:
            self.option_for_progress_bar: bool = self.utils.is_option(
                ('-B', '--progress-bar'), flags)

            self.option_for_reinstall: bool = self.utils.is_option(
                ('-r', '--reinstall'), flags)

    def process_and_log(self, command: str, filename: str, progress_message: str) -> None:
        """Start a multiprocessing process.

        Args:
            command: The command of process
            filename: The filename of process.
            progress_message: The message of progress.
        Returns:
            None.
        """
        if self.progress_bar_conf or self.option_for_progress_bar:
            skip: str = f'{self.bred}{self.ascii.skipped}{self.endc}'
            done: str = f'{self.bgreen}{self.ascii.done}{self.endc}'
            failed: str = f'{self.bred}{self.ascii.failed}{self.endc}'
            installed: str = ''

            if filename.endswith(tuple(self.package_type)) and not self.option_for_reinstall:
                installed_package = self.log_packages.glob(filename[:-4])
                for inst in installed_package:
                    if inst.name == filename[:-4]:
                        installed: str = filename[:-4]

            # Starting multiprocessing
            process_1 = Process(target=self._run, args=(command,))
            process_2 = Process(target=self.progress.progress_bar, args=(progress_message, filename))

            process_1.start()
            process_2.start()

            # Wait until process 1 finish
            process_1.join()

            # Terminate process 2 if process 1 finished
            if not process_1.is_alive():
                process_2.terminate()
                print(f"\r{' ' * (self.columns - 1)}", end='')  # Delete previous line.
                if process_1.exitcode != 0:
                    print(f"\r{'':>2}{self.bred}{self.ascii.bullet}{self.endc} {filename} {failed}", end='')
                elif installed:
                    print(f"\r{'':>2}{self.bred}{self.ascii.bullet}{self.endc} {filename} {skip}", end='')
                else:
                    print(f"\r{'':>2}{self.bgreen}{self.ascii.bullet}{self.endc} {filename} {done}", end='')

            # Restore the terminal cursor
            print('\x1b[?25h', self.endc)
        else:
            self._run(command)

    def _run(self, command: str, stdout: subprocess = subprocess.PIPE, stderr: subprocess = subprocess.STDOUT) -> None:
        """Build the package and write a log file.

        Args:
            command: The command of process
            stdout: Captured stdout from the child process.
            stderr: Captured stderr from the child process.
        Returns:
            None.
        """
        with subprocess.Popen(command, shell=True, stdout=stdout, stderr=stderr, text=True) as process:

            self._write_log_head()

            # Write the process to the log file and to the terminal.
            with process.stdout as output:  # type: ignore[union-attr]
                for line in output:
                    if not self.progress_bar_conf and not self.option_for_progress_bar:
                        print(line.strip())  # Print to console
                    if self.process_log:
                        with open(self.slpkg_log_file, 'a', encoding='utf-8') as log:
                            log.write(line)  # Write to log file

            self._write_log_eof()

            process.wait()  # Wait for the process to finish

            # If the process failed, return exit code.
            if process.returncode != 0:
                self._error_process()
                raise SystemExit(process.returncode)

    def _error_process(self) -> None:
        """Print error message for a process."""
        if not self.progress_bar_conf and not self.option_for_progress_bar:
            message: str = 'Error occurred with process. Please check the log file.'
            print()
            print(len(message) * '=')
            print(f'{self.bred}{message}{self.endc}')
            print(len(message) * '=')
            print()

    def _write_log_head(self) -> None:
        """Write the timestamp at the head of the log file."""
        if self.process_log:
            with open(self.slpkg_log_file, 'a', encoding='utf-8') as log:
                log.write(f"{len(self.head_message) * '='}\n")
                log.write(f'{self.head_message}\n')
                log.write(f"{len(self.head_message) * '='}\n")

    def _write_log_eof(self) -> None:
        """Write the bottom of the log file."""
        if self.process_log:
            with open(self.slpkg_log_file, 'a', encoding='utf-8') as log:
                log.write(f"\n{len(self.bottom_message) * '='}\n")
                log.write(f'{self.bottom_message}\n')
                log.write(f"{len(self.bottom_message) * '='}\n\n")

    @staticmethod
    def process(command: str, stderr: subprocess = None, stdout: subprocess = None) -> None:
        """Build the package and write a log file.

        Args:
            command: The command of process
            stdout: Captured stdout from the child process.
            stderr: Captured stderr from the child process.
        Returns:
            None.
        """
        try:
            output = subprocess.run(f'{command}', shell=True, stderr=stderr, stdout=stdout, check=False)
        except KeyboardInterrupt as e:
            raise SystemExit(1) from e

        if output.returncode != 0:
            if not command.startswith(('wget', 'wget2', 'curl', 'lftp')):
                raise SystemExit(output.returncode)

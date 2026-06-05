# File: src/ftwpki/unpacker/cli_parser.py
# Author: Fitzz TeXnik Welt
# Email: FitzzTeXnikWelt@t-online.de
# License: LGPLv2 or above
"""
cli_parser
===============================

Parser for the certificate unpacker CLI, managing private key identification
and transport package paths. (rw)
"""

from argparse import Namespace
from pathlib import Path
from typing import cast

from ftwpki.baselibs.cli_parser import ArgparseFix311, AutoHelpParserMixin, load_help_entries
from ftwpki.unpacker.protocols import UnpackerCliProtocol

HELP_FILE = Path(__file__).parent.joinpath("cli_parser.help")

_HELP = {}

load_help_entries(_HELP, HELP_FILE)

LANG = "en"


# CLASS - UnpackerCliParser
class UnpackerCliParser(AutoHelpParserMixin, ArgparseFix311):
    """
    Parser for certificate reception arguments. (rw)

    Handles the input for the local private key filename and the path
    to the encrypted transport package.
    """

    def __init__(self, *args, run_setup: bool = True, exit_on_error: bool = False, **kwargs):
        self._is_preparser = not kwargs.get("add_help", True)
        kwargs["exit_on_error"] = exit_on_error
        super().__init__(*args, help_id="unpacker", help_entries=_HELP, **kwargs)
        if run_setup:
            self._setup_parser()

    def _setup_parser(self) -> None:
        """
        Configure the argument parser with unpacker-specific options. (ro)
        """
        self.add_argument(
            "private_key",
            nargs = "?" if self._is_preparser else None ,
            help=self._help("private_key"),
        )
        self.add_argument(
            "cert_file",
            nargs="?" if self._is_preparser else None,
            help=self._help("cert_file"),
        )
        self.add_argument(
            "passphrase_file", nargs="?", default=None, help=self._help("passphrase_file"),
        )
        self.add_argument("-c", "--config-name", dest="configname", help=self._help("configname"))

    def parse_args(
        self, args: list[str] | None = None, namespace: Namespace | None = None
    ) -> UnpackerCliProtocol:
        """
        Parse command-line arguments and cast to UnpackerCliProtocol. (ro)

        :param args: List of command-line argument strings.
        :param namespace: Existing Namespace object to populate.
        :returns: Arguments adhering to the UnpackerCliProtocol interface.
        """
        return cast(UnpackerCliProtocol, super().parse_args(args, namespace))


# !CLASS - UnpackerCliParser


def get_parser() -> UnpackerCliParser:
    """
    Factory function to retrieve a configured UnpackerCliParser instance. (ro)

    :returns: A new instance of UnpackerCliParser.
    """
    return UnpackerCliParser()

if __name__ == "__main__":  # pragma: no cover
    from doctest import FAIL_FAST, testfile

    be_verbose = False
    be_verbose = True
    option_flags = 0
    option_flags = FAIL_FAST
    test_sum = 0
    test_failed = 0
    passed_files = 0

    # Pfad zu den dokumentierenden Tests
    testfiles_dir = Path(__file__).parents[3] / "doc/source/devel"
    test_files = [
        "test_new_parser.rst",
        # "get_started_cli_parser.rst",
    ]
    for file in test_files:
        test_file = testfiles_dir / file
        if test_file.exists():
            print(f"--- Running Doctest for {test_file.name} ---")
            doctestresult = testfile(
                str(test_file),
                module_relative=False,
                verbose=be_verbose,
                optionflags=option_flags,
            )
            test_failed += doctestresult.failed
            test_sum += doctestresult.attempted
            if doctestresult.failed > 0 and option_flags & FAIL_FAST:
                print(f"Doctest result for {test_file.name}: {doctestresult}")
                print(
                    f"\nKeep going! You already passed {passed_files} files "
                    f"with {test_sum} tests before this hit."
                )
                break  # Stop on first failure if FAIL_FAST is set
            passed_files += 1
        else:
            print(f"⚠️ Warning: Test file {test_file.name} not found.")
    if test_failed == 0:
        print(f"\nDocTests passed without errors, {test_sum} tests.")
    else:
        if not option_flags & FAIL_FAST:
            print(f"\nDocTests failed: {test_failed} tests out of {test_sum}.")

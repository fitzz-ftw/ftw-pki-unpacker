# File: src/ftwpki/receiver/cli_parser.py
# Author: Fitzz TeXnik Welt
# Email: FitzzTeXnikWelt@t-online.de
# License: LGPLv2 or above
"""
cli_parser
===============================

Parser for the certificate receiver CLI, managing private key identification
and transport package paths. (rw)
"""

from argparse import Namespace
from pathlib import Path
from typing import cast

from ftwpki.baselibs.cli_parser import ArgparseFix311
from ftwpki.receiver.protocols import ReceiverCliProtocol


# CLASS - ReceiverCliParser
class ReceiverCliParser(ArgparseFix311):
    """
    Parser for certificate reception arguments. (rw)

    Handles the input for the local private key filename and the path
    to the encrypted transport package.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._setup_parser()

    def _setup_parser(self) -> None:
        """
        Configure the argument parser with receiver-specific options. (ro)
        """
        self.add_argument(
            "private_key",
            help="The filename of the local private key used for decryption.",
        )
        self.add_argument(
            "cert_file",
            help="The file path of the encrypted certificate transport package.",
        )

    def parse_args(
        self, args: list[str] | None = None, namespace: Namespace | None = None
    ) -> ReceiverCliProtocol:
        """
        Parse command-line arguments and cast to ReceiverCliProtocol. (ro)

        :param args: List of command-line argument strings.
        :param namespace: Existing Namespace object to populate.
        :returns: Arguments adhering to the ReceiverCliProtocol interface.
        """
        return cast(ReceiverCliProtocol, super().parse_args(args, namespace))


# !CLASS - ReceiverCliParser


def get_parser() -> ReceiverCliParser:
    """
    Factory function to retrieve a configured ReceiverCliParser instance. (ro)

    :returns: A new instance of ReceiverCliParser.
    """
    return ReceiverCliParser()

if __name__ == "__main__":  # pragma: no cover
    from doctest import FAIL_FAST, testfile

    be_verbose = False
    be_verbose = True
    option_flags = 0
    option_flags = FAIL_FAST
    test_sum = 0
    test_failed = 0

    # Pfad zu den dokumentierenden Tests
    testfiles_dir = Path(__file__).parents[3] / "doc/source/devel"
    test_file = testfiles_dir / "get_started_cli_parser.rst"

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
        if test_failed == 0:
            print(f"\nDocTests passed without errors, {test_sum} tests.")
        else:
            print(f"\nDocTests failed: {test_failed} tests.")
    else:
        print(f"⚠️ Warning: Test file {test_file.name} not found.")

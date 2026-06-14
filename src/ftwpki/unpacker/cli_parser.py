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

from pathlib import Path
from typing import TypeAlias

from ftwpki.baselibs._cli_parser import _HELP, BaseArguments, PKIBaseParser, parser_factory_creator
from ftwpki.baselibs.cli_parser import load_help_entries

HELP_FILE = Path(__file__).parent.joinpath("cli_parser.help")


load_help_entries(_HELP, HELP_FILE)

LANG = "en"

class UnpackerCliArguments(BaseArguments):
    __slots__ = ["private_key", "cert_file", "passphrase_file", "configname"]
    helpid = ["unpacker"]
    arg_data = {
        "private_key": {"flags": [], "kws": {}, "pre": {"nargs": "?"}},
        "cert_file": {"flags": [], "kws": {}, "pre": {"nargs": "?"}},
        "passphrase_file": {"flags": [], "kws": {"nargs": "?"}, "pre": {}},
        "configname": {"flags": ["-c", "--config-name"], "kws": {}, "pre": {}},
    }

    def __init__(self) -> None:
        super().__init__()
        self.private_key:str=""
        self.cert_file:str = ""
        self.passphrase_file:str=""
        self.configname:str=""

UnpCli:TypeAlias = UnpackerCliArguments

unpacker_cli_parser = parser_factory_creator(UnpackerCliArguments)

def UnpackerCliParser(**kwargs) -> PKIBaseParser[UnpackerCliArguments]:
    parser: PKIBaseParser[UnpCli] = parser_factory_creator(UnpackerCliArguments)()
    return parser


def get_parser()  -> PKIBaseParser[UnpackerCliArguments]:
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
        # "test_new_parser.rst",
        "get_started_cli_parser.rst",
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

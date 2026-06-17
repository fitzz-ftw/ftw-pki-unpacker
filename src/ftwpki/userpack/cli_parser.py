# File: src/ftwpki/remotepack/cli_parser.py
# Author: Fitzz TeXnik Welt
# Email: FitzzTeXnikWelt@t-online.de
# License: LGPLv2 or above
"""
cli_parser
===============================


Modul cli_parser documentation
"""

from pathlib import Path
from typing import TypeAlias

from ftwpki.baselibs._cli_parser import (
    _HELP,
    PackArguments,
    load_help_entries,
    parser_factory_creator,
)

HELP_FILE = Path(__file__).parent.joinpath("cli_parser.help")


load_help_entries(_HELP, HELP_FILE)

LANG = "en"


class PKCS12CliArguments(PackArguments):
    """
    Container class for PKCS12 command line arguments.
    """
    __slots__ = ["old", "rootca"]
    helpid = ["pkcs12cli"]
    arg_data = {
        "old": {"flags":["-o","--old", "--pgpsm-compatible"],
                   "kws":{"action":"store_true",
                          },
                    "pre":{}
        },
        "rootca":{
            "flags": ["-c", "--caroot"],
            "kws": {"action":"store_true",},
            "pre":{}
        }
    }

    def __init__(self) -> None:
        """
        Initialize the PKCS12 argument container with default values.
        """
        super().__init__()
        self.old:bool = False
        self.rootca:bool = False

PKCS12: TypeAlias = PKCS12CliArguments
"""
Type alias for the PKCS12 command line argument container.
"""

pkcs12_cli_parser = parser_factory_creator(PKCS12CliArguments)
"""
Factory function for creating PKCS12 command line parsers.

This object is a factory function returned by the parser factory creator. 
It uses the PKCS12CliArguments class to generate specific parser instances 
for command line arguments.

:type: Callable
"""

if __name__ == "__main__": # pragma: no cover
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
        "get_started_cli_parser_remote.rst",
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
                print(f"\nKeep going! You already passed {passed_files} files "
                  f"with {test_sum} tests before this hit.")                
                break  # Stop on first failure if FAIL_FAST is set
            passed_files += 1
        else:
            print(f"⚠️ Warning: Test file {test_file.name} not found.")
    if test_failed == 0:
        print(f"\nDocTests passed without errors, {test_sum} tests.")
    else:
        if not option_flags & FAIL_FAST:
            print(f"\nDocTests failed: {test_failed} tests out of {test_sum}.")

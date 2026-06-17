# File: src/ftwpki/server/programms.py
# Author: Fitzz TeXnik Welt
# Email: FitzzTeXnikWelt@t-online.de
# License: LGPLv2 or above
"""
programms
===============================


Modul programms documentation
"""

import getpass
from pathlib import Path

from ftwpki.baselibs._cli_parser import PKIBaseParser
from ftwpki.baselibs.configuration import BasePKIConfig
from ftwpki.baselibs.core import load_private_key_from_pem
from ftwpki.baselibs.protocols import ClientTypeName
from ftwpki.remotepack.cli_parser import RPCli, remote_pack_cli_parser
from ftwpki.remotepack.container import PKIRemoteContainer


def prog_remotepack(argv:list[str]|None = None)->int:
    """
    Process and save a remote PKI container package for a server.

    This function configures the server identity, creates a cryptographic
    container, and loads required certificates and keys. The resulting
    container is then saved to the local file system.

    :param argv: The list of command line arguments.
    :raises KeyboardInterrupt: If the user cancels the program execution.
    :raises PKIMissingExportPathError: If a required export path is not defined.
    :raises Exception: For any other errors during execution.
    :returns: A status code where 0 is success, 1 is error, and 2 is interrupt.
    """
    try:
        # SECTION - Configuration
        config_type: ClientTypeName = "server"
        parser: PKIBaseParser[RPCli] = remote_pack_cli_parser()
        args = parser.parse_args(argv)
        pki_name = Path(args.configname).stem
        config: BasePKIConfig = BasePKIConfig(args.configname)
        config.set_config(config_type)
        config.handle_pki_file()
        # !SECTION - Configuration
        # SECTION - Container Creation
        container = PKIRemoteContainer(args.format)
        priv_key_bytes = config.private_key(args.private_key)
        if b"BEGIN PRIVATE" in priv_key_bytes:
            password=None
        else:
            password = getpass.getpass(f"Password for {args.private_key}: ")
            password = password if password else None
        priv_key_obj = load_private_key_from_pem(priv_key_bytes, password)
        container.private_key = priv_key_obj
        container.fullchain = config.fullchain
        container.caroot_cert = config.pki.caroot_cert
        pathfile = Path(Path(args.configname).stem).with_suffix(".id.toml").name
        container.load_pathes(config.pki.additional_files.get(pathfile,b""))
        # !SECTION - Container Creation
        # SECTION - Save Container
        container.save(pki_name)
        # !SECTION - Stop programm
        return 0
    except KeyboardInterrupt:
        return 2
    except Exception as e:
        print(e)
        return 1



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
        # "get_started_programms_remote.ci.rst",
        "get_started_run_programms_remote.ci.rst",
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

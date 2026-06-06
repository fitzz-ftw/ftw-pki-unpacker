# File: src/ftwpki/unpacker/programms.py
# Author: Fitzz TeXnik Welt
# Email: FitzzTeXnikWelt@t-online.de
# License: LGPLv2 or above
"""
programms
===============================


Main entry points for the certificate unpacker process. (rw)
"""

import getpass
import traceback
from pathlib import Path

from ftwpki.baselibs.configuration import PKIPackage, RootSignerPKIConfig
from ftwpki.baselibs.core import load_private_key_from_pem
from ftwpki.baselibs.passwd import PasswordManager
from ftwpki.baselibs.transport import RSAPrivateKey
from ftwpki.unpacker.cli_parser import UnpackerCliParser
from ftwpki.unpacker.protocols import UnpackerCliProtocol


def prog_unpacker_certs(argv: list[str] | None = None, **kwargs)->int:
    #DOC - change?
    """
    Execute the main process for receiving and installing certificates.

    This function coordinates the configuration setup, private key loading,
    package decryption, and the extraction of certificates and keys to
    their configured target directories.

    :param argv: List of command line arguments. Defaults to None.
    :param kwargs: Additional keyword arguments for future extensions.
    :raises FileNotFoundError: If the private key file or the certificate
                               package does not exist.
    :raises PermissionError: If the application cannot create directories
                             or write files due to missing permissions.
    :raises ValueError: If the private key loading or package decryption fails.
    :raises TOMLDecodeError: If the configuration file has an invalid format.
    :raises Exception: For any other errors during the process.
    :returns: Zero if the process is successful, or one if an error
              or a user interrupt occurs.
    """
    try:
        # SECTION - Configuration
        parser:UnpackerCliParser  = UnpackerCliParser()
        args:UnpackerCliProtocol = parser.parse_args(argv)
        config:RootSignerPKIConfig = RootSignerPKIConfig(args.cert_file)  
        config.set_config(args.configname)
        config.handle_pki_file()
        # !SECTION - Configuration
        if args.configname == "intermediate" and args.passphrase_file:
        # SECTION - Passphrasefilehandling
            pass_phrase = getpass.getpass("Enter Password: ")
            pwd_man = PasswordManager(private_dir=str(config.passphrases)) 
            pass_phrase:str|None = pwd_man.decrypt_password_file(
                config.passphrases / args.passphrase_file,
                pass_phrase
            )
            private_key_name = "CA.key.pem"
            del pwd_man
        #!SECTION - Passphrasefilehandling
        else:
            # SECTION - Standard password handling
            private_key_name = args.private_key
            if b"ENCRYPTED PRIVATE" in config.private_key(private_key_name):
                pass_phrase = getpass.getpass("Enter Password: ")
            else:
                pass_phrase = None
            # !SECTION - Standard password handling

        # SECTION - Loading private key
        private_key:RSAPrivateKey = load_private_key_from_pem(
                config.private_key(private_key_name), 
                pass_phrase
             )
        del pass_phrase
        # !SECTION - Loading private key
        # SECTION - Decrypting and Loading the file 
        pack = PKIPackage()
        pack.private_key = private_key
        del private_key
        pack.load(args.cert_file)
        del pack.private_key
        # !SECTION - Decrypting and Loading the file 
        # SECTION - Extraction and transfer of the content.
        conf_pki = config.pki
        conf_pki.fullchain.extend(pack.fullchain)
        conf_pki.ca_cert = pack.ca_cert
        conf_pki.caroot_cert = pack.caroot_cert
        conf_pki.own_cert = pack.own_cert
        conf_pki.intermediatechain.extend(pack.intermediatechain)
        conf_pki.additional_files.update(pack.additional_files)
        conf_pki.save()
        #  !SECTION - Extraction and transfer of the content.
        # SECTION - Cleaning up
        conf_pki = None
        del conf_pki
        Path(args.cert_file).unlink()
        # !SECTION - Cleaning up
        return 0
    except KeyboardInterrupt:
        return 1
    except Exception as e:
        traceback.print_exc()
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
    passed_files =0
    # Pfad zu den dokumentierenden Tests
    testfiles_dir = Path(__file__).parents[3] / "doc/source/devel"
    test_files = [
        "get_started_programms_server.rst",
        "get_started_programms_intermed.rst",
        "get_started_run_programms_intermed.rst",
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

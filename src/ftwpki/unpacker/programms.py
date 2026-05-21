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
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

from ftwpki.baselibs.configuration import ReaderPKIConfig
from ftwpki.baselibs.core import load_private_key_from_pem
from ftwpki.baselibs.passwd import PasswordManager
from ftwpki.baselibs.transport import RSAPrivateKey, decrypt_transport_package
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
        config:ReaderPKIConfig = ReaderPKIConfig()
        config.read_main_config()
        from_file:dict[str,str]={"configname": config.default_config,}
        parser:UnpackerCliParser  = UnpackerCliParser()
        parser.set_defaults(**from_file)
        args:UnpackerCliProtocol = parser.parse_args(argv)
        config.read_config(args.configname)
        # !SECTION - Configuration
        if args.passphrase_file is not None:
            # SECTION - Passphrasefilehandling
            pwd_man = PasswordManager(private_dir=str(config.private_keys))
            pass_phrase = pwd_man.decrypt_password_file(
                args.passphrase_file, getpass.getpass("Enter Password: ")
            )
          # SECTION - Loading Certificate package and private key
            private_key: RSAPrivateKey = load_private_key_from_pem(
                (config.private_keys / args.private_key).read_bytes(),
                pass_phrase
            )
            # !SECTION - Loading Certificate package and private key
            # !SECTION - Passphrasefilehandling
        else:
            # SECTION - Standardhandling
            # SECTION - Loading Certificate package and private key
            private_key:RSAPrivateKey = load_private_key_from_pem(
                    (config.private_keys / args.private_key).read_bytes(),
                    getpass.getpass("Enter Password: ")
                )
            # !SECTION - Loading Certificate package and private key
            # !SECTION - Standardhandling
        # SECTION - Decrypting the file
        decrypted_zip_bytes:bytes = decrypt_transport_package(
            Path(args.cert_file).read_bytes(),
            private_key,
        )
        # !SECTION - Decrypting the file
        # SECTION - Extraction and installation of the content.
        with ZipFile(BytesIO(decrypted_zip_bytes)) as zf:
            for file_ in zf.namelist():
                ext = "".join(Path(file_).suffixes)
                if ext == config.ext_cert :
                    _=zf.extract(file_, config.certs)
                elif ext == config.ext_public:
                    _=zf.extract(file_, config.public_data)
                elif ext == config.ext_chain:
                    _=zf.extract(file_, config.chains)
                else:
                    _=zf.extract(file_)
        # !SECTION - Extraction and installation of the content.
        return 0
    except KeyboardInterrupt:
        return 1
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
    passed_files =0
    # Pfad zu den dokumentierenden Tests
    testfiles_dir = Path(__file__).parents[3] / "doc/source/devel"
    test_files = [
        "get_started_programms.rst",
        "get_started_programms_intermed.rst",
        "get_started_run_programms.rst",
        # "get_started_programms_old.rst",
        
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

# File: src/ftwpki/userpack/programms.py
# Author: Fitzz TeXnik Welt
# Email: FitzzTeXnikWelt@t-online.de
# License: LGPLv2 or above
"""
programms
===============================


Modul programms documentation
"""
import getpass
import os
from pathlib import Path

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    KeySerializationEncryption,
    PrivateFormat,
    pkcs12,
)

from ftwpki.baselibs._cli_parser import PKIBaseParser
from ftwpki.baselibs.configuration import BasePKIConfig
from ftwpki.baselibs.core import load_private_key_from_pem
from ftwpki.baselibs.protocols import ClientTypeName
from ftwpki.userpack.cli_parser import PKCS12, pkcs12_cli_parser

file_ext:str = ".pfx" if os.name == "nt" else ".p12"

def prog_userpack(argv:list[str]|None = None)->int:
    """
    Process and save a PKCS12 user certificate package.

    This function sets up the configuration for a user client. It parses
    command line arguments, loads private keys, and serializes certificates.
    The final output is saved as a PKCS12 file and can optionally include
    the root CA certificate.

    :param argv: The list of command line arguments for the parser.
    :raises KeyboardInterrupt: If the user stops the program execution.
    :raises Exception: For any errors during configuration or file handling.

    Catch Order: 1. KeyboardInterrupt 2. Exception

    :returns: A status code where 0 is success, 1 is error, and 2 is interrupt.
    """
    try:
        # SECTION - Configuration
        nopasswd:bool=False
        config_type: ClientTypeName = "user"
        parser: PKIBaseParser[PKCS12] = pkcs12_cli_parser()
        args = parser.parse_args(argv)
        pki_name = Path(args.configname).stem
        config: BasePKIConfig = BasePKIConfig(args.configname)
        config.set_config(config_type)
        config.handle_pki_file()
        # !SECTION - Configuration
        # SECTION - Create and save pkcs12 certificate
        priv_key_bytes = config.private_key(args.private_key)
        if b"BEGIN PRIVATE" in priv_key_bytes:
            password = None
            nopasswd=True
        else:
            password = getpass.getpass(f"Password for {args.private_key}: ")
            password = password if password else None
        priv_key_obj = load_private_key_from_pem(priv_key_bytes, password)
        if password:
            if args.old:
                encrypt_algo: KeySerializationEncryption = (
                    PrivateFormat.PKCS12.encryption_builder()
                    .kdf_rounds(50000)
                    .key_cert_algorithm(pkcs12.PBES.PBESv1SHA1And3KeyTripleDESCBC)
                    .hmac_hash(hashes.SHA256())
                    .build(f"{password}".encode())
                )
            else:
                encrypt_algo: KeySerializationEncryption = serialization.BestAvailableEncryption(
                    password.encode()
                )
            
        encrypt_algo = encrypt_algo if not nopasswd else serialization.NoEncryption()
        p12_data = pkcs12.serialize_key_and_certificates(
            name=b"User Certificate",
            key=priv_key_obj,
            cert=config.own_cert,
            cas=config.fullchain,
            encryption_algorithm= encrypt_algo,
        )    
        
        target_path = Path(pki_name).with_suffix(file_ext)
        target_path.write_bytes(p12_data)
        if args.rootca:
            root_cert = config.pki.caroot_cert
            caroot_path = Path(f"{pki_name}-caroot.crt")
            caroot_path.write_bytes(root_cert.public_bytes(Encoding.PEM))

        # !SECTION - Create and save pkcs12 certificate

        return 0
    except KeyboardInterrupt:
        return 2
    except Exception as e:
        print(e)
        return 1


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
        "get_started_userpack_run_programms.rst",
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

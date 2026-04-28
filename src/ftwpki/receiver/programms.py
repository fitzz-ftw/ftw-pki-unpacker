# File: src/ftwpki/receiver/programms.py
# Author: Fitzz TeXnik Welt
# Email: FitzzTeXnikWelt@t-online.de
# License: LGPLv2 or above
"""
programms
===============================


Modul programms documentation
"""

import getpass
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

from ftwpki.baselibs.app_dirs import config_file_path, create_app_pathes
from ftwpki.baselibs.config_file_create import toml_conf_str, write_example_config
from ftwpki.baselibs.core import load_private_key_from_pem
from ftwpki.baselibs.toml_utils import toml2config
from ftwpki.baselibs.transport import decrypt_transport_package
from ftwpki.receiver.cli_parser import ReceiverCliParser

get_password = getpass.getpass


def prog_receive_certs(argv: list[str] | None = None, **kwargs):
    try:
        # SECTION - Configuration
        if not config_file_path().is_file():
            write_example_config(toml_conf_str)
        config = toml2config()
        parser = ReceiverCliParser()
        args = parser.parse_args(argv)
        dirs_to_create = [path for path in config if not path.startswith("ext")]
        pathconf = create_app_pathes(config, ["private_keys", "passphrases"], *dirs_to_create)
        # !SECTION - Configuration
        # SECTION - Loading Certificate package and private key
        enc_value = Path(args.cert_file).read_bytes()
        current_private_key_path = pathconf["private_keys"] / args.private_key
        private_key = load_private_key_from_pem(
            current_private_key_path.read_bytes(), get_password("Enter Password: ")
        )
        #!SECTION - Loading Certificate package and private key
        # SECTION - Decrypting the file
        decrypted_zip_bytes = decrypt_transport_package(
            enc_value,
            private_key,
        )
        # !SECTION - Decrypting the file
        # SECTION - Extraction and installation of the content.
        with ZipFile(BytesIO(decrypted_zip_bytes)) as zf:
            for file_ in zf.namelist():
                ext= Path(file_).suffix
                if ext == config["ext_cert"] :
                    _=zf.extract(file_, pathconf["certs"])
                elif ext == config["ext_public"]:
                    _=zf.extract(file_, pathconf["public_data"])
                elif ext == config["ext_chain"]:
                    _=zf.extract(file_, pathconf["chains"])
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

    # Pfad zu den dokumentierenden Tests
    testfiles_dir = Path(__file__).parents[3] / "doc/source/devel"
    test_file = testfiles_dir / "get_started_programms.rst"

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

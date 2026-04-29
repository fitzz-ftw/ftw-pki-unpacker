The ftwpkirecieiver programm
=============================

.. SECTION - Setup Test-Environment

>>> test_transport_package="testtransport.zip.enc"
>>> from pathlib import Path
>>> from fitzzftw.devtools.testinfra import TestHomeEnvironment
>>> env = TestHomeEnvironment(Path("doc/source/devel/testhome"))
>>> env.setup()
>>> _ = env.copy2cwd(test_transport_package)
>>> Path("tests_pki_root").mkdir(parents=True, exist_ok=True)
>>> _ = env.copy2cwd("tests_pki_root/ca.crt")
>>> _ = env.copy2cwd("tests_pki_root/ca.key")

.. !SECTION - Setup Test-Environment

.. SECTION - Perpare Test 

>>> import time

>>> class StubPassword:
...     def __init__(self):
...         self.generate = self._generate()
...     def _generate(self):
...         # first run 
...         yield "1234"
...     def __call__(self, prompt):
...         print(prompt, flush=True)
...         return next(self.generate)

>>> stubpwinput = StubPassword()

>>> sys_argv = ["ca.key",test_transport_package,]

.. !SECTION - Perpare Test 

>>> get_password=stubpwinput

.. SECTION - Configuration

>>> from ftwpki.baselibs.config_file_create import write_example_config, toml_conf_str 

>>> from ftwpki.baselibs.app_dirs import config_file_path

>>> if not config_file_path().is_file():
...     write_example_config(toml_conf_str)

>>> from ftwpki.baselibs.toml_utils import toml2config

>>> config = toml2config()
>>> config #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
{'private_keys': '~/.config/ftwpki/.private', 
 'passphrases': '~/.config/ftwpki/.private', 
 'csr_configs': '~/.config/ftwpki/csr', 
 'policies': '~/.config/ftwpki/policies', 
 'public_data': '~/.local/share/ftwpki', 
 'certs': '~/.local/share/ftwpki/certs', 
 'chains': '~/.local/share/ftwpki/chains', 
 'ext_cert': '.crt', 
 'ext_public': '.pub', 
 'ext_chain': '.pem', 
 'ext_csr_conf': '.toml', 
 'ext_policy': '.policy', 
 'ext_signedcert': '.zip.enc'}

>>> from ftwpki.receiver.cli_parser import ReceiverCliParser

>>> parser = ReceiverCliParser("ftwpkirecieiver")

>>> parser #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
ReceiverCliParser(prog='ftwpkirecieiver', 
    usage=None, description=None, 
    formatter_class=<class 'argparse.HelpFormatter'>, 
    conflict_handler='error', 
    add_help=True)

>>> parser.print_help() #doctest: +NORMALIZE_WHITESPACE
usage: ftwpkirecieiver [-h] private_key cert_file
<BLANKLINE>
positional arguments:
    private_key  The private key file name.
    cert_file    The path of the encrypted certificate package
<BLANKLINE>
options:
    -h, --help   show this help message and exit

>>> args = parser.parse_args(sys_argv)

>>> args
Namespace(private_key='ca.key', cert_file='testtransport.zip.enc')

.. SECTION - Create Directories from Configuration for testing needs only

>>> dirs_to_create = [path for path in config if not path.startswith("ext")]

>>> dirs_to_create
['private_keys', 'passphrases', 'csr_configs', 'policies', 'public_data', 'certs', 'chains']

>>> from ftwpki.baselibs.app_dirs import create_app_pathes
>>> pathconf=create_app_pathes(config,['private_keys','passphrases' ], *dirs_to_create)


.. ANCHOR - Copy Privatkey and Certifikate

>>> from shutil import copy2
>>> priv_key_path=copy2("tests_pki_root/ca.key", Path(config['private_keys']).expanduser())
>>> cert_path=copy2("tests_pki_root/ca.crt", Path(config['certs']).expanduser())

.. !SECTION - Create Directories from Configuration

.. !SECTION - Configuration

.. SECTION - Loading Certificate package and private key

>>> enc_value=Path(args.cert_file).read_bytes()


>>> current_private_key_path = pathconf['private_keys']/ args.private_key

>>> from ftwpki.baselibs.core import load_private_key_from_pem

>>> private_key = load_private_key_from_pem(current_private_key_path.read_bytes(), 
...     get_password("Enter Password: ")) #doctest: +NORMALIZE_WHITESPACE
Enter Password:


.. !SECTION - Loading Certificate package and private key


.. SECTION - Decrypting the file 

>>> from ftwpki.baselibs.transport import decrypt_transport_package
>>> decrypted_zip_bytes = decrypt_transport_package(
...     enc_value,
...     private_key,
... )

>>> decrypted_zip_bytes.startswith(b'PK')
True

.. !SECTION - Decrypting the file 

.. SECTION - Extraction and installation of the content.

>>> from io import BytesIO
>>> from zipfile import ZipFile

>>> zf = ZipFile(BytesIO(decrypted_zip_bytes))
>>> zf.infolist() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
[<ZipInfo filename='user.crt' 
    compress_type=deflate 
    filemode='?rw-------' 
    file_size=1996 
    compress_size=1503>, 
 <ZipInfo filename='certificate_chain.pem' 
    compress_type=deflate 
    filemode='?rw-------' 
    file_size=1995 
    compress_size=1503>, 
 <ZipInfo filename='ca.crt' 
    compress_type=deflate 
    filemode='?rw-------' 
    file_size=1996 
    compress_size=1503>]

>>> zf.namelist()
['user.crt', 'certificate_chain.pem', 'ca.crt']


>>> for file_ in zf.namelist():
...     ext= Path(file_).suffix
...     if ext == config["ext_cert"] :
...         _=zf.extract(file_, pathconf["certs"])
...     elif ext == config["ext_public"]:
...         _=zf.extract(file_, pathconf["public_data"])
...     elif ext == config["ext_chain"]:
...         _=zf.extract(file_, pathconf["chains"])
...     else:
...         _=zf.extract(file_)

>>> zf.close()

.. !SECTION - Extraction and installation of the content.



.. SECTION - Teardown Test-Environment

>>> env.clean_home()
>>> env.teardown()

.. !SECTION - Teardown Test-Environment


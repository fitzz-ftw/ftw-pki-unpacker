The ftwpki-unpacker program
=============================

.. SECTION - Setup Test-Environment

>>> test_transport_package = "testtransport.zip.enc"
>>> from pathlib import Path
>>> from fitzzftw.devtools.testinfra import TestHomeEnvironment

Schritt 1: Initialisieren der frischen Sandbox via ftw-devtools-0.3.0
>>> env = TestHomeEnvironment(Path("doc/source/devel/testhome"),
...     appname="ftwpki", appauthor="FitzzTeXnikWelt")
>>> env.setup()
>>> env.clean_home()
>>> env.clean_output()

Schritt 2: Wir instanziieren die reale IntermedPKIConfig. Sie schreibt die 
Konfiguration und erzeugt die komplette Ordnerstruktur physisch auf der Platte!
>>> from ftwpki.baselibs.configuration import UserPKIConfig
>>> cfg = UserPKIConfig()
>>> cfg.set_config()

>>> _ = env.copy2config("tests_pki_root/ca.key",".private/ca.key")

>>> _ =env.copy2cwd("testtransport.zip.enc")

.. !SECTION - Setup Test-Environment

.. SECTION - Perpare Test 

>>> import time
>>> class StubPassword:
...     def __init__(self):
...         self.generate = self._generate()
...     def _generate(self):
...         yield "1234"
...     def __call__(self, prompt):
...         print(prompt, flush=True)
...         return next(self.generate)

>>> stubpwinput = StubPassword()

Schritt 3: Globales getpass patchen, BEVOR das Programmmodul geladen wird!

>>> import getpass
>>> getpass.getpass = stubpwinput

Schritt 4: Jetzt das Modul importieren – es übernimmt sofort den globalen Patch:

>>> from ftwpki.unpacker import programms

>>> 

>>> sys_argv = ["ca.key", test_transport_package]

.. !SECTION - Perpare Test 

.. SECTION - Start programm: prog_receive_certs

.. SECTION - Configuration

>>> from ftwpki.baselibs.configuration import ReaderPKIConfig

>>> config:ReaderPKIConfig = ReaderPKIConfig()

>>> config.read_main_config()

>>> config.default_config
'user.toml'

>>> from_file:dict[str,str]={"configname": config.default_config,}

>>> from ftwpki.unpacker.cli_parser import UnpackerCliParser

>>> parser:UnpackerCliParser  = UnpackerCliParser()
>>> parser.set_defaults(**from_file)

>> parser.print_help()

>>> from ftwpki.unpacker.protocols import UnpackerCliProtocol

>>> args:UnpackerCliProtocol = parser.parse_args(sys_argv)

>>> args
Namespace(private_key='ca.key', cert_file='testtransport.zip.enc', passphrase_file=None, configname='user.toml')

>>> config.read_config(args.configname)


.. !SECTION - Configuration

.. SECTION - Standardhandling
.. SECTION - Loading Certificate package and private key

>>> from ftwpki.baselibs.core import load_private_key_from_pem
>>> from ftwpki.baselibs.transport import RSAPrivateKey, decrypt_transport_package



Der Aufruf nutzt durch den frühen Import-Patch direkt den globalen Stub:
>>> private_key:RSAPrivateKey = load_private_key_from_pem(
...     (config.private_keys / args.private_key).read_bytes(), 
...     getpass.getpass("Enter Password: ")
... )
Enter Password: 

.. !SECTION - Loading Certificate package and private key
.. !SECTION - Standardhandling

.. SECTION - Decrypting the file 

>>> from ftwpki.baselibs.transport import decrypt_transport_package

>>> decrypted_zip_bytes:bytes = decrypt_transport_package(
...     Path(args.cert_file).read_bytes(),
...     private_key,
... )

>>> decrypted_zip_bytes.startswith(b'PK')
True

.. !SECTION - Decrypting the file 

.. SECTION - Extraction and installation of the content.

>>> from io import BytesIO

>>> from zipfile import ZipFile

>>> zf:ZipFile = ZipFile(BytesIO(decrypted_zip_bytes))
>>> for file_ in zf.namelist():
...     ext= Path(file_).suffix
...     if ext == config.ext_cert :
...         _=zf.extract(file_, config.certs)
...     elif ext == config.ext_public:
...         _=zf.extract(file_, config.public_data)
...     elif ext == config.ext_chain:
...         _=zf.extract(file_, config.chains)
...     else:
...         _=zf.extract(file_)
>>> zf.close()

.. !SECTION - Extraction and installation of the content.

.. !SECTION - End proggramm: prog_receive_certs

.. SECTION - Tests

>>> from platformdirs import user_config_path, user_data_path
>>> conf_path:Path = user_config_path(appname="ftwpki", appauthor="FitzzTeXnikWelt") 
>>> public_path:Path = user_data_path(appname="ftwpki", appauthor="FitzzTeXnikWelt")

>>> (conf_path / ".private"/ "ca.key.pem").is_file()
False

>>> (public_path / "certs"/ "ca.crt.pem").is_file()
False

>>> (public_path / "certs"/ "user.crt.pem").is_file()
False

>>> (public_path / "chains" / "certificate_chain.chain.pem").is_file()
False


>>> (conf_path / ".private"/ "ca.key").is_file()
True

>>> Path("ca.crt").is_file()
True

>>> Path("user.crt").is_file()
True

>>> Path("certificate_chain.pem").is_file()
True

.. !SECTION - Tests


.. SECTION - Teardown

>> env.clean_home()
>>> env.teardown()

.. !SECTION Teardown

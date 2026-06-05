The ftwpki-unpacker program for intermediate
=============================================

.. SECTION - Setup Test-Environment

>>> test_transport_package = ""
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

>>> from ftwpki.baselibs.configuration import IntermedPKIConfig
>>> cfg = IntermedPKIConfig()
>>> cfg.set_config()

>>> del cfg


>>> test_data_dir = "test-server-data"
>>> private_key_file_name = "member-web.key.pem"
>>> pki_conf_file = "M-V-HH-Members.pki"
>>> pki_transport = "M-V-HH-Members.spki"

>>> _ = env.copy2config(f"{test_data_dir}/{private_key_file_name}",
...     f".private/{private_key_file_name}")
>>> _ = env.copy2data(f"{test_data_dir}/{pki_conf_file}",f"{pki_conf_file}")
>>> _ =env.copy2cwd(f"{test_data_dir}/{pki_transport}", f"{pki_transport}")

.. !SECTION - Setup Test-Environment

.. SECTION - Perpare Test 

>>> import time
>>> class StubPassword:
...     def __init__(self):
...         self.generate = self._generate()
...     def _generate(self):
...         yield "secret"
...     def __call__(self, prompt):
...         print(prompt, flush=True)
...         return next(self.generate)

>>> stubpwinput = StubPassword()

Schritt 3: Globales getpass patchen, BEVOR das Programmmodul geladen wird!

>>> import getpass
>>> getpass.getpass = stubpwinput

Schritt 4: Jetzt das Modul importieren – es übernimmt sofort den globalen Patch:

>>> from ftwpki.unpacker import programms


>>> sys_argv = ["-c","server", "member-web.key.pem", pki_transport]

.. !SECTION - Perpare Test 

.. SECTION - Start programm: prog_receive_certs

.. SECTION - Configuration

>>> from ftwpki.unpacker.cli_parser import UnpackerCliParser

>>> parser:UnpackerCliParser  = UnpackerCliParser()

>> parser.print_help()

>>> from ftwpki.unpacker.protocols import UnpackerCliProtocol

>>> args:UnpackerCliProtocol = parser.parse_args(sys_argv)

>>> args #doctest: +NORMALIZE_WHITESPACE
Namespace(private_key='member-web.key.pem', 
    cert_file='M-V-HH-Members.spki', 
    passphrase_file=None, 
    configname='server')



>>> from ftwpki.baselibs.configuration import RootSignerPKIConfig

>>> config:RootSignerPKIConfig = RootSignerPKIConfig(args.cert_file)

>>> config.set_config(args.configname)

>>> config.current_configfile_entries #doctest: +NORMALIZE_WHITESPACE
{'private_keys': '#config#.private', 
 'zip': '#data#', 
 'certs': '#zip#', 
 'chains': '#zip#', 
 'config_path': '#config#', 
 'data_path': '#data#'}

>>> config.handle_pki_file()

.. !SECTION - Configuration

>>> ppf = args.configname == "intermediate" 

>>> ppf
False

.. SECTION - Loading private key

>>> private_key_name:str = args.private_key

>>> enc = b"ENCRYPTED PRIVATE" in config.private_key(private_key_name)

>>> enc
False

>>> pass_phrase = getpass.getpass("Enter Password: ") if enc else None; print("Enter Password: ")
Enter Password: 

>>> from ftwpki.baselibs.core import load_private_key_from_pem
>>> from ftwpki.baselibs.transport import RSAPrivateKey

>>> private_key:RSAPrivateKey = load_private_key_from_pem(
...     config.private_key(private_key_name), 
...     pass_phrase
... ) 

>>> isinstance(private_key, RSAPrivateKey)
True

.. !SECTION - Loading private key

.. SECTION - Decrypting and Loading the file 

>>> from ftwpki.baselibs.package import PKIPackage
>>> pack = PKIPackage()
>>> pack.private_key = private_key
>>> del private_key
>>> pack.load(args.cert_file)
>>> del pack.private_key

.. !SECTION - Decrypting and Loading the file 

.. SECTION - Extraction and transfer of the content.

>>> conf_pki = config.pki

>>> conf_pki.fullchain.extend(pack.fullchain)
>>> conf_pki.ca_cert = pack.ca_cert

>>> conf_pki.caroot_cert = pack.caroot_cert
>>> conf_pki.own_cert = pack.own_cert
>>> conf_pki.intermediatechain.extend(pack.intermediatechain)
>>> conf_pki.additional_files.update(pack.additional_files)
>>> _ = conf_pki.save()

.. !SECTION - Extraction and transfer of the content.
.. SECTION - Cleaning up

>>> conf_pki = None
>>> del conf_pki

>>> Path(args.cert_file).unlink()

.. !SECTION - Cleaning up


.. !SECTION - End proggramm: prog_receive_certs



.. SECTION - Teardown

>> env.clean_home()
>>> env.teardown()

.. !SECTION Teardown

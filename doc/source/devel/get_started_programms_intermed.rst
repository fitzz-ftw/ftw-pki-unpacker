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


>>> test_data_dir = "data-unpacker/data-inter-base"
>>> passphraese_file_name = "inter1secret"
>>> pki_conf_file = "M-V-HH-CA.pki"
>>> pki_transport = "M-V-HH-CA.spki"

>>> _ = env.copy2config(f"{test_data_dir}/{passphraese_file_name}",
...     f".private/{passphraese_file_name}")
>>> _ = env.copy2config(f"{test_data_dir}/{pki_conf_file}",f".private/{pki_conf_file}")
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


>>> sys_argv = ["-c","intermediate", "inter1secret", pki_transport]

.. !SECTION - Perpare Test 

.. SECTION - Start programm: prog_receive_certs

.. SECTION - Configuration

>>> from ftwpki.unpacker.cli_parser import UnpackerCliParser

>>> parser:UnpackerCliParser  = UnpackerCliParser()

>> parser.print_help()

>>> from ftwpki.unpacker.protocols import UnpackerCliProtocol

>>> args:UnpackerCliProtocol = parser.parse_args(sys_argv)

>>> args #doctest: +NORMALIZE_WHITESPACE
UnpackerCliArguments(cert_file='M-V-HH-CA.spki'
configname='intermediate'
passphrase_file='None'
private_key='inter1secret')



>>> from ftwpki.baselibs.configuration import RootSignerPKIConfig

>>> config:RootSignerPKIConfig = RootSignerPKIConfig(args.cert_file)

>>> config.set_config(args.configname)

>>> config.current_configfile_entries #doctest: +NORMALIZE_WHITESPACE
{'private_keys': '#zip#', 
 'zip': '#config#.private', 
 'certs': '#zip#', 
 'chains': '#zip#', 
 'passphrases': '#config#.private', 
 'policies': '#zip#', 
 'config_path': '#config#', 
 'data_path': '#data#'}

>>> config.handle_pki_file()

.. !SECTION - Configuration

>>> ppf = args.configname == "intermediate" 

>>> if ppf:
...     print("This part until '!SECTION - Passphrasefilehandling'")
This part until '!SECTION - Passphrasefilehandling'

.. SECTION - Passphrasefilehandling

>>> from ftwpki.baselibs.passwd import PasswordManager
>>> pwd_man = PasswordManager(private_dir=str(config.passphrases)) 

>>> pwd_man #doctest: +ELLIPSIS
PasswordManager(private_dir='...ftwpki/.private')


>>> pass_phrase = pwd_man.decrypt_password_file(args.private_key, getpass.getpass("Enter Password: "))
Enter Password: 

>>> pass_phrase == "lökjdfaijndbjefrzuiexhLOHioIHUOIH987621929OPLNl*'khjGZO}"
True
>>> del pwd_man

.. !SECTION - Passphrasefilehandling

else:

>>> pass_phrase = getpass.getpass("Enter Password: ") #doctest: +SKIP
Enter Password: 

.. SECTION - Loading private key

>>> from ftwpki.baselibs.core import load_private_key_from_pem
>>> from ftwpki.baselibs.transport import RSAPrivateKey, decrypt_transport_package

Der Aufruf nutzt durch den frühen Import-Patch direkt den globalen Stub:




>>> private_key:RSAPrivateKey = load_private_key_from_pem(
...     config.private_key(), 
...     pass_phrase
... ) 

>>> del pass_phrase

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

.. SECTION - Tests

>> from platformdirs import user_config_path, user_data_path
>> conf_path:Path = user_config_path(appname="ftwpki", appauthor="FitzzTeXnikWelt") 
>> public_path:Path = user_data_path(appname="ftwpki", appauthor="FitzzTeXnikWelt")

>> (conf_path / ".private"/ "intermed1.key.pem").is_file()
True

>> (public_path / "certs"/ "ca.crt.pem").is_file()
True

>> (public_path / "certs"/ "Muster-Verband-eV_Hamburg.crt.pem").is_file()
True

>> (public_path / "chains" / "all.chain.pem").is_file()
True



>> Path("ca.crt").is_file()
False

>> Path("user.crt").is_file()
False

>> Path("certificate_chain.pem").is_file()
False

.. !SECTION - Tests


.. SECTION - Teardown

>> env.clean_home()
>>> env.teardown()

.. !SECTION Teardown

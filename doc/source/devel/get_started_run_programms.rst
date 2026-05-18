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
>>> from ftwpki.baselibs.configuration import IntermedPKIConfig
>>> cfg = IntermedPKIConfig()
>>> cfg.set_config()

>>> _ = env.copy2config("tests_pki_root/ca.key",".private/ca.key")

>>> _ =env.copy2cwd("testtransport.zip.enc")

.. !SECTION - Setup Test-Environment

.. SECTION - Perpare Test 

>>> import time
>>> class StubPassword:
...     def __init__(self):
...         self.reset()
...     def _generate(self):
...         yield "1234"
...         raise KeyboardInterrupt
...     def __call__(self, prompt):
...         print(prompt, flush=True)
...         return next(self.generate)
...     def reset(self):
...         self.generate = self._generate()
>>> stubpwinput = StubPassword()

Schritt 3: Globales getpass patchen, BEVOR das Programmmodul geladen wird!
>>> import getpass
>>> getpass.getpass = stubpwinput

Schritt 4: Jetzt das Modul importieren – es übernimmt sofort den globalen Patch:
>>> from ftwpki.unpacker import programms

>>> 

>>> sys_argv = ["ca.key", test_transport_package]

.. !SECTION - Perpare Test 

>>> from ftwpki.unpacker.programms import prog_unpacker_certs

>>> prog_unpacker_certs(sys_argv)
Enter Password: 
0

>>> prog_unpacker_certs(sys_argv)
Enter Password: 
1

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

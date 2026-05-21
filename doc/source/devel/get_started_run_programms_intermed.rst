The ftwpki-unpacker program for intermediate
=============================================

.. SECTION - Setup Test-Environment

>>> test_transport_package = "Muster-Verband-eV_Hamburg.zip.enc"
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

>>> _ = env.copy2config("test_files/intermed1.key.pem",".private/intermed1.key.pem")
>>> _ = env.copy2config("test_files/inter1secret",".private/inter1secret")


>>> _ =env.copy2cwd("test_files/Muster-Verband-eV_Hamburg.zip.enc", "Muster-Verband-eV_Hamburg.zip.enc")

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



>>> sys_argv = ["intermed1.key.pem", test_transport_package, "inter1secret"]

>>> from ftwpki.unpacker.programms import prog_unpacker_certs

>>> prog_unpacker_certs(sys_argv)
Enter Password: 
0

>> prog_receive_certs(sys_argv)


.. SECTION - Teardown

>>> env.clean_home()
>>> env.teardown()

.. !SECTION Teardown


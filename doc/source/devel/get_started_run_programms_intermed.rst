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
...     def reset(self):
...         self.generate = self._generate()

>>> def stub_keyboard_interrupt(prompt:str)->str:
...     print(prompt)
...     raise KeyboardInterrupt

>>> def stub_exception(prompt:str):
...     raise Exception("Test exception!")



>>> stubpwinput = StubPassword()

Schritt 3: Globales getpass patchen, BEVOR das Programmmodul geladen wird!

>>> import getpass
>>> getpass.getpass = stubpwinput

Schritt 4: Jetzt das Modul importieren – es übernimmt sofort den globalen Patch:

>>> sys_argv = ["-c","intermediate", "test", pki_transport, "inter1secret"]

.. !SECTION - Perpare Test 

.. ANCHOR - Start programm: prog_receive_certs

>>> from ftwpki.unpacker.programms import prog_unpacker_certs

>>> prog_unpacker_certs(sys_argv)
Enter Password: 
0

>>> getpass.getpass = stub_keyboard_interrupt
>>> prog_unpacker_certs(sys_argv)
Enter Password: 
1

>>> getpass.getpass = stub_exception
>>> prog_unpacker_certs(sys_argv)
Test exception!
1

Server Test
-------------

.. SECTION - Test Server

>>> test_data_dir = "data-unpacker/data-server"
>>> private_key_file_name = "member-web.key.pem"
>>> pki_conf_file = "M-V-HH-Members.pki"
>>> pki_transport = "M-V-HH-Members.spki"

>>> _ = env.copy2config(f"{test_data_dir}/{private_key_file_name}",
...     f".private/{private_key_file_name}")
>>> _ = env.copy2data(f"{test_data_dir}/{pki_conf_file}",f"{pki_conf_file}")
>>> _ =env.copy2cwd(f"{test_data_dir}/{pki_transport}", f"{pki_transport}")

>>> sys_argv = ["-c","server", "member-web.key.pem", pki_transport]

>>> prog_unpacker_certs(sys_argv)
0

.. !SECTION - Test Server

Test 'User'
------------

.. SECTION - Test User

>>> test_data_dir = "data-unpacker/data-user"
>>> private_key_file_name = "max_m_v.key.pem"
>>> pki_conf_file = "M-V-HH-MaxMustermann.pki"
>>> pki_transport = "M-V-HH-MaxMustermann.spki"

>>> _ = env.copy2config(f"{test_data_dir}/{private_key_file_name}",
...     f".private/{private_key_file_name}")
>>> _ = env.copy2data(f"{test_data_dir}/{pki_conf_file}",f"{pki_conf_file}")
>>> _ =env.copy2cwd(f"{test_data_dir}/{pki_transport}", f"{pki_transport}")

>> _ = env.copy2config("test-user-data/max_m_v.key.pem", ".private/max_m_v.key.pem")
>> _ = env.copy2data("test-user-data/M-V-HH-MaxMustermann.pki", "M-V-HH-MaxMustermann.pki")
>> _ = env.copy2cwd("test-user-data/M-V-HH-MaxMustermann.spki", "M-V-HH-MaxMustermann.spki")

>>> import shlex

>>> cmd_line = "ftwpkiunpacker -c user "
>>> cmd_line += " max_m_v.key.pem "
>>> cmd_line += " M-V-HH-MaxMustermann.spki "
>>> sys_argv = shlex.split(cmd_line)[1:]
>>> sys_argv #doctest: +NORMALIZE_WHITESPACE
['-c', 'user', 'max_m_v.key.pem', 'M-V-HH-MaxMustermann.spki']


>>> getpass.getpass = stubpwinput

>>> getpass.getpass.reset()

>>> Path('M-V-HH-MaxMustermann.spki').exists()
True

>>> prog_unpacker_certs(sys_argv)
Enter Password: 
0




.. !SECTION - Test User


.. SECTION - Teardown

>>> env.clean_home()
>>> env.teardown()

.. !SECTION Teardown

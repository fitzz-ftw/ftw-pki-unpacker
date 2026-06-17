The Certificat Sign Request Creation
#########################################




.. SECTION - Setup

>>> from fitzzftw.devtools.testinfra import TestHomeEnvironment
>>> from pathlib import Path
>>> env = TestHomeEnvironment(Path("doc/source/devel/testhome"),
...     appname="ftwpki", appauthor="FitzzTeXnikWelt")

>>> env.setup(True)
>>> env.clean_home()

.. !SECTION - Setup
.. SECTION - Prepare

>>> from pathlib import Path

>>> def stub_exception(*args,**kwargs):
...     raise Exception("This is a testexception")


Schritt 2: Wir instanziieren die reale IntermedPKIConfig. Sie schreibt die 
Konfiguration und erzeugt die komplette Ordnerstruktur physisch auf der Platte!

>>> from ftwpki.baselibs.configuration import IntermedPKIConfig
>>> cfg = IntermedPKIConfig()
>>> cfg.set_config()

>>> del cfg

>>> test_data_dir = "data-userpack"
>>> pki_conf_file = "M-V-HH-MaxMustermann.pki"
>>> private_key_file_name = "max_m_v.key.pem"

>>> _ = env.copy2config(f"{test_data_dir}/{private_key_file_name}",
...     f".private/{private_key_file_name}")
>>> _ = env.copy2data(f"{test_data_dir}/{pki_conf_file}",f"{pki_conf_file}")


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

>>> stubpwinput = StubPassword()

>>> def stub_keyboard_interrupt(prompt:str)->str:
...     print(prompt)
...     raise KeyboardInterrupt

>>> def stub_exception(prompt:str):
...     raise Exception("Test exception!")




Schritt 3: Globales getpass patchen, BEVOR das Programmmodul geladen wird!

>>> import getpass
>>> getpass.getpass = stubpwinput

Schritt 4: Jetzt das Modul importieren – es übernimmt sofort den globalen Patch:

>>> from ftwpki.userpack.programms import prog_userpack



>>> cmd_line="M-V-HH-MaxMustermann.toml  "

>> cmd_line += "-o -k max_m_v"

>>> cmd_line += "-c -k max_m_v"

>>> import shlex
>>> sys_argv= shlex.split(cmd_line) 
>>> sys_argv #doctest: +NORMALIZE_WHITESPACE
['M-V-HH-MaxMustermann.toml', '-c', '-k', 'max_m_v']

['M-V-HH-MaxMustermann.toml', '-k', 'max_m_v']

['M-V-HH-MaxMustermann.toml', '-o', '-k', 'max_m_v']


>>> prog_userpack(sys_argv) #doctest: +NORMALIZE_WHITESPACE
Password for max_m_v.key.pem:
0

>>> getpass.getpass = stub_keyboard_interrupt
>>> prog_userpack(sys_argv) #doctest: +NORMALIZE_WHITESPACE
Password for max_m_v.key.pem: 
2

>>> getpass.getpass = stub_exception
>>> prog_userpack(sys_argv) #doctest: +NORMALIZE_WHITESPACE
Test exception!
1

>>> getpass.getpass = stubpwinput
>>> getpass.getpass.reset()
>>> cmd_line="M-V-HH-MaxMustermann.toml  "
>>> cmd_line += "-o -k max_m_v"
>>> sys_argv= shlex.split(cmd_line) 
>>> prog_userpack(sys_argv) #doctest: +NORMALIZE_WHITESPACE
Password for max_m_v.key.pem:
0

>>> test_data_dir = "data-remotepack/data-server"
>>> pki_conf_file = "M-V-HH-Members.pki"
>>> private_key_file_name = "member-web.key.pem"

>>> _ = env.copy2config(f"{test_data_dir}/{private_key_file_name}",
...     f".private/{private_key_file_name}")
>>> _ = env.copy2data(f"{test_data_dir}/{pki_conf_file}",f"{pki_conf_file}")

>>> cmd_line="M-V-HH-Members.toml  "
>>> cmd_line += " -k member-web"
>>> sys_argv= shlex.split(cmd_line) 

>>> prog_userpack(sys_argv) #doctest: +NORMALIZE_WHITESPACE
0







.. !SECTION - Prepare


.. SECTION - Teardown

>>> env.clean_home()
>>> env.teardown()


.. !SECTION - Teardown

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

>>> import getpass

>>> from pathlib import Path

>>> def stub_exception(*args,**kwargs):
...     raise Exception("This is a testexception")


Schritt 2: Wir instanziieren die reale IntermedPKIConfig. Sie schreibt die 
Konfiguration und erzeugt die komplette Ordnerstruktur physisch auf der Platte!

>>> from ftwpki.baselibs.configuration import IntermedPKIConfig
>>> cfg = IntermedPKIConfig()
>>> cfg.set_config()

>>> del cfg

>>> test_data_dir = "data-remotepack/data-server"
>>> pki_conf_file = "M-V-HH-Members.pki"
>>> private_key_file_name = "member-web.key.pem"

>>> _ = env.copy2config(f"{test_data_dir}/{private_key_file_name}",
...     f".private/{private_key_file_name}")
>>> _ = env.copy2data(f"{test_data_dir}/{pki_conf_file}",f"{pki_conf_file}")

>>> cmd_line="M-V-HH-Members.toml  "
>>> cmd_line += " -k member-web"

>>> import shlex
>>> sys_argv= shlex.split(cmd_line) 
>>> sys_argv #doctest: +NORMALIZE_WHITESPACE
['M-V-HH-Members.toml', '-k', 'member-web']

>>> from ftwpki.remotepack.programms import prog_remotepack

>>> prog_remotepack(sys_argv)
0

>>> cmd_line="M-V-HH-Members.toml  "
>>> cmd_line += " -f DER -k member-web"
>>> sys_argv= shlex.split(cmd_line) 

>>> prog_remotepack(sys_argv)
0


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

>>> getpass.getpass = stubpwinput

>>> cmd_line="M-V-HH-MaxMustermann.toml  "

>>> cmd_line += " -k max_m_v"

>>> sys_argv= shlex.split(cmd_line) 

>>> prog_remotepack(sys_argv)
Password for max_m_v.key.pem: 
At least path for fullchain is empty.
1

>>> getpass.getpass = stub_keyboard_interrupt
>>> prog_remotepack(sys_argv)
Password for max_m_v.key.pem: 
2



.. !SECTION - Prepare


.. SECTION - Teardown

>> env.clean_home()
>>> env.teardown()


.. !SECTION - Teardown

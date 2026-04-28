

>>> from pathlib import Path
>>> from fitzzftw.devtools.testinfra import TestHomeEnvironment
>>> env = TestHomeEnvironment(Path("doc/source/devel/testhome"))
>>> env.setup()
>>> _ = env.copy2cwd("password.txt")

>>> import time

>>> class StubPassword:
...     def __init__(self):
...         self.generate = self._generate()
...     def _generate(self):
...         # first run 
...         yield "secret"
...         time.sleep(2)
...         yield "secret"
...     def __call__(self, prompt):
...         print(prompt, flush=True)
...         return next(self.generate)

>>> stubpwinput = StubPassword()

>>> sys_argv = ["mypasswordfile",]

>>> from ftwpki.password.cli_parser import PasswordFileParser

>>> pfp = PasswordFileParser()
>>> args = pfp.parse_args(sys_argv) # doctest: +NORMALIZE_WHITESPACE

>>> from ftwpki.password.passwd_file import PasswdFile
>>> pwd_file = PasswdFile(args, require_terminal=False, pwcall=stubpwinput)

>>> pwd_file.encrypt()
Password for 'mypasswordfile': 
Retype password: 
0

>>> from ftwpki.password.programms import prog_password_enc
>>> stubpwinput = StubPassword()

>>> prog_password_enc(sys_argv, require_terminal=False, pwcall=stubpwinput)
Password for 'mypasswordfile': 
Retype password: 
0



>>> env.clean_home()
>>> env.teardown()


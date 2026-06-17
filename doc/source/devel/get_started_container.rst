Get started with Containers
================================

>>> from ftwpki.remotepack.container import RemoteKeys

>>> remkeys = RemoteKeys()

>>> remkeys.items() #doctest: +ELLIPSIS -SKIP
Traceback (most recent call last):
    ...
KeyError: AttributeError("'...RemoteKeys' object has no attribute '_fullchain'")

>>> from ftwpki.remotepack.container import RemotePathes

>>> remo_path = RemotePathes()

>>> remo_path.fullchain = "fulchain-path"

>>> remo_path.fullchain
'fulchain-path'

>>> remo_path.rootca = "root-ca-path"
>>> remo_path.rootca
'root-ca-path'

>>> remo_path.private_key = "piv-key-path"
>>> remo_path.private_key
'piv-key-path'

>>> remo_path["fullchain"] = "another-path"
>>> remo_path.fullchain
'another-path'

>>> "private_key" in remo_path
True


>>> from ftwpki.remotepack.container import RemoteContent

>>> rem_cont = RemoteContent()

>>> rem_cont.fullchain
[]

>>> rem_cont.rootca


>>> rem_cont.private_key

>>> from ftwpki.remotepack.container import PKIRemoteContainer

>>> container = PKIRemoteContainer()

>>> container.fullchain
[]

>>> container.private_key

>>> container.caroot_cert

>>> from fitzzftw.devtools.testinfra import TestHomeEnvironment
>>> from pathlib import Path
>>> env = TestHomeEnvironment(Path("doc/source/devel/testhome"),
...     appname="ftwpki", appauthor="FitzzTeXnikWelt")

>>> env.setup(True)
>>> env.clean_home()
>>> test_data_dir = "data-remotepack/container"
>>> toml_conf_file = "double_path.toml"
>>> pki_conf_file = "M-V-HH-Members.pki"
>>> priv_key_file = "member-web.key.pem"

>>> _ = env.copy2cwd(f"{test_data_dir}/{toml_conf_file}",f"{toml_conf_file}")
>>> pki_path = env.copy2cwd(f"{test_data_dir}/{pki_conf_file}",f"{pki_conf_file}")
>>> privkey_path = env.copy2cwd(f"{test_data_dir}/{priv_key_file}",f"{priv_key_file}")

>>> from ftwpki.baselibs.package import PKIPackage

>>> from ftwpki.baselibs.core import load_private_key_from_pem

>>> priv_key_obj =load_private_key_from_pem(privkey_path.read_bytes(), None)

>>> pack = PKIPackage()
>>> pack.load(pki_path)


>>> container.fullchain = pack.fullchain

>>> container.private_key = priv_key_obj

>>> container.caroot_cert = pack.caroot_cert

>>> tests_bytes = Path(toml_conf_file).read_bytes()


>>> container.load_pathes(tests_bytes)

>>> container.save("test")

.. SECTION - Teardown

>>> env.clean_home()
>>> env.teardown()


.. !SECTION - Teardown

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



.. !SECTION - Prepare


>>> from ftwpki.baselibs.configuration import BasePKIConfig
>>> from ftwpki.baselibs.protocols import ClientTypeName
>>> from ftwpki.remotepack.cli_parser import remote_pack_cli_parser
>>> import tomllib
>>> from io import StringIO, BytesIO
>>> from ftwpki.remotepack.container import PKIRemoteContainer
>>> from ftwpki.baselibs.core import load_private_key_from_pem

.. SECTION - Start programm


.. SECTION - Configuration

>>> config_type: ClientTypeName = "server"
>>> parser = remote_pack_cli_parser()
>>> args = parser.parse_args(sys_argv)

>>> args
RemotePackCliArguments(configname='M-V-HH-Members.toml'
format='PEM'
key_name='member-web')

>>> pki_name = Path(args.configname).stem
>>> pre_conf={"pki_name": pki_name}
>>> config: BasePKIConfig = BasePKIConfig(args.configname)

>>> config.set_config(config_type)

>>> config.current_configfile_entries #doctest: +NORMALIZE_WHITESPACE
{'private_keys': '#config#.private', 
 'zip': '#data#', 
 'certs': '#zip#', 
 'chains': '#zip#', 
 'config_path': '#config#', 
 'data_path': '#data#'}

>>> config.handle_pki_file()



.. !SECTION - Configuration



.. SECTION - Container Creation


>>> container = PKIRemoteContainer()

>>> priv_key_bytes = config.private_key(args.private_key)

>>> b"BEGIN PRIVATE" in priv_key_bytes
True

>>> priv_key_obj = load_private_key_from_pem(priv_key_bytes, None)

>>> container.private_key = priv_key_obj


>>> container.fullchain = config.fullchain


>>> container.caroot_cert = config.pki.caroot_cert

>>> pathfile = Path(Path(args.configname).stem).with_suffix(".id.toml").name


>>> container.load_pathes(config.pki.additional_files.get(pathfile))

>>> container._file_path #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
RemotePathes(
    fullchain: etc/chains/chainfull.chain, 
    rootca: etc/rootCa/caroot.cert, 
    private_key: etc/.private/my_key.key
)

>>> container._content #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
RemoteContent(
    fullchain: [<Certificate...],
    rootca: <Certificate...>,
    private_key: <cryptography.hazmat.bindings._rust.openssl.rsa.RSAPrivateKey...
)

.. !SECTION - Container Creation


.. SECTION - Save Container

>>> container.save("test")

.. !SECTION - Save Container



.. !SECTION - Stop programm



.. SECTION - Teardown

>> env.clean_home()
>>> env.teardown()


.. !SECTION - Teardown

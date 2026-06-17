Command Line Interface for Remotepack
======================================


>>> from ftwpki.remotepack.cli_parser import remote_pack_cli_parser, RemotePackCliArguments


>>> rpc_arg = RemotePackCliArguments()

>>> rpc_arg
RemotePackCliArguments(configname=''
format='PEM'
key_name='')

>>> remote_pack_cli_parser() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
PKIBaseParser(prog=..., 
    usage=None, 
    description=None, 
    formatter_class=<class 'argparse.HelpFormatter'>, 
    conflict_handler='error', 
    add_help=True)

>>> rpc_parser = remote_pack_cli_parser()

>>> rpc_parser.parse_args(["-k", "web_serv", "test-config"])
RemotePackCliArguments(configname='test-config'
format='PEM'
key_name='web_serv')

>>> rpc_parser.parse_args([])
Traceback (most recent call last):
    ...
argparse.ArgumentError: the following arguments are required: configname, -k/--key/--key-name

>>> rpc_preparser = remote_pack_cli_parser(add_help=False)

>>> rpc_preparser #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
PKIBaseParser(prog=..., 
    usage=None, 
    description=None, 
    formatter_class=<class 'argparse.HelpFormatter'>, 
    conflict_handler='error', 
    add_help=False)

>>> rpc_preparser.parse_args([])
RemotePackCliArguments(configname='None'
format='PEM'
key_name='')

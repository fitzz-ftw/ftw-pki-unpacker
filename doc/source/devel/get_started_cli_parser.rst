Command Line Interface for Unpacker
===================================



>>> from ftwpki.unpacker.cli_parser import get_parser

>>> get_parser() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
UnpackerCliParser(prog='...', 
    usage=None, 
    description=None, 
    formatter_class=<class 'argparse.HelpFormatter'>, 
    conflict_handler='error', 
    add_help=True)


>>> from ftwpki.unpacker.cli_parser import UnpackerCliParser

>>> cli_p = UnpackerCliParser(run_setup=False)

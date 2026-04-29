Command Line Interface for Receiver
===================================



>>> from ftwpki.receiver.cli_parser import get_parser

>>> get_parser() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
ReceiverCliParser(prog='...', 
    usage=None, 
    description=None, 
    formatter_class=<class 'argparse.HelpFormatter'>, 
    conflict_handler='error', 
    add_help=True)

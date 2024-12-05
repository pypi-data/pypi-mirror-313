#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
import time
#import ssh_agent_setup
import os

from stardiceonline.tools.config import config
from stardiceonline.archive.archive import local_archive
from stardiceonline.web import ServerStart
from stardiceonline.processing.processor import Process
from stardiceonline.simulation.fakeinstrument import FakeInstrumentServer

def connect(args):
    '''Establish the ssh tunnels required for live observations
    '''
    from stardiceonline.archive import ssh
    ssh.ssh_tunnel(config['webapp.webcamport'], config['ssh.telhost']) # webcam
    ssh.ssh_tunnel(config['webapp.serverport'], '127.0.0.1') # webcam
    return 'Connected'

def shift(args):
    connect(args)
    args.option = 'live'
    Process()(args)
    ServerStart()(args)

def main():
    import argparse, argcomplete
    parser = argparse.ArgumentParser(
        description='')
    subparsers = parser.add_subparsers(help='sub-command help')#, required=True)
    # create the parser for the "power" commands
    
    for parser_name, handler in [('config', config), ('archive', local_archive), ('connect', connect), ('webapp', ServerStart()), ('process', Process()), ('simulator', FakeInstrumentServer()),('shift', shift)]:
        subparser = subparsers.add_parser(parser_name, help=handler.__doc__)
        subparser.set_defaults(func=handler)
        if hasattr(handler, 'choices'):
            subparser.add_argument('option', choices=handler.choices())
            
        subparser.add_argument('value', nargs='?')
        
    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    if hasattr(args, 'func'):
        ret = args.func(args)
        if ret is not None:
            print(ret)
    else:
        print(parser.format_usage())

#!/usr/bin/env python

# Standard library modules
import ConfigParser
import argparse
import os
import textwrap


def create_config(configuration):
    """ Function used to create the configuration file
    if it does not exist in the program's path.

    It returns a ConfigParser object
    """
    configuration.add_section('Defaults')
    configuration.set('Defaults', 'path', 'C:\\XKCD')

    if not os.path.lexists('C:\\XKCD'):
        os.mkdir('C:\\XKCD')

    with open('xkcd.cfg', 'wb') as configfile:
        configuration.write(configfile)


def get_args():
    """ Function that parses the command line arguments and returns
    them in a argparse.Namespace object
    """
    config = ConfigParser.ConfigParser()

    if not os.path.lexists('xkcd.cfg'):
        create_config(config)
    else:
        config.read('xkcd.cfg')

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
            Examples on how to use the program
            ----------------------------------
            python xkcd.py --path C:\\Users\\admin\\Desktop\\xkcd --all
                **all xkcd comics will be saved in path described

            python xkcd.py -n 158
                **downloads comic number 158

            python xkcd.py --range 300 #
                **downloads all comics from comic number 300
                to the latest one. Inclusive of the latest one.

            python xkcd.py --latest
                **Downloads the latest comic.
            '''))

    parser.add_argument('-p', '--path', default=config.get('Defaults', 'path'),
                        help='The folder where the xkcd comics will be saved\
                        (default: %(default)s)')

    # Only one of the arguments can be present in the command line.
    group = parser.add_mutually_exclusive_group()

    group.add_argument('-l', '--latest', action='store_true', help='\
            Downloads the latest comic.')

    group.add_argument('-a', '--all', action='store_true', help='\
        Downloads all xkcd comics.')

    group.add_argument('-n', dest='comic_number', default=argparse.SUPPRESS,
                       type=int, help='The comic number to be downloaded.')

    group.add_argument('--range', dest='comic_range',
                       default=argparse.SUPPRESS, nargs=2,
                       help='Download the range of comics.\
                        e.g. --range 30 100 # represents the latest comic.')

    args = parser.parse_args()

    if args.path != config.get('Defaults', 'path'):

        if not os.path.lexists(args.path):
            os.mkdir(args.path)
            config.set('Defaults', 'path', args.path)
        else:
            config.set('Defaults', 'path', args.path)

        with open('xkcd.cfg', 'wb') as configfile:
            config.write(configfile)

    return vars(args)

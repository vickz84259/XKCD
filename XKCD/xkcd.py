#! python2
# [SublimeLinter @python:2]
# xkcd.py - Downloads comics from xkcd.com.

# Standard library modules
import os
import ConfigParser
import argparse
import logging
import textwrap

# Third-party modules
import requests
import bs4

# Project-specific modules

# Defining Constants
STATUS = ['Image not found', 'Error downloading', 'Success']
PATH = ''

CONFIG = ConfigParser.ConfigParser()

LOGGER = logging.getLogger(__name__)


def create_config():
    """ Function used to create the configuration file
    if it does not exist in the program's path.

    It returns a ConfigParser object
    """
    CONFIG.add_section('Defaults')
    CONFIG.set('Defaults', 'path', 'C:\\XKCD')

    if not os.path.lexists('C:\\XKCD'):
        os.mkdir('C:\\XKCD')

    with open('xkcd.cfg', 'wb') as configfile:
        CONFIG.write(configfile)

    return CONFIG


def get_args():
    """ Function that parses the command line arguments and returns
    them in a argparse.Namespace object
    """
    global PATH, CONFIG
    if not os.path.lexists('xkcd.cfg'):
        CONFIG = create_config()
    else:
        CONFIG.read('xkcd.cfg')

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
                **Downloads the latest comic if there are no previously\
                downloaded comics. Otherwise it downloads all the\
                comics since the last one that was downloaded
            '''))

    parser.add_argument('-p', '--path', default=CONFIG.get('Defaults', 'path'),
                        help='The folder where the xkcd comics will be saved\
                        (default: %(default)s)')

    # Only one of the arguments can be present in the command line.
    group = parser.add_mutually_exclusive_group()

    group.add_argument('-l', '--latest', action='store_true', help='\
            Downloads the latest comic if there are no previously\
            downloaded comics. Otherwise it downloads all the\
            comics since the last one that was downloaded.')

    group.add_argument('-a', '--all', action='store_true', help='\
        Downloads all xkcd comics.')

    group.add_argument('-n', dest='comic_number', default=argparse.SUPPRESS,
                       type=int, help='The comic number to be downloaded.')

    group.add_argument('--range', dest='comic_range',
                       default=argparse.SUPPRESS, nargs=2,
                       help='Download the range of comics.\
                        e.g. --range 30 100 # represents the latest comic.')

    args = parser.parse_args()

    if args.path != CONFIG.get('Defaults', 'path'):

        if not os.path.lexists(args.path):
            os.mkdir(args.path)
            CONFIG.set('Defaults', 'path', args.path)
        else:
            CONFIG.set('Defaults', 'path', args.path)

        with open('xkcd.cfg', 'wb') as configfile:
            CONFIG.write(configfile)

    PATH = args.path

    return vars(args)


def main():
    LOGGER.setLevel(logging.INFO)

    file_handler = logging.FileHandler('xkcd.log', 'ab')

    formatter = logging.Formatter('%(levelname)s:%(message)s')
    file_handler.setFormatter(formatter)

    LOGGER.addHandler(file_handler)

    args = get_args()
    keys = args.keys()

    comics = []
    initial = None
    final = None

    # Reading the log file to check the previously downloaded
    # comics
    with open('xkcd.log', 'rb') as fin:
        for line in fin.readlines():
            x = line.split(':')
            if x[0] != 'INFO':
                continue
            elif x[2] == STATUS[2]:
                comics.append(x[1])

    if comics != []:
        for i in comics:
            comic_one = i.split('--')[0]
            comic_two = i.split('--')[1]

            if initial is None or comic_one < initial:
                initial = int(comic_one)

            if final != '#' and final is None or comic_two == '#'\
                    or comic_two > final:
                final = comic_two

    try:
        if 'comic_number' in keys:
                download_comic(start=str(args['comic_number']),
                               end=str(int(args['comic_number']) + 1))

        elif 'comic_range' in keys and args['comic_range'][1] != '#':

                download_comic(start=args['comic_range'][0],
                               end=str(int(args['comic_range'][1]) + 1))

        elif 'comic_range' in keys and args['comic_range'][1] == '#':

                download_comic(start=args['comic_range'][0])

        elif args['all']:
                download_comic()

        else:
            if initial is None or final == '#':
                download_comic(start='')
            else:
                download_comic(start=initial, end=str(int(final) + 1))
    except Exception, e:
        LOGGER.exception('There was a problem: {}'.format(str(e)))
        print 'Error logged.'


def download_comic(start='1', end='#'):
    """ Function to download the comicson the xkcd website

    Start parameter specifies the first comic to download and
    end specifies where to stop. If end is a comic number, the
    specified comic will not be downloaded.
    """
    current_comic = start
    url = 'http://xkcd.com/{0}'.format(start)

    while not url.endswith(end):
        # Getting the webpage
        res = get_resource(url)

        soup = bs4.BeautifulSoup(res.text, "html.parser")

        if current_comic == '':
            current_comic = os.path.split(url)[1]

        image_element = soup.select('#comic img')
        if len(image_element) > 0:
            try:
                # Getting the url for the image.
                comic_url = 'http:{0}'.format(image_element[0].get('src'))

                # Download and save the image
                res = download_image(comic_url)

                # Get the nexk link
                url = get_next_url(current_comic)

            except requests.exceptions.MissingSchema:
                LOGGER.error('{0}:{1}'.format(current_comic, STATUS[1]))

                # skip this comic
                url = get_next_url(current_comic)
                continue
        else:
            LOGGER.error('{0}:{1}'.format(current_comic, STATUS[0]))

            # skip to the next link
            url = get_next_url(current_comic)
            continue
    if end != '#':
        end = str(int(end) - 1)
        LOGGER.info('{0}--{1}:{2}'.format(start, end, STATUS[2]))
    else:
        LOGGER.info('{0}--{1}:{2}'.format(start, end, STATUS[2]))


def get_next_url(comic, ascending=True):
    if ascending:
        comic = str(int(comic) + 1)
    else:
        comic = str(int(comic) - 1)

    return 'http://xkcd.com/{0}'.format(comic)


def download_image(url):
    """ This function downloads and saves the image specified
    by the given url.
    """

    print 'Downloading image {0}...'.format(os.path.basename(url))
    res = get_resource(url)

    with open(os.path.join(PATH, os.path.basename(url)), 'wb') as imageFile:
        for chunk in res.iter_content(100000):
            imageFile.write(chunk)


def get_resource(url):
    """ Function to download a web resource at the specified url.
    Example: website, image e.t.c

    It returns a requests object
    """
    res = requests.get(url)
    try:
        res.raise_for_status()
    except Exception, e:
        raise e

    return res

if __name__ == '__main__':
    main()

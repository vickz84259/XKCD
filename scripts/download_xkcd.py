#!/usr/bin/env python
# [SublimeLinter @python:2]
# download_xkcd.py - Downloads comics from xkcd.com.

__author__ = 'Victor Otieno Omondi'
__version__ = ''

# Standard library modules
import logging

# Project-specific modules
import argument
import xkcd


def main():
    # Initializing the logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler('xkcd.log', 'ab')

    formatter = logging.Formatter('%(levelname)s:%(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    # Getting the command line arguments
    # args is a dictionary
    args = argument.get_args()
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
            elif x[2] == 'success':
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

                download_comic(
                    args['path'],
                    start=str(args['comic_number']),
                    end=str(int(args['comic_number']) + 1))

        elif 'comic_range' in keys and args['comic_range'][1] != '#':

                download_comic(
                    args['path'],
                    start=args['comic_range'][0],
                    end=str(int(args['comic_range'][1]) + 1))

        elif 'comic_range' in keys and args['comic_range'][1] == '#':

                download_comic(args['path'], start=args['comic_range'][0])

        elif args['all']:
                download_comic(args['path'])

        else:

            if initial is None or final == '#':
                download_comic(args['path'], start='')
            else:
                download_comic(args['path'], start=initial,
                               end=str(int(final) + 1))
    except Exception, e:
        logger.exception('There was a problem: {}'.format(str(e)))
        print 'Error logged.'


def download_comic(path, start='1', end='#'):
    """ Function to download the comics on the xkcd website.

    Parameters:
        path: specifies where the comics will be downloaded.
        start: specifies the first comic to be downloaded.
        end: specifies where the program to stop. The comic number
            indicated with this parameter will not be downloaded.
    """
    log = logging.getLogger(__name__)
    current_comic = start
    url = 'http://xkcd.com/{0}'.format(start)

    while not url.endswith(end):

        # Getting the url for the image.
        comic_url = xkcd.get_image_url(url)

        # The function could not find any image url
        if comic_url is None:
            # Skips to the next comic
            url = get_next_url(current_comic)
            continue

        # Download and save the image
        xkcd.download_image(comic_url, path)

        # Get the nexk link
        url = get_next_url(current_comic)

    if end != '#':
        end = str(int(end) - 1)
        log.info('{0}--{1}:{2}'.format(start, end, 'success'))
    else:
        log.info('{0}--{1}:{2}'.format(start, end, 'success'))


def get_next_url(comic, ascending=True):
    if comic == '':
        return 'http//xkcd.com/#'

    if ascending:
        comic = str(int(comic) + 1)
    else:
        comic = str(int(comic) - 1)

    return 'http://xkcd.com/{0}'.format(comic)


if __name__ == '__main__':
    main()

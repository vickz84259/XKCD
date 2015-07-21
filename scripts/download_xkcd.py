#!/usr/bin/env python
# [SublimeLinter @python:2]
# download_xkcd.py - Downloads comics from xkcd.com.

__author__ = 'Victor Otieno Omondi'
__version__ = '2.2.4'

# Standard library modules
import logging
import Queue
import time

# Third-Party modules
import requests

# Project-specific modules
import argument
import workers

url_workers = 10
download_workers = 8

url_queue = Queue.Queue()
download_queue = Queue.Queue()


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

    try:
        if 'comic_number' in keys:

            download_comic(
                args['path'],
                start=int(args['comic_number']),
                end=int(args['comic_number']) + 1)

        elif 'comic_range' in keys and args['comic_range'][1] != '#':

            download_comic(
                args['path'],
                start=int(args['comic_range'][0]),
                end=int(args['comic_range'][1]) + 1)

        elif 'comic_range' in keys and args['comic_range'][1] == '#':

            download_comic(args['path'], start=int(args['comic_range'][0]))

        elif args['all']:

            download_comic(args['path'])

        elif args['latest']:

            download_comic(args['path'], start=0)

    except Exception, e:
        logger.exception('There was a problem: {}'.format(str(e)))
        print e
        print 'Error logged'


def download_comic(path, start=1, end=0):
    """ Function to download the comics on the xkcd website.

    Parameters:
        path: specifies where the comics will be downloaded.
        start: specifies the first comic to be downloaded.
        end: specifies where the program to stop. The comic number
            indicated with this parameter will not be downloaded.
    """
    log = logging.getLogger(__name__)

    for i in range(url_workers):
        t = workers.UrlWorker(url_queue, download_queue)
        t.setDaemon(True)
        t.start()

    if end == 0:
        req = requests.get('https://xkcd.com/info.0.json')
        end = req.json()['num'] + 1
    if start == 0:
        req = requests.get('https://xkcd.com/info.0.json')
        start = req.json()['num']
        end = start + 1

    for number in range(start, end):
        url_queue.put(
            (str(number), 'http://xkcd.com/{}/info.0.json'.format(number)))

    time.sleep(5)

    for i in range(download_workers):
        t = workers.DownloadWorker(path, download_queue)
        t.setDaemon(True)
        t.start()

    url_queue.join()
    download_queue.join()

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

#! python2
# [SublimeLinter @python:2]
# xkcd.py - Downloads comics from xkcd.com.

# Standard library modules
import os
import logging

# Third-party modules
import requests
import bs4

# Project-specific modules
import argument


def main():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler('xkcd.log', 'ab')

    formatter = logging.Formatter('%(levelname)s:%(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

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
    """ Function to download the comicson the xkcd website

    Start parameter specifies the first comic to download and
    end specifies where to stop. If end is a comic number, the
    specified comic will not be downloaded.
    """
    log = logging.getLogger(__name__)
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
                res = download_image(comic_url, path)

                # Get the nexk link
                url = get_next_url(current_comic)

            except requests.exceptions.MissingSchema:

                log.error('{0}:{1}'.format(
                    current_comic,
                    'error downloading'))

                # skip this comic
                url = get_next_url(current_comic)
                continue
        else:
            log.error('{0}:{1}'.format(
                current_comic,
                'image not found'))

            # skip to the next link
            url = get_next_url(current_comic)
            continue
    if end != '#':
        end = str(int(end) - 1)
        log.info('{0}--{1}:{2}'.format(start, end, 'success'))
    else:
        log.info('{0}--{1}:{2}'.format(start, end, 'success'))


def get_next_url(comic, ascending=True):
    if ascending:
        comic = str(int(comic) + 1)
    else:
        comic = str(int(comic) - 1)

    return 'http://xkcd.com/{0}'.format(comic)


def download_image(url, path):
    """ This function downloads and saves the image specified
    by the given url.
    """

    print 'Downloading image {0}...'.format(os.path.basename(url))
    res = get_resource(url)

    with open(os.path.join(path, os.path.basename(url)), 'wb') as imageFile:
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

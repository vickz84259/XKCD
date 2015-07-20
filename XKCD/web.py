#! python2
# [SublimeLinter @python:2]

__author__ = 'Victor Otieno Omondi'

import logging
import os
import requests

log = logging.getLogger(__name__).addHandler(logging.NullHandler())


def get_image_url(webpage):
    """ Function to parse a webpage and get an image's url.

    The webpage url should point to it's json format.

    If the above is true it returns the image's url. Otherwise it returns none.
    """

    # Getting the webpage
    res = get_resource(webpage)

    webpage = res.json()

    try:
        return webpage['img']
    except Exception:
        log.exception('{0}:{1}'.format(webpage, 'image not found'))

        return None


def download_image(url, path, number):
    """ This function downloads and saves the image specified
    by the given url.

    The image is saved in the specified path.
    """

    print 'Downloading image {0}...'.format(os.path.basename(url))
    res = get_resource(url)

    with open(os.path.join(path, number, os.path.basename(url)), 'wb') \
            as imageFile:
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

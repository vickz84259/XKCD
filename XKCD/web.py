#! python2
# [SublimeLinter @python:2]
import logging
import os
import requests
import bs4

log = logging.getLogger(__name__).addHandler(logging.NullHandler())


def get_image_url(webpage):
    # Getting the webpage
    res = get_resource(webpage)

    soup = bs4.BeautifulSoup(res.text, "html.parser")
    image_element = soup.select('#comic img')

    if image_element > 0:
        return 'http:{0}'.format(image_element[0].get('src'))
    else:
        log.error('{0}:{1}'.format(webpage, 'image not found'))

        return None


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

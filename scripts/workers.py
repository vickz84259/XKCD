#! python2
# [SublimeLinter @python:2]

__author__ = 'Victor Otieno Omondi'

import threading
import xkcd


class UrlWorker(threading.Thread):
    """UrlWorker objects get a webpage's url from a queue
    and parse the webpage for a specified image's url.

    The image's url is placed in another queue for processing by
    other workers.
    """
    def __init__(self, web_queue, image_queue):
        """Initializing a UrlWorker objects

        web_queue represents the queue containing urls to webpages.

        image_queue represents the queue where the UrlWorker object
            will store the image url received.
        """
        super(UrlWorker, self).__init__()
        self.web_queue = web_queue
        self.image_queue = image_queue

    def run(self):
        while True:
            # fetch webpage url from queue
            url = self.web_queue.get()

            # fetch image url from webpage
            image_url = xkcd.get_image_url(url)

            if image_url is not None:
                # place url in download queue
                self.image_queue.put(image_url)

            self.web_queue.task_done()


class DownloadWorker(threading.Thread):
    """DownloadWorker objects get an image's url from a queue
    and download the image and save it in a specified path
    """
    def __init__(self, path, image_queue):
        """ Initializing DownloadWorker object.

        path represents where the images will be downloaded

        image_queue is the queue where the object will retrieve the
        urls for the images.
        """
        super(DownloadWorker, self).__init__()
        self.image_queue = image_queue
        self.path = path

    def run(self):
        while True:
            # fetch image url from queue
            url = self.image_queue.get()

            # download the image
            xkcd.download_image(url, self.path)

            self.image_queue.task_done()

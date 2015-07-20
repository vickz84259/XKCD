#! python2
# [SublimeLinter @python:2]

import threading
import xkcd


class UrlWorker(threading.Thread):
    """docstring for UrlWorker"""
    def __init__(self, queue, out_queue):
        super(UrlWorker, self).__init__()
        self.queue = queue
        self.out_queue = out_queue

    def run(self):
        while True:
            # fetch webpage url from queue
            url = self.queue.get()

            # fetch image url from webpage
            image_url = xkcd.get_image_url(url)

            if image_url is not None:
                # place url in download queue
                self.out_queue.put(image_url)

            self.queue.task_done()


class DownloadWorker(threading.Thread):
    """docstring for DownloadWorker"""
    def __init__(self, path, out_queue):
        super(DownloadWorker, self).__init__()
        self.out_queue = out_queue
        self.path = path

    def run(self):
        while True:
            # fetch image url from queue
            url = self.out_queue.get()

            # download the image
            xkcd.download_image(url, self.path)

            self.queue.task_done()

import threading
import time
import logging
import random
from multiprocessing import Queue
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)


def file_input(filename):
    return [x for x in open(filename).read().split('\n') if x]

def file_output(filename):
    return open(filename, 'w')

def is_absolute(url):
    return bool(urllib.parse.urlparse(url).netloc)

def make_absolute_url(url, link):
    if link.startswith('//'):
        link = link.replace('//', 'http://')
    elif link.startswith('/'):
        return urllib.parse.urljoin(url, link)

    return link

class FetchUrl(threading.Thread):
    def __init__(self, name, url, q):
        threading.Thread.__init__(self)
        self.url = url
        self.name = name
        self.q = q

    def run(self):
        while not self.q.full():
            try:
                source = urllib.request.urlopen(self.url).read()
                self.q.put({'url': self.url, 'source': source})
                logging.debug('Inserting ' + str(self.url)
                              + ' : ' + str(self.q.qsize()) + ' responses in queue')
                return
            except Exception as e:
                logging.debug('Error ' + str(self.url) + ': ' + str(e))
                return


class ProducerThread(threading.Thread):
    def __init__(self, name, urls, q):
        super(ProducerThread, self).__init__()
        self.name = name
        self.urls = urls
        self.q = q

    def run(self):
        for url in self.urls:
            FetchUrl('Fetch', url, self.q).start()

        #Join all existing threads to main thread.
        for thread in threading.enumerate():
            if thread is not threading.currentThread() and thread is not self.consumer:
                thread.join()

        return


class ConsumerThread(threading.Thread):
    def __init__(self, name, producer, q, out):
        super(ConsumerThread,self).__init__()
        self.producer = producer
        self.name = name
        self.q = q
        self.out = out

    def run(self):

        while self.producer.isAlive() or not self.q.empty():
            item = self.q.get()

            url = item['url']
            source = item['source']
            try:
                soup = BeautifulSoup(source, 'lxml')
                logging.debug('Processing: ' + url)
                for a in soup.find_all('a', href=True):
                    hyperlink = a['href']
                    if not is_absolute(hyperlink):
                        hyperlink = make_absolute_url(url, hyperlink)

                    self.out.write(hyperlink+'\n')
            except:
                logging.debug('Error: ' + url)

        return

def scrap(filename_in='url_list.txt', filename_out='urls_output.txt'):
    BUF_SIZE = 7
    q = Queue(BUF_SIZE)


    urls = file_input(filename_in)
    output = file_output(filename_out)
    p = ProducerThread('producer', urls, q)
    c = ConsumerThread('consumer', p, q, output)
    p.consumer = c

    p.start()
    c.start()

if __name__ == '__main__':
    scrap()

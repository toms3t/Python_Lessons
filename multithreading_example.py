#! python3
# downloadXkcd.py - Downloads every single XKCD comic.
# Original script from 'Automate the Boring Stuff' by Al Sweigart
# Modified to show time differences between single threaded operation
# and multi-threaded operation


import requests
import os
import bs4
import threading
import time


os.makedirs('xkcdmt', exist_ok=True) # store comics in ./xkcd
start_time = time.time()


def download_xkcd(start_comic, end_comic):
    for url_num in range(start_comic, end_comic):
        # Download the page.
        print('Downloading page http://xkcd.com/%s...' % (url_num))
        res = requests.get('http://xkcd.com/%s' % (url_num))
        res.raise_for_status()

        soup = bs4.BeautifulSoup(res.text)

        # Find the URL of the comic image.
        comicElem = soup.select('#comic img')
        if comicElem == []:
            print('Could not find comic image.')
        else:
            comicUrl = comicElem[0].get('src')
            # Download the image.
            print('Downloading image %s...' % (comicUrl))
            res = requests.get('http:'+comicUrl)
            res.raise_for_status()

            # Save the image to ./xkcd
            imageFile = open(
                os.path.join('xkcdmt', os.path.basename(comicUrl)), 'wb')
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()


def single_or_multithreaded(single=False):
    if single:
        download_xkcd(1, 51)
    else:
        download_threads = [] # a list of all the Thread objects
        for i in range(1, 50, 10): # loops 10 times, creates 10 threads
            download_thread = threading.Thread(
                target=download_xkcd, args=(i, i + 10)
            )
            download_threads.append(download_thread)
            download_thread.start()

        # Wait for all threads to end.
        for download_thread in download_threads:
            download_thread.join()

    print('Done.')
    seconds = time.time() - start_time
    print('\n')

    
    file_count = os.popen('ls xkcdmt | wc -l').read().strip()
    print('{} comics were downloaded in {} seconds'.format(
        str(file_count), seconds)
    )


if __name__ == '__main__':
    single_or_multithreaded()



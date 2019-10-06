# a small script to handle downloading data from urls
import urllib
from urllib.request import urlretrieve
from urllib.parse import urlparse
import os, sys
import zipfile
from math import ceil
import time


BYTES_PER_MB = 1024 * 1024


def error_handle():
    """Print out error line and filename
    (from stack overflow)
    """
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)


def retri_file_size(url: str):
    """Return to-be-downloaded file size
    """
    meta = urllib.request.urlopen(url).info()
    return int(meta['Content-Length'])


def retri_fn_url(url: str) -> str:
    """return filename from an url
    Parameters
    ----------
    url : str
        link url
    Returns
    -------
    str
        url file name
    """
    addr = urlparse(url).path
    return os.path.basename(addr)

def time_format(secs: int):
    """Transform nb of secs to time format
    """
    s = '{}s'.format(secs % 60).zfill(3)
    if secs < 60:
        return s.rjust(6);
    secs = secs // 60
    m = '{}\''.format(secs % 60).zfill(3)
    if secs < 60:
        return (m + s).rjust(6)
    secs = secs // 60
    h = '{}h'.format(secs % 24).zfill(3)
    if secs < 24:
        return (h + m).rjust(6)
    if secs > 2 * 24:
        return 'uknown'
    d = '{}d'.format(secs // 24)
    return (d + h).rjust(6)


def down_fr_url(urls: list, save_dir: str='', unzip: bool=False):
    for url in urls:
        try:
            fn = retri_fn_url(url)
            save_path = os.path.join(save_dir, fn)
            
            print('Downloading {} ...'.format(fn))
            urlretrieve(url, save_path)
            print('\n')
            if unzip:
                print('Extracting file ...')
                zip = zipfile.ZipFile(save_path)
                zip.extractall('.')
                zip.close()

        except Exception as e:
            error_handle()
            print(e)
    print('Done.')


if __name__ == '__main__':
    test = 'funny'
    print(retri_fn_url(test))
    urls = ['https://www.dropbox.com/s/h4pypk9s2mxzzme/checkpoint-3.pth.tar?dl=1']
    down_fr_url(urls, unzip=False)

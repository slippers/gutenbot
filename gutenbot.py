import os
import requests
import argparse
import io
from urllib.parse import urlparse
from os.path import splitext
from random import randint
from gutenberg.cleanup import strip_headers
from gutenberg.query import (
    get_etexts,
    get_metadata,
    list_supported_metadatas
)
from gutenberg.acquire import set_metadata_cache, load_etext
from gutenberg.acquire.metadata import SqliteMetadataCache


def get_ext(url):
    """Return the filename extension from url, or ''."""
    parsed = urlparse(url)
    root, ext = splitext(parsed.path)
    return ext[1:]  # or ext[1:] if you don't want the leading '.'


def get_uri(book, ext):
    for uri in get_metadata('formaturi', book):
        print(uri)
        if get_ext(uri) == ext:
            return uri


def get_author(book):
    return ''.join(get_metadata('author', book))


def get_title(book):
    return ''.join(get_metadata('title', book))


def acquire_corpora():
    while True:
        book = randint(100, 10000)
        if get_metadata('title', book):
            # uri = get_uri(book, 'images')
            uri = 'http://www.gutenberg.org/ebooks/{}'.format(book)
            return [book, get_title(book), uri, get_author(book)]


def post_corpora(url, auth_token):
    corpora = acquire_corpora()
    text = strip_headers(load_etext(corpora[0])).strip()

    print(corpora, text[:100])

    authentication_token = {'authentication-token': auth_token}

    # data to post
    files = {'file': io.StringIO(text)}
    data = {
        'label': '{} {}'.format(corpora[1], corpora[3]),
        'source': corpora[2]
    }

    # post
    ru = requests.post(url + '/v1/corpora',
                       headers=authentication_token,
                       files=files,
                       data=data)
    print(ru.json())


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='post corpora to flask-prose')
    parser.add_argument('url')
    parser.add_argument('auth_token')
    args = parser.parse_args()

    sqlite_cache = './gutenbot.sqlite'
    cache = SqliteMetadataCache(sqlite_cache)

    if not os.path.exists(sqlite_cache):
        cache.populate()
    set_metadata_cache(cache)

    post_corpora(args.url, args.auth_token)

'''
    # print(list_supported_metadatas())
    # prints (u'author', u'formaturi', u'language', ...)
    # text = strip_headers(load_etext(2701)).strip()
    # print(text)  # prints 'MOBY DICK; OR THE WHALE\n\nBy Herman Melville ...'
'''

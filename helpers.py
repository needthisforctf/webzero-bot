import os
import argparse
from urllib.parse import urlparse, urlunparse, ParseResult
from validators import domain

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--token')
parser.add_argument('-u', '--urlsfile')

def get_arg(argname: str):
    args = parser.parse_args()
    return getattr(args, argname) or os.getenv(argname.upper())

def link_normalizer(link: str) -> str:
    try:
        if not link.startswith('http'):
            link = "http://" + link
        return link
    except TypeError as e:
        print('Type error', e)
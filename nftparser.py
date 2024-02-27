import asyncio
import aiohttp
from lxml import etree
import json
import helpers
from pathlib import Path
import re
from fake_useragent import UserAgent

banned_lst = {'ethereumjs', 'ethers', 'web3.min.js'}
banned_regex = re.compile('|'.join(map(re.escape, banned_lst)))
ua = UserAgent(min_percentage=1.3)

class Urls:
    def __init__(self, filepath=None, urllist=None):
        if filepath:
            self._filepath = Path(filepath)
        elif helpers.get_arg('urlsfile'):
            self._filepath = Path(helpers.get_arg('urlsfile'))
        else:
            raise ValueError('No urls file specified')
        self._file_is_blank, self._loaded_from_file = None, None
        if type(urllist) == list:
            self._lst = urllist
            self._loaded_from_file = True
            self.dump() # backing up supplied list just in case
        else:
            if not self._loaded_from_file:
                self._lst = []
    
    def load(self) -> bool:
        try:
            with open(self._filepath, 'r') as file:
                self._lst = json.load(file)
                self._loaded_from_file = True
                return True
        except FileNotFoundError as e:
            self._file_is_blank = True
            open(self._filepath, 'a').close() # we're creating a blank file by opening and closing it immediately
        except PermissionError as e:
            print('Check permissions for urls file, cannot read it')

    def dump(self) -> bool:
        try:
            with open(self._filepath, 'w') as file:
                json.dump(self._lst, file)
                return True
        except AttributeError as e:
            print('Wtf the urls list does not exist')
            return False
        except FileNotFoundError as e:
            print('The file does not exist. Have you deleted it during runtime?')
            return False
        except PermissionError as e:
            print('Check permissions for urls file, cannot write to it')

    def get(self) -> list:
        return self._lst.copy() # lists are mutable
    
    def add(self, item: str) -> bool:
        try:
            self._lst.append(helpers.link_normalizer(item))
            return True
        except ValueError as e:
            print(e)

urls = Urls()

async def fetch_and_parse(url: str):
    async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=10), 
            headers={"UserAgent":ua.google}
        ) as session:
        try:
            async with session.get(url) as response:
                html_content = await response.text() # get html
                html_tree = etree.HTML(html_content) # parse it
                if (head := html_tree.find("head")) is not None:
                    return head
        except aiohttp.client_exceptions.ClientConnectorError as e:
            print(e)

def check_for_eth(head_tag):
    links = (
            link.attrib.get('src') 
            for link in head_tag.iterfind('./script[@src]')
            )

    for link in links:
        if banned_regex.search(link):
            return True
            break
    else:
        return False

async def fetch2check(url):
    if url in urls.get():
        return True
    else:
        if check_for_eth(await fetch_and_parse(url)):
            urls.add(url)
            return True
    return False
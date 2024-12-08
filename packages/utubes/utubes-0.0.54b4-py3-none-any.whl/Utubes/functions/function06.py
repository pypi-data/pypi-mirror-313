import requests
from bs4 import BeautifulSoup
from .collections import SMessage
#======================================================================

class Dlinks:

    async def get01(filelink):
        try:
            uris = str(filelink)
            cors = requests.get(uris).content
            page = BeautifulSoup(cors, 'lxml')
            info = page.find('a', {'aria-label': 'Download file'})
            oung = info.get('href')
            return SMessage(filelink=oung)
        except Exception as errors:
            return SMessage(filelink=filelink, errors=errors)

#======================================================================

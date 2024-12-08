import asyncio
from spotdl import Spotdl
from .collections import THREAD
from .collections import SMessage
from spotdl.types.song import Song
from ..scripts import Creds, Spotifyconfig
from spotdl.download.downloader import Downloader
from spotdl.utils.formatter import create_file_name
#=====================================================================================================

class Spotify:

    async def clinton(client=Creds.DATA01, secret=Creds.DATA02, config=Spotifyconfig):
        try:
            return Spotdl(client_id=client, client_secret=secret, downloader_settings=config)
        except Exception:
            return None

#=====================================================================================================

    async def config():
        return Spotifyconfig

#=====================================================================================================

    async def downloadER(configs):
        loomed = asyncio.get_event_loop()
        moonus = Downloader(loop=loomed, settings=configs)
        return moonus

#=====================================================================================================

    async def download(mains, sid):
        somuid = sid[0]
        moonus = await asyncio.to_thread(mains.search_and_download, somuid)
        return moonus

#=====================================================================================================

import os, asyncio
from ..scripts import Okeys
from ..scripts import Flite
from ..scripts import Scripted
from .exceptions import Cancelled
from .collections import THREAD, SMessage
from yt_dlp import YoutubeDL, DownloadError
#===============================================================================================

class DownloadER:

    async def download(link, command, progress=None):
        with YoutubeDL(command) as ydl:
            try:
                filelink = [link]
                loop = asyncio.get_event_loop()
                ydl.add_progress_hook(progress) if progress else progress
                await loop.run_in_executor(THREAD, ydl.download, filelink)
                return SMessage(status=True, code=200)
            except DownloadError as errors:
                return SMessage(status=False, code=400, errors=errors)
            except Cancelled as errors:
                return SMessage(status=False, code=300, errors=errors)
            except Exception as errors:
                return SMessage(status=False, code=400, errors=errors)

#===============================================================================================
    
    async def metadata(link, command):
        with YoutubeDL(command) as ydl:
            try:
                loop = asyncio.get_event_loop()
                #moonus = ydl.extract_info(link, download=False)
                moonus = await loop.run_in_executor(THREAD, ydl.extract_info, link, False)
                return SMessage(result=moonus)
            except Exception as errors:
                return SMessage(errors=errors)

#===============================================================================================

    async def extracts(link, command):
        with YoutubeDL(command) as ydl:
            try:
                loop = asyncio.get_event_loop()
                #moonus = ydl.extract_info(link, download=False)
                moonus = await loop.run_in_executor(THREAD, ydl.extract_info, link, False)
                return SMessage(result=moonus)
            except Exception as errors:
                return SMessage(errors=errors)

#===============================================================================================

    async def filename(link, command, names=Okeys.DATA01):
        with YoutubeDL(command) as ydl:
            try:
                loop = asyncio.get_event_loop()
                meawes = ydl.extract_info(link, download=False)
                meawes = await loop.run_in_executor(THREAD, ydl.extract_info, link, False)
                moonus = ydl.prepare_filename(meawes, outtmpl=names)
                return SMessage(result=moonus, captions=moonus)
            except Exception as errors:
                return SMessage(result=Scripted.DATA09, errors=errors)

#===============================================================================================

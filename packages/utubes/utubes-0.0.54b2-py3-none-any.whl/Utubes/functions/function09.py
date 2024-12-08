import os
from .collections import SMessage
#=================================================================================================

class Finders:

    async def get01(flocation, exo):
        try:
            location = str(flocation)
            filesize = int(os.path.getsize(location))
            return SMessage(location=location, filesize=filesize)
        except Exception:
            pass
        try:
            location = os.path.splitext(flocation)[0]
            filesize = int(os.path.getsize(location))
            return SMessage(location=location, filesize=filesize)
        except Exception:
            pass
        try:
            location = os.path.splitext(flocation)[0] + str(exo)
            filesize = int(os.path.getsize(location))
            return SMessage(location=location, filesize=filesize)
        except Exception as errors:
            return SMessage(location=None, filesize=0, errors=errors)

#=================================================================================================

    async def get02(dlocation, exo, exe):
        try:
            location = str(dlocation)
            filesize = int(os.path.getsize(location))
            return SMessage(location=location, filesize=filesize)
        except Exception:
            pass
        try:
            location = os.path.splitext(dlocation)[0]
            filesize = os.path.getsize(location)
            return SMessage(location=location, filesize=int(filesize))
        except Exception:
            pass
        try:
            location = os.path.splitext(dlocation)[0] + str(exe)
            filesize = os.path.getsize(location)
            return SMessage(location=location, filesize=int(filesize))
        except Exception:
            pass
        try:
            location = os.path.splitext(dlocation)[0] + str(exo)
            filesize = os.path.getsize(location)
            return SMessage(location=location, filesize=int(filesize))
        except Exception:
            pass
        try:
            location = os.path.splitext(dlocation)[0] + "." + str(exe)
            filesize = os.path.getsize(location)
            return SMessage(location=location, filesize=int(filesize))
        except Exception as errors:
            return SMessage(location=None, filesize=int(0), errors=errors)

#=================================================================================================

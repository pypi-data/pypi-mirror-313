from ..scripts import Ulinks
from .function06 import Dlinks
#=====================================================================

async def Glink(finelink):
    if finelink.startswith(Ulinks.DATA01):
        moonus = await Dlinks.get01(finelink)
        return moonus.filelink
    else:
        return finelink

#=====================================================================

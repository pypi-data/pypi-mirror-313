from ..scripts import Plinks
from .function06 import Dlinks
#=====================================================================

async def Glink(finelink):
    if finelink.startswith(Plinks.DATA01):
        moonus = await Dlinks.get01(finelink)
        return moonus.filelink
    else:
        return finelink

#=====================================================================

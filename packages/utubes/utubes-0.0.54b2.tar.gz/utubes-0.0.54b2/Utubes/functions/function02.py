import os
from ..scripts import Smbo
from ..scripts import Flite
from ..scripts import Scripted
from .collections import SMessage
from pyrogram.enums import MessageEntityType
#=====================================================================================================================

class Extractors:

    async def extract00(update, incoming):
        amoend = filter(lambda o: o.type == MessageEntityType.URL, update.entities)
        amoond = list(amoend)
        neomos = amoond[0].offset
        sosmso = amoond[0].length
        linked = incoming[ neomos : neomos + sosmso ]
        return linked

    async def extract07(filename):
        namesz = os.path.splitext(filename)[0] if filename else None
        exeson = os.path.splitext(filename)[1] if filename else None
        return SMessage(filename=namesz, extenson=exeson)

    async def extract08(filename):
        namews = os.path.splitext(filename)[0] if filename else Scripted.DATA08
        exeson = os.path.splitext(filename)[1] if filename else Scripted.DATA12
        return SMessage(filename=namews, extenson=exeson)

    async def extract03(texted, length=None, clean=Flite.DATA01):
        texted = Scripted.DATA01.join(clean.get(chao, chao) for chao in texted)
        return texted[:length] if length else texted

    async def extract04(anames, exeson):
        onames = await Extractors.extract07(anames)
        exeoxo = exeson if exeson else Scripted.DATA06
        return Scripted.DATA07.format(onames.filename, exeoxo)

    async def extract05(cnames, exeson):
        answer = await Extractors.extract07(cnames)
        exeoxo = exeson if exeson else Scripted.DATA06
        exesxs = answer.extenson.replace(".", "") if answer.extenson else exeoxo
        return Scripted.DATA10.format(answer.filename, exesxs)

#=====================================================================================================================
    
    async def extract01(update, incoming):
        poxwers = incoming.split(Smbo.DATA04)
        if len(poxwers) == 2 and Smbo.DATA04 in incoming:
             Username = None
             Password = None
             Flielink = poxwers[0] # INCOMING URL
             Filename = poxwers[1] # INCOMING FILENAME
        elif len(poxwers) == 3 and Smbo.DATA04 in incoming:
             Filename = None
             Flielink = poxwers[0] # INCOMING URL
             Username = poxwers[1] # INCOMING USERNAME
             Password = poxwers[2] # INCOMING PASSWORD
        elif len(poxwers) == 4 and Smbo.DATA04 in incoming:
             Flielink = poxwers[0] # INCOMING URL
             Filename = poxwers[1] # INCOMING FILENAME
             Username = poxwers[2] # INCOMING USERNAME
             Password = poxwers[3] # INCOMING PASSWORD
        else:
             Filename = None # INCOMING FILENAME
             Username = None # INCOMING USERNAME
             Password = None # INCOMING PASSWORD
             Flielink = await Extractors.extract00(update, incoming)

        moon01 = Flielink.strip() if Flielink != None else None
        moon02 = Filename.strip() if Filename != None else None
        moon03 = Username.strip() if Username != None else None
        moon04 = Password.strip() if Password != None else None
        return SMessage(filelink=moon01, filename=moon02, username=moon03, password=moon04)

#=====================================================================================================================

    async def extract02(update, filename, incoming):
        poxwers = incoming.split(Smbo.DATA04)
        if len(poxwers) == 2 and Smbo.DATA04 in incoming:
             Username = None
             Password = None
             Flielink = poxwers[0] # INCOMING URL
             Filename = poxwers[1] # INCOMING FILENAME
        elif len(poxwers) == 3 and Smbo.DATA04 in incoming:
             Filename = None
             Flielink = poxwers[0] # INCOMING URL
             Username = poxwers[1] # INCOMING USERNAME
             Password = poxwers[2] # INCOMING PASSWORD
        elif len(poxwers) == 4 and Smbo.DATA04 in incoming:
             Flielink = poxwers[0] # INCOMING URL
             Filename = poxwers[1] # INCOMING FILENAME
             Username = poxwers[2] # INCOMING USERNAME
             Password = poxwers[3] # INCOMING PASSWORD
        else:
             Filename = None # INCOMING FILENAME
             Username = None # INCOMING USERNAME
             Password = None # INCOMING PASSWORD
             Flielink = await Extractors.extract00(update, incoming)

        moon01 = Flielink.strip() if Flielink != None else None
        moon03 = Username.strip() if Username != None else None
        moon04 = Password.strip() if Password != None else None
        moon02 = Filename.strip() if Filename != None else filename
        return SMessage(filelink=moon01, filename=moon02, username=moon03, password=moon04)

#=====================================================================================================================

    async def extract06(anames, cnames, exeson):
        return await Extractors.extract05(cnames, exeson) if cnames else await Extractors.extract04(anames, exeson)

#=====================================================================================================================

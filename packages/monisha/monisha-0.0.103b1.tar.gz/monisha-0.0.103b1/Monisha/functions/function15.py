import os
import time
import shutil
from ..scripts import Folders
from ..scripts import Scripted
#================================================================================

class Location:

    async def mak00(name=Folders.DATA07):
        shutil.rmtree(name) if os.path.isdir(name) else name
        os.makedirs(name)

#================================================================================
    
    async def mak01(name=Folders.DATA07):
        direos = str(name)
        osemse = os.getcwd()
        moonse = os.path.join(osemse, direos, Scripted.DATA01)
        moonse if os.path.exists(moonse) else os.makedirs(moonse)
        return moonse

#================================================================================

    async def mak02(name=Folders.DATA07):
        direos = str(name)
        osemse = os.getcwd()
        timeso = str(round(time.time()))
        moonse = os.path.join(osemse, direos, timeso, Scripted.DATA01)
        moonse if os.path.exists(moonse) else os.makedirs(moonse)
        return moonse

#================================================================================

    async def mak03(uid, name=Folders.DATA07):
        usered = str(uid)
        direos = str(name)
        osemse = os.getcwd()
        timeso = str(round(time.time()))
        moonse = os.path.join(osemse, direos, usered, timeso, Scripted.DATA01)
        moonse if os.path.exists(moonse) else os.makedirs(moonse)
        return moonse

#================================================================================

import socket
import requests
from ..scripts import Apis
#====================================================================

class Internet:

    def GetIP():
        moones = requests.get(Apis.DATA02)
        moonus = moones.json()
        return moonus['ip']

#====================================================================

    def GetLIP():
        moones = socket.gethostname()
        moonus = socket.gethostbyname(moones)
        return moonus

#====================================================================

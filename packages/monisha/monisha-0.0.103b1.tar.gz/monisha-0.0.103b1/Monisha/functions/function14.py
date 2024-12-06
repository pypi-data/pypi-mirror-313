from pathlib import Path
from .function04 import Eimes
from .collections import SMessage
#======================================================================

class Locations:

    async def get01(directory, stored=None):
        sos = stored if stored else []
        for item in Path(directory).rglob('*'):
            if not item.is_dir():
                sos.append(str(item))

        sos.sort()
        return SMessage(allfiles=sos, numfiles=len(sos))

#======================================================================

    async def get02(directory, stored=None, skip=Eimes.DATA00):
        sos = stored if stored else []
        for patho in directory:
            if not patho.upper().endswith(skip):
                sos.append(patho)

        sos.sort()
        return SMessage(allfiles=sos, numfiles=len(sos))

#======================================================================

    async def get03(directory, stored=None, filter=Eimes.DATA05):
        sos = stored if stored else []
        for patho in directory:
            if patho.upper().endswith(filter):
                sos.append(patho)

        sos.sort()
        return SMessage(allfiles=sos, numfiles=len(sos))

#======================================================================

    async def rem01(file):
        file_path = Path(file)
        file_path.unlink() if file_path.exists() else None

#======================================================================    
    
    async def rem02(files):
        for file in files:
            file_path = Path(file)
            file_path.unlink() if file_path.exists() else None
    
#======================================================================

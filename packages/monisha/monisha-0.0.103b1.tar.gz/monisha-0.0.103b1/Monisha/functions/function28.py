import os
from pathlib import Path
from .collections import SMessage
#====================================================================

class Filesize:

    def get01(flocation):
        try:
            moonus = os.path.getsize(flocation)
            return SMessage(filesize=moonus)
        except FileNotFoundError as errors:
            return SMessage(errors=errors)
        except PermissionError as errors:
            return SMessage(errors=errors)
        except Exception as errors:
            return SMessage(errors=errors)

#====================================================================

    def get02(flocation):
        try:
            moones = Path(flocation)
            moonus = moones.stat().st_size
            return SMessage(filesize=moonus)
        except FileNotFoundError as errors:
            return SMessage(errors=errors)
        except PermissionError as errors:
            return SMessage(errors=errors)
        except Exception as errors:
            return SMessage(errors=errors)

#====================================================================

    async def get11(flocation):
        try:
            moonus = os.path.getsize(flocation)
            return SMessage(filesize=moonus)
        except FileNotFoundError as errors:
            return SMessage(errors=errors)
        except PermissionError as errors:
            return SMessage(errors=errors)
        except Exception as errors:
            return SMessage(errors=errors)

#====================================================================

    async def get12(flocation):
        try:
            moones = Path(flocation)
            moonus = moones.stat().st_size
            return SMessage(filesize=moonus)
        except FileNotFoundError as errors:
            return SMessage(errors=errors)
        except PermissionError as errors:
            return SMessage(errors=errors)
        except Exception as errors:
            return SMessage(errors=errors)

#====================================================================

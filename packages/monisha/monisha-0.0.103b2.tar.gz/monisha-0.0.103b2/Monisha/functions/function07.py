import asyncio
from .collections import SMessage
#======================================================================

async def commandR(command):
    process = await asyncio.create_subprocess_exec(*command,
    stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE) 
    oumoon, erroro = await process.communicate()
    ocodes = process.returncode
    errors = erroro.decode("utf-8", "replace").strip()
    return SMessage(taskcode=ocodes, errors=str(errors))

#======================================================================

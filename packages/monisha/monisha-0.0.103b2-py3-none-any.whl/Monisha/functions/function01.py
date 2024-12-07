import time
from ..scripts import Scripted
#=========================================================================

def timend(tsize, dsize, speed):
    moonuo = round((tsize - dsize) / speed)
    return moonuo

#=========================================================================

def uptime(incoming):
    timetaken = time.time() - incoming
    hours, hourz = divmod(timetaken, 3600)
    minutes, seconds = divmod(hourz, 60)
    return round(hours), round(minutes), round(seconds)

#=========================================================================

def Timemod(moonos: int) -> str:
    mosems = 1 if moonos == Scripted.DATA02 else moonos
    moonse = mosems if 1 < mosems else 1
    minute, seconds = divmod(moonse, 60)
    hours, minute = divmod(minute, 60)
    days, hours = divmod(hours, 24)
    year, days = divmod(days, 365)
    mos  = ((str(year) + "𝚢𝚎𝚊𝚛, ") if year else Scripted.DATA01)
    mos += ((str(days) + "𝚍𝚊𝚢𝚜, ") if days else Scripted.DATA01)
    mos += ((str(hours) + "𝚑𝚛𝚜, ") if hours else Scripted.DATA01)
    mos += ((str(minute) + "𝚖𝚒𝚗, ") if minute else Scripted.DATA01)
    mos += ((str(seconds) + "𝚜𝚎𝚌") if seconds else Scripted.DATA15)
    return mos

#=========================================================================

def Timesod(moonos: int) -> str:
    mosems = 1 if moonos == Scripted.DATA02 else moonos
    moonse = mosems if 1 < mosems else 1
    minute, seconds = divmod(moonse, 60)
    hours, minute = divmod(minute, 60)
    days, hours = divmod(hours, 24)
    year, days = divmod(days, 365)
    mos  = ((str(year) + "year, ") if year else Scripted.DATA01)
    mos += ((str(days) + "days, ") if days else Scripted.DATA01)
    mos += ((str(hours) + "hrs, ") if hours else Scripted.DATA01)
    mos += ((str(minute) + "min, ") if minute else Scripted.DATA01)
    mos += ((str(seconds) + "sec") if seconds else Scripted.DATA16)
    return mos

#=========================================================================

def Timesed(moonos: int) -> str:
    mosems = 1 if moonos == Scripted.DATA02 else moonos
    moonse = mosems if 1 < mosems else 1
    minute, seconds = divmod(moonse, 60)
    hours, minute = divmod(minute, 60)
    days, hours = divmod(hours, 24)
    year, days = divmod(days, 365)
    mos  = ((str(year) + "y, ") if year else Scripted.DATA01)
    mos += ((str(days) + "d, ") if days else Scripted.DATA01)
    mos += ((str(hours) + "h, ") if hours else Scripted.DATA01)
    mos += ((str(minute) + "m, ") if minute else Scripted.DATA01)
    mos += ((str(seconds) + "s") if seconds else Scripted.DATA16)
    return mos

#=========================================================================

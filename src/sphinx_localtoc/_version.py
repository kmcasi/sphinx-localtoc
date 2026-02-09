#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 09 Feb 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|

#// GLOBAL VARIABLES
YEAR: int = 26
MONTH: int = 2
DAY: int = 9
REVISION: int = 2
RELEASE: bool = True

__version__ = "{year}.{month}.{day}{state}".format(
    year=YEAR, month=MONTH, day=DAY,
    state=f".dev{max(1, REVISION)}" if not RELEASE else f".{REVISION}" if REVISION else ""
)

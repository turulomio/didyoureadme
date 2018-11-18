
from didyoureadme.version import __version__, __versiondate__
from didyoureadme.didyoureadme import main



import platform
if platform.system()=="Windows":
    from didyoureadme.shortcuts import *

from __future__ import annotations
from os import getenv

local = getenv('LOCALAPPDATA')
roaming = getenv('APPDATA')
__version__ = "0.0.1"

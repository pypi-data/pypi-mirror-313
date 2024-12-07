
__title__ = 'chzzk'
__author__ = 'westreed'
__license__ = 'MIT'
__copyright__ = 'Copyright 2024-present westreed'
__version__ = '0.1.1'

from typing import NamedTuple, Literal
from .chzzk import Chzzk
from .chzzk_chat import ChzzkChat


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal['alpha', 'beta', 'final']
    serial: int


version_info: VersionInfo = VersionInfo(major=0, minor=1, micro=1, releaselevel='alpha', serial=0)

del NamedTuple, Literal, VersionInfo

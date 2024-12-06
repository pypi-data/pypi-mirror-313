"""
辅助测试的一些常用功能
"""

from ._date import DateLib
from ._net import NetLib
from ._path import DirLib, PathLib
from ._person import Person
from ._rand import Random

__all__: list[str] = [
    "DateLib",
    "PathLib",
    "DirLib",
    "Random",
    "NetLib",
    "Person",
]


import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import moa.options
import moa.recommender.rc.data
import typing



class RecommenderData:
    def getData(self) -> moa.recommender.rc.data.RecommenderData: ...

class MemRecommenderData(moa.options.AbstractOptionHandler, RecommenderData):
    def __init__(self): ...
    def getData(self) -> moa.recommender.rc.data.RecommenderData: ...
    def getDescription(self, stringBuilder: java.lang.StringBuilder, int: int) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("moa.recommender.data")``.

    MemRecommenderData: typing.Type[MemRecommenderData]
    RecommenderData: typing.Type[RecommenderData]

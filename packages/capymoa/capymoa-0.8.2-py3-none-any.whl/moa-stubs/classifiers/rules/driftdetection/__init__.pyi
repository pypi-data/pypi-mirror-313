
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import typing



class PageHinkleyTest(java.io.Serializable):
    def __init__(self, double: float, double2: float): ...
    def getCumulativeSum(self) -> float: ...
    def getMinimumValue(self) -> float: ...
    def reset(self) -> None: ...
    def update(self, double: float) -> bool: ...

class PageHinkleyFading(PageHinkleyTest):
    def __init__(self, double: float, double2: float): ...
    def reset(self) -> None: ...
    def update(self, double: float) -> bool: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("moa.classifiers.rules.driftdetection")``.

    PageHinkleyFading: typing.Type[PageHinkleyFading]
    PageHinkleyTest: typing.Type[PageHinkleyTest]

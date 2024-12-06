
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import moa.classifiers.core.driftdetection
import typing



class NoChangeDetection(moa.classifiers.core.driftdetection.AbstractChangeDetector, moa.classifiers.core.driftdetection.ChangeDetector):
    def __init__(self): ...
    def getDescription(self, stringBuilder: java.lang.StringBuilder, int: int) -> None: ...
    def getPurposeString(self) -> str: ...
    def input(self, double: float) -> None: ...
    def resetLearning(self) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("moa.classifiers.rules.core.changedetection")``.

    NoChangeDetection: typing.Type[NoChangeDetection]


import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import moa.options
import typing



class ProbabilityFunction(moa.options.OptionHandler):
    def getProbability(self, double: float, double2: float, double3: float) -> float: ...

class CantellisInequality(moa.options.AbstractOptionHandler, ProbabilityFunction):
    def __init__(self): ...
    def getDescription(self, stringBuilder: java.lang.StringBuilder, int: int) -> None: ...
    def getProbability(self, double: float, double2: float, double3: float) -> float: ...

class ChebyshevInequality(moa.options.AbstractOptionHandler, ProbabilityFunction):
    def __init__(self): ...
    def getDescription(self, stringBuilder: java.lang.StringBuilder, int: int) -> None: ...
    def getProbability(self, double: float, double2: float, double3: float) -> float: ...

class GaussInequality(moa.options.AbstractOptionHandler, ProbabilityFunction):
    def __init__(self): ...
    def getDescription(self, stringBuilder: java.lang.StringBuilder, int: int) -> None: ...
    def getProbability(self, double: float, double2: float, double3: float) -> float: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("moa.classifiers.rules.core.anomalydetection.probabilityfunctions")``.

    CantellisInequality: typing.Type[CantellisInequality]
    ChebyshevInequality: typing.Type[ChebyshevInequality]
    GaussInequality: typing.Type[GaussInequality]
    ProbabilityFunction: typing.Type[ProbabilityFunction]

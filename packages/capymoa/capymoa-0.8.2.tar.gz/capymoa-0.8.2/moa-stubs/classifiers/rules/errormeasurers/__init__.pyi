
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import com.github.javacliparser
import com.yahoo.labs.samoa.instances
import java.lang
import jpype
import moa
import typing



class ErrorMeasurement(moa.AbstractMOAObject):
    fadingErrorFactorOption: com.github.javacliparser.FloatOption = ...
    def __init__(self): ...
    def addPrediction(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], instance: com.yahoo.labs.samoa.instances.Instance) -> None: ...
    def getCurrentError(self) -> float: ...
    def getDescription(self, stringBuilder: java.lang.StringBuilder, int: int) -> None: ...

class MeanAbsoluteDeviation(ErrorMeasurement):
    def __init__(self): ...
    def addPrediction(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], instance: com.yahoo.labs.samoa.instances.Instance) -> None: ...
    def getCurrentError(self) -> float: ...

class RootMeanSquaredError(ErrorMeasurement):
    def __init__(self): ...
    def addPrediction(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], instance: com.yahoo.labs.samoa.instances.Instance) -> None: ...
    def getCurrentError(self) -> float: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("moa.classifiers.rules.errormeasurers")``.

    ErrorMeasurement: typing.Type[ErrorMeasurement]
    MeanAbsoluteDeviation: typing.Type[MeanAbsoluteDeviation]
    RootMeanSquaredError: typing.Type[RootMeanSquaredError]

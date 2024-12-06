
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import jpype
import moa
import moa.classifiers.core.attributeclassobservers
import moa.classifiers.core.conditionaltests
import moa.classifiers.core.driftdetection
import moa.classifiers.core.splitcriteria
import moa.classifiers.core.statisticaltests
import typing



class AttributeSplitSuggestion(moa.AbstractMOAObject, java.lang.Comparable['AttributeSplitSuggestion']):
    splitTest: moa.classifiers.core.conditionaltests.InstanceConditionalTest = ...
    resultingClassDistributions: typing.MutableSequence[typing.MutableSequence[float]] = ...
    merit: float = ...
    def __init__(self, instanceConditionalTest: moa.classifiers.core.conditionaltests.InstanceConditionalTest, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], double2: float): ...
    def compareTo(self, attributeSplitSuggestion: 'AttributeSplitSuggestion') -> int: ...
    def getDescription(self, stringBuilder: java.lang.StringBuilder, int: int) -> None: ...
    def numSplits(self) -> int: ...
    def resultingClassDistributionFromSplit(self, int: int) -> typing.MutableSequence[float]: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("moa.classifiers.core")``.

    AttributeSplitSuggestion: typing.Type[AttributeSplitSuggestion]
    attributeclassobservers: moa.classifiers.core.attributeclassobservers.__module_protocol__
    conditionaltests: moa.classifiers.core.conditionaltests.__module_protocol__
    driftdetection: moa.classifiers.core.driftdetection.__module_protocol__
    splitcriteria: moa.classifiers.core.splitcriteria.__module_protocol__
    statisticaltests: moa.classifiers.core.statisticaltests.__module_protocol__

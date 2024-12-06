
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jpype
import moa.core
import typing



class FeatureRankingMessage: ...

class ChangeDetectedMessage(FeatureRankingMessage):
    def __init__(self): ...

class MeritCheckMessage(FeatureRankingMessage):
    @typing.overload
    def __init__(self, doubleVector: moa.core.DoubleVector): ...
    @typing.overload
    def __init__(self, doubleVector: moa.core.DoubleVector, booleanArray: typing.Union[typing.List[bool], jpype.JArray]): ...
    def getLearningAttributes(self) -> typing.MutableSequence[bool]: ...
    def getMerits(self) -> moa.core.DoubleVector: ...

class RuleExpandedMessage(FeatureRankingMessage):
    @typing.overload
    def __init__(self, int: int): ...
    @typing.overload
    def __init__(self, int: int, boolean: bool): ...
    def getAttributeIndex(self) -> int: ...
    def isSpecialization(self) -> bool: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("moa.classifiers.rules.featureranking.messages")``.

    ChangeDetectedMessage: typing.Type[ChangeDetectedMessage]
    FeatureRankingMessage: typing.Type[FeatureRankingMessage]
    MeritCheckMessage: typing.Type[MeritCheckMessage]
    RuleExpandedMessage: typing.Type[RuleExpandedMessage]

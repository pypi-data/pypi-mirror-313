
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import com.yahoo.labs.samoa.instances
import java.lang
import moa.classifiers
import moa.core
import typing



class MultiTargetNoChange(moa.classifiers.AbstractMultiLabelLearner, moa.classifiers.MultiTargetRegressor):
    def __init__(self): ...
    def getModelDescription(self, stringBuilder: java.lang.StringBuilder, int: int) -> None: ...
    @typing.overload
    def getPredictionForInstance(self, instance: com.yahoo.labs.samoa.instances.Instance) -> com.yahoo.labs.samoa.instances.Prediction: ...
    @typing.overload
    def getPredictionForInstance(self, example: moa.core.Example[com.yahoo.labs.samoa.instances.Instance]) -> com.yahoo.labs.samoa.instances.Prediction: ...
    @typing.overload
    def getPredictionForInstance(self, multiLabelInstance: com.yahoo.labs.samoa.instances.MultiLabelInstance) -> com.yahoo.labs.samoa.instances.Prediction: ...
    def getPurposeString(self) -> str: ...
    def isRandomizable(self) -> bool: ...
    def resetLearningImpl(self) -> None: ...
    @typing.overload
    def trainOnInstanceImpl(self, instance: com.yahoo.labs.samoa.instances.Instance) -> None: ...
    @typing.overload
    def trainOnInstanceImpl(self, multiLabelInstance: com.yahoo.labs.samoa.instances.MultiLabelInstance) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("moa.classifiers.multitarget.functions")``.

    MultiTargetNoChange: typing.Type[MultiTargetNoChange]

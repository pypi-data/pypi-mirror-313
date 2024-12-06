
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import com.github.javacliparser
import java.lang
import jpype
import moa.classifiers.rules.multilabel.core
import moa.options
import typing



class InputAttributesSelector(moa.options.OptionHandler):
    def getNextInputIndices(self, attributeExpansionSuggestionArray: typing.Union[typing.List[moa.classifiers.rules.multilabel.core.AttributeExpansionSuggestion], jpype.JArray]) -> typing.MutableSequence[int]: ...

class MeritThreshold(moa.options.AbstractOptionHandler, InputAttributesSelector):
    percentageThresholdOption: com.github.javacliparser.FloatOption = ...
    def __init__(self): ...
    def getDescription(self, stringBuilder: java.lang.StringBuilder, int: int) -> None: ...
    def getNextInputIndices(self, attributeExpansionSuggestionArray: typing.Union[typing.List[moa.classifiers.rules.multilabel.core.AttributeExpansionSuggestion], jpype.JArray]) -> typing.MutableSequence[int]: ...

class SelectAllInputs(moa.options.AbstractOptionHandler, InputAttributesSelector):
    def __init__(self): ...
    def getDescription(self, stringBuilder: java.lang.StringBuilder, int: int) -> None: ...
    def getNextInputIndices(self, attributeExpansionSuggestionArray: typing.Union[typing.List[moa.classifiers.rules.multilabel.core.AttributeExpansionSuggestion], jpype.JArray]) -> typing.MutableSequence[int]: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("moa.classifiers.rules.multilabel.inputselectors")``.

    InputAttributesSelector: typing.Type[InputAttributesSelector]
    MeritThreshold: typing.Type[MeritThreshold]
    SelectAllInputs: typing.Type[SelectAllInputs]

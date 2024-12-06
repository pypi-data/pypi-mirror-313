
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import com.yahoo.labs.samoa.instances
import java.lang
import java.util
import moa
import typing



class Converter(moa.AbstractMOAObject):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, int: int): ...
    def createTemplate(self, instances: com.yahoo.labs.samoa.instances.Instances) -> com.yahoo.labs.samoa.instances.Instances: ...
    def formatInstance(self, instance: com.yahoo.labs.samoa.instances.Instance) -> com.yahoo.labs.samoa.instances.Instance: ...
    def getDescription(self, stringBuilder: java.lang.StringBuilder, int: int) -> None: ...
    def getL(self) -> int: ...
    def getRelevantLabels(self, instance: com.yahoo.labs.samoa.instances.Instance) -> java.util.List[int]: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("moa.core.utils")``.

    Converter: typing.Type[Converter]

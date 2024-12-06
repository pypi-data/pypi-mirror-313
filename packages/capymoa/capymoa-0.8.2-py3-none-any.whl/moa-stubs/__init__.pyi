
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.lang
import jpype
import moa.capabilities
import moa.classifiers
import moa.cluster
import moa.clusterers
import moa.core
import moa.evaluation
import moa.gui
import moa.learners
import moa.options
import moa.recommender
import moa.streams
import moa.tasks
import typing



class DoTask:
    progressAnimSequence: typing.ClassVar[typing.MutableSequence[str]] = ...
    MAX_STATUS_STRING_LENGTH: typing.ClassVar[int] = ...
    def __init__(self): ...
    @staticmethod
    def isJavaVersionOK() -> bool: ...
    @staticmethod
    def isWekaVersionOK() -> bool: ...
    @staticmethod
    def main(stringArray: typing.Union[typing.List[str], jpype.JArray]) -> None: ...

class MOAObject(java.io.Serializable):
    def copy(self) -> 'MOAObject': ...
    def getDescription(self, stringBuilder: java.lang.StringBuilder, int: int) -> None: ...
    def measureByteSize(self) -> int: ...

class MakeObject:
    def __init__(self): ...
    @staticmethod
    def main(stringArray: typing.Union[typing.List[str], jpype.JArray]) -> None: ...

class AbstractMOAObject(MOAObject):
    def __init__(self): ...
    @typing.overload
    def copy(self) -> MOAObject: ...
    @typing.overload
    @staticmethod
    def copy(mOAObject: MOAObject) -> MOAObject: ...
    @typing.overload
    def measureByteSize(self) -> int: ...
    @typing.overload
    @staticmethod
    def measureByteSize(mOAObject: MOAObject) -> int: ...
    def toString(self) -> str: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("moa")``.

    AbstractMOAObject: typing.Type[AbstractMOAObject]
    DoTask: typing.Type[DoTask]
    MOAObject: typing.Type[MOAObject]
    MakeObject: typing.Type[MakeObject]
    capabilities: moa.capabilities.__module_protocol__
    classifiers: moa.classifiers.__module_protocol__
    cluster: moa.cluster.__module_protocol__
    clusterers: moa.clusterers.__module_protocol__
    core: moa.core.__module_protocol__
    evaluation: moa.evaluation.__module_protocol__
    gui: moa.gui.__module_protocol__
    learners: moa.learners.__module_protocol__
    options: moa.options.__module_protocol__
    recommender: moa.recommender.__module_protocol__
    streams: moa.streams.__module_protocol__
    tasks: moa.tasks.__module_protocol__

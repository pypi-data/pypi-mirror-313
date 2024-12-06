
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import com.github.javacliparser
import moa.classifiers.core.attributeclassobservers
import typing



class FIMTDDNumericAttributeClassLimitObserver(moa.classifiers.core.attributeclassobservers.FIMTDDNumericAttributeClassObserver):
    maxNodesOption: com.github.javacliparser.IntOption = ...
    def __init__(self): ...
    @typing.overload
    def observeAttributeClass(self, double: float, int: int, double2: float) -> None: ...
    @typing.overload
    def observeAttributeClass(self, double: float, double2: float, double3: float) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("moa.classifiers.rules.core.attributeclassobservers")``.

    FIMTDDNumericAttributeClassLimitObserver: typing.Type[FIMTDDNumericAttributeClassLimitObserver]


import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import com.github.javacliparser
import java.lang
import moa.options
import typing



class BudgetManager:
    def getLastLabelAcqReport(self) -> int: ...
    def isAbove(self, double: float) -> bool: ...
    def resetLearning(self) -> None: ...

class FixedBM(moa.options.AbstractOptionHandler, BudgetManager):
    budgetOption: com.github.javacliparser.FloatOption = ...
    def __init__(self): ...
    def getDescription(self, stringBuilder: java.lang.StringBuilder, int: int) -> None: ...
    def getLastLabelAcqReport(self) -> int: ...
    def getPurposeString(self) -> str: ...
    def isAbove(self, double: float) -> bool: ...
    def resetLearning(self) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("moa.classifiers.active.budget")``.

    BudgetManager: typing.Type[BudgetManager]
    FixedBM: typing.Type[FixedBM]

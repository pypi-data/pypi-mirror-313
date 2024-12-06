
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.awt
import typing



class ColorGenerator:
    def generateColors(self, int: int) -> typing.MutableSequence[java.awt.Color]: ...

class HSVColorGenerator(ColorGenerator):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, float: float, float2: float, float3: float, float4: float): ...
    @typing.overload
    def __init__(self, float: float, float2: float, float3: float, float4: float, float5: float, float6: float): ...
    def generateColors(self, int: int) -> typing.MutableSequence[java.awt.Color]: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("moa.gui.colorGenerator")``.

    ColorGenerator: typing.Type[ColorGenerator]
    HSVColorGenerator: typing.Type[HSVColorGenerator]

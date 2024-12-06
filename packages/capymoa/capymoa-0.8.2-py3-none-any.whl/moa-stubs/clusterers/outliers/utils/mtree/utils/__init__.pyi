
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import java.util
import typing



_Pair__T = typing.TypeVar('_Pair__T')  # <T>
class Pair(typing.Generic[_Pair__T]):
    first: typing.Any = ...
    second: typing.Any = ...
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, t: _Pair__T, t2: _Pair__T): ...
    def get(self, int: int) -> _Pair__T: ...

class Utils:
    _minMax__T = typing.TypeVar('_minMax__T', bound=java.lang.Comparable)  # <T>
    @staticmethod
    def minMax(iterable: typing.Union[java.lang.Iterable[_minMax__T], typing.Sequence[_minMax__T], typing.Set[_minMax__T], typing.Callable[[], java.util.Iterator[typing.Any]]]) -> Pair[_minMax__T]: ...
    _randomSample__T = typing.TypeVar('_randomSample__T')  # <T>
    @staticmethod
    def randomSample(collection: typing.Union[java.util.Collection[_randomSample__T], typing.Sequence[_randomSample__T], typing.Set[_randomSample__T]], int: int) -> java.util.List[_randomSample__T]: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("moa.clusterers.outliers.utils.mtree.utils")``.

    Pair: typing.Type[Pair]
    Utils: typing.Type[Utils]

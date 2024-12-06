
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import moa.recommender.dataset.impl
import typing



class Dataset:
    def curItemID(self) -> int: ...
    def curRating(self) -> float: ...
    def curUserID(self) -> int: ...
    def next(self) -> bool: ...
    def reset(self) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("moa.recommender.dataset")``.

    Dataset: typing.Type[Dataset]
    impl: moa.recommender.dataset.impl.__module_protocol__


import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import moa.clusterers.outliers.utils.mtree
import typing


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("moa.clusterers.outliers.utils")``.

    mtree: moa.clusterers.outliers.utils.mtree.__module_protocol__

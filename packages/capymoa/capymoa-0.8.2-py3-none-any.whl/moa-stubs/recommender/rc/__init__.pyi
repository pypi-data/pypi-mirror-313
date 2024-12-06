
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import moa.recommender.rc.data
import moa.recommender.rc.predictor
import moa.recommender.rc.utils
import typing


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("moa.recommender.rc")``.

    data: moa.recommender.rc.data.__module_protocol__
    predictor: moa.recommender.rc.predictor.__module_protocol__
    utils: moa.recommender.rc.utils.__module_protocol__

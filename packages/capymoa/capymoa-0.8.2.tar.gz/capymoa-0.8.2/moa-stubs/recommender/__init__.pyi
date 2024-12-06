
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import moa.recommender.data
import moa.recommender.dataset
import moa.recommender.predictor
import moa.recommender.rc
import typing


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("moa.recommender")``.

    data: moa.recommender.data.__module_protocol__
    dataset: moa.recommender.dataset.__module_protocol__
    predictor: moa.recommender.predictor.__module_protocol__
    rc: moa.recommender.rc.__module_protocol__

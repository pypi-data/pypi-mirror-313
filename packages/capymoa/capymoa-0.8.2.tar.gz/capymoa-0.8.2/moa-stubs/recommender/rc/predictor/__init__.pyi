
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.util
import moa.recommender.rc.data
import moa.recommender.rc.predictor.impl
import typing



class RatingPredictor(java.io.Serializable):
    def getData(self) -> moa.recommender.rc.data.RecommenderData: ...
    def predictRating(self, int: int, int2: int) -> float: ...
    def predictRatings(self, int: int, list: java.util.List[int]) -> java.util.List[float]: ...
    def train(self) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("moa.recommender.rc.predictor")``.

    RatingPredictor: typing.Type[RatingPredictor]
    impl: moa.recommender.rc.predictor.impl.__module_protocol__

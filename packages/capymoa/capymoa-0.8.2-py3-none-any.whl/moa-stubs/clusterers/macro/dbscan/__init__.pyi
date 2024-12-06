
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import moa.cluster
import moa.clusterers.macro
import typing



class DBScan(moa.clusterers.macro.AbstractMacroClusterer):
    def __init__(self, clustering: moa.cluster.Clustering, double: float, int: int): ...
    def getClustering(self, clustering: moa.cluster.Clustering) -> moa.cluster.Clustering: ...

class DenseMicroCluster:
    def __init__(self, cFCluster: moa.cluster.CFCluster): ...
    def getCFCluster(self) -> moa.cluster.CFCluster: ...
    def isClustered(self) -> bool: ...
    def isVisited(self) -> bool: ...
    def setClustered(self) -> None: ...
    def setVisited(self) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("moa.clusterers.macro.dbscan")``.

    DBScan: typing.Type[DBScan]
    DenseMicroCluster: typing.Type[DenseMicroCluster]

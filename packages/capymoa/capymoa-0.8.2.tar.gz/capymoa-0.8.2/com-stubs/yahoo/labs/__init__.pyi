
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import com.yahoo.labs.samoa
import typing


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("com.yahoo.labs")``.

    samoa: com.yahoo.labs.samoa.__module_protocol__

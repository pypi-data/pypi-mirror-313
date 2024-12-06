
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import com.github
import com.yahoo
import typing


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("com")``.

    github: com.github.__module_protocol__
    yahoo: com.yahoo.__module_protocol__

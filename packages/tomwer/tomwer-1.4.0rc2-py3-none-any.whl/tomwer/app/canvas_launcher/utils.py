from __future__ import annotations

import tomoscan.version

import ewokscore
import ewoksorange
import tomwer.version
import sluurp

try:
    import nxtomomill.version
except ImportError:
    has_nxtomomill = False
else:
    has_nxtomomill = True
try:
    import nabu
except ImportError:
    has_nabu = False
else:
    has_nabu = True
try:
    import nxtomo.version
except ImportError:
    has_nxtomo = False
else:
    has_nxtomo = True


def get_tomotools_stack_versions() -> dict[str, str]:
    """Return the version of the main libraries used by tomwer"""
    stack = {
        "tomwer": tomwer.version.version,
    }

    if has_nabu:
        stack["nabu"] = nabu.version
    if has_nxtomo:
        stack["nxtomo"] = nxtomo.version.version
    if has_nxtomomill:
        stack["nxtomomill"] = nxtomomill.version.version
    stack["tomoscan"] = tomoscan.version.version
    stack["ewokscore"] = ewokscore.__version__
    stack["ewoksorange"] = ewoksorange.__version__
    stack["sluurp"] = sluurp.__version__

    return stack

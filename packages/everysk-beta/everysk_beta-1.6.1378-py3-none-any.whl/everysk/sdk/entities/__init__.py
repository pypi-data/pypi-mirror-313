###############################################################################
#
# (C) Copyright 2024 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################

###############################################################################
#   Imports
###############################################################################
from typing import TYPE_CHECKING
from everysk.core.string import import_from_string

if TYPE_CHECKING:
    from everysk.sdk.entities.query import Query

###############################################################################
#   __init__ Implementation
###############################################################################
def __getattr__(_name: str):
    from everysk.config import settings
    modules = settings.EVERYSK_SDK_ENTITIES_MODULES_PATH

    if _name in modules:
        return import_from_string(modules[_name])

    raise AttributeError(f"cannot import name '{_name}' from everysk.sdk")

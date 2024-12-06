#===============================================================================
# PSCAD Remotable objects
#===============================================================================

"""
PSCAD Remote Proxies
"""


#===============================================================================
# Imports
#===============================================================================

from __future__ import annotations

from typing import TYPE_CHECKING

# Allow modules to import rmi, rmi_property, deprecated and requires from here.
# pylint: disable=unused-import
from mhi.common.remote import Remotable as _Remotable
from mhi.common.remote import rmi, rmi_property, deprecated, requires
# pylint: enable=unused-import

if TYPE_CHECKING:
    from .pscad import PSCAD


#===============================================================================
# PSCAD Remotable
#===============================================================================

class Remotable(_Remotable):            # pylint: disable=too-few-public-methods
    """
    The Remote Proxy
    """

    # Treat all derived classes as being in the mhi.pscad module
    _MODULE = "mhi.pscad"

    @property
    def _pscad(self) -> PSCAD:
        return self._context._main


    @property
    def main(self) -> PSCAD:
        return self._context._main

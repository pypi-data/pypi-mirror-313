#===============================================================================
# PSCAD User Component Definition
#===============================================================================

"""
==========
Definition
==========
"""

#===============================================================================
# Imports
#===============================================================================

from __future__ import annotations

import logging
from typing import Dict, Iterable, Optional, Sequence, Union, TYPE_CHECKING
from xml.etree import ElementTree as ET

from mhi.common.cache import cached_property

from .remote import Remotable, rmi, rmi_property, requires
from .form import FormCodec
from .types import View

if TYPE_CHECKING:
    from .canvas import Canvas
    from .graphics import GfxCanvas


#===============================================================================
# Logging
#===============================================================================

LOG = logging.getLogger(__name__)


#===============================================================================
# PSCAD ZComponent
#===============================================================================

class Definition(Remotable):
    """
    Component Definition
    """

    #===========================================================================
    # Properties
    #===========================================================================

    #---------------------------------------------------------------------------
    # Identity
    #---------------------------------------------------------------------------

    @property
    def project_name(self) -> str:
        """
        The project which defines this definition (read-only)
        """
        return self._identity['project']


    @property
    def scope(self) -> str:
        """
        The project which defines this definition (read-only)
        """
        return self.project_name


    @property
    def name(self) -> str:
        """
        Name of the definition (read-only)
        """
        return self._identity['name']


    @property
    def scoped_name(self) -> str:
        """
        The scoped definition name is the project and definition names,
        separated by a colon (read-only)
        """

        return f"{self.project_name}:{self.name}"


    #---------------------------------------------------------------------------
    # Instances
    #---------------------------------------------------------------------------

    @rmi_property
    def _instances(self):
        pass


    @property
    @requires("5.0.2")
    def instances(self) -> int:
        """
        Number of live instances of this definition (read-only)

        .. versionadded:: 2.8
        """

        return self._instances


    #---------------------------------------------------------------------------
    # XML
    #---------------------------------------------------------------------------

    @rmi_property
    def _xml(self) -> str:
        pass

    @property
    def xml(self):
        """
        XML for the Definition (read-only)
        """

        return ET.fromstring(self._xml)


    #---------------------------------------------------------------------------
    # Repr
    #---------------------------------------------------------------------------

    def __repr__(self):
        return f"Definition[{self.scoped_name}]"


    #===========================================================================
    # Methods
    #===========================================================================

    #---------------------------------------------------------------------------
    # Form
    #---------------------------------------------------------------------------

    @rmi(fallback=True)
    def _form_xml(self):

        return self.xml.find('form')


    @cached_property
    def form_codec(self) -> FormCodec:
        """
        The definition's parameter form codec
        """

        xml = self._form_xml()
        codec = FormCodec(xml) if xml is not None else FormCodec()

        return codec


    #---------------------------------------------------------------------------
    # Definition Has a canvas?
    #---------------------------------------------------------------------------

    @rmi
    def is_module(self) -> bool:
        """
        Check to see if this component has its own canvas, with in turn,
        can contain additional components.

        Returns:
            bool: True if the component has an internal canvas, False otherwise.
        """


    #---------------------------------------------------------------------------
    # Parameters
    #---------------------------------------------------------------------------

    @rmi
    def _parameters(self, **kwargs):
        pass

    @requires("5.0.2")
    def parameters(self, *,
                   name=None, desc=None, url=None, group=None,
                   tags=None) -> Optional[Dict[str, str]]:
        """
        Set or get the definition's parameters.

        Parameters:
            name (str): The definition name.  Must be unique, alphanumeric,
                        and a maximum of 30 characters
            desc (str): A short description for the definition
            url (str): Location if loaded from an external resource
            group (str): One or more labels to describe group categorization
                         (Comma separated)
            tags (str): One or more tags to help find this definition
                        (Comma separated)

        Returns:
            A dictionary of parameter values (if no parameters are being set),
            or None.
        """

        kwargs = {"name": name, "desc": desc, "group": group, "tags": tags, "url": url}
        kwargs = {key: val for key, val in kwargs.items() if val is not None}
        return self._parameters(**kwargs)


    #---------------------------------------------------------------------------
    # Definition Compile
    #---------------------------------------------------------------------------

    @rmi
    def _compile(self):
        pass

    def compile(self) -> None:
        """
        Compile this component definition page
        """

        if not self.is_module():
            raise ValueError("Cannot compile; not a module")

        return self._compile()


    #---------------------------------------------------------------------------
    # Navigate Into
    #---------------------------------------------------------------------------

    @rmi
    def navigate_to(self) -> Canvas:
        """
        Attempt to navigate to the first instance if possible

        Returns:
            Canvas: The definition's canvas
        """

    @rmi
    def _set_view(self, view):
        pass

    def set_view(self, view: Union[str, View]) -> None:
        """
        Activate the appropriate definition editor tab

        Valid view tabs are one of the strings: "Schematic", "Graphic",
        "Parameters", "Script", "Fortran", "Data", or the equivalent
        :class:`.View` constant.

        Parameters:
            view: The desired view tab
        """

        if isinstance(view, str):
            view_id = View[view.upper()].value
        elif isinstance(view, View):
            view_id = view.value
        else:
            raise TypeError("Expected View or View string")

        self._set_view(view_id)


    #---------------------------------------------------------------------------
    # Definition Canvas
    #---------------------------------------------------------------------------

    def canvas(self) -> Canvas:
        """
        Definition canvas
        """

        prj = self._pscad.project(self.project_name)
        return prj.canvas(self.name)


    @cached_property
    def _graphic_canvas(self):

        return self._rmi_getprop('_graphics')


    def graphics(self) -> GfxCanvas:
        """
        Get the :class:`graphics canvas <.GfxCanvas>`

        .. versionadded:: 2.2
        """

        self.set_view(View.GRAPHIC)

        return self._graphic_canvas


    #---------------------------------------------------------------------------
    # Copy the definition to the clipboard
    #---------------------------------------------------------------------------

    def copy(self) -> None:
        """
        Copy the definition to the clipboard.
        """

        raise NotImplementedError()


    #===========================================================================
    # Scripts, Parameters, ...
    #===========================================================================

    #---------------------------------------------------------------------------
    # Scripts
    #---------------------------------------------------------------------------

    @rmi
    def _script_get(self, section_name):
        pass

    @rmi
    def _script_set(self, section_name):
        pass

    @rmi
    def _script_keys(self):
        pass

    @cached_property
    def script(self):
        """
        The definition's script sections are accessed with this property.

        Examples::

            checks = defn.script['Checks']       # Get script section
            defn.script['Computations'] = "..."  # Add/Change script section
            del defn.script['FlyBy']             # Delete script section

        .. versionadded:: 2.2
        """
        return Scripts(self)


#===============================================================================
# Definition Scripts
#===============================================================================

class Scripts:
    """
    Definition Script Container

    Examples::

        checks = defn.script['Checks']       # Get script section
        defn.script['Computations'] = "..."  # Add/Change script section
        del defn.script['FlyBy']             # Delete script section
    """

    def __init__(self, defn):
        self._defn = defn


    def __getitem__(self, section_name: str) -> str:
        return self._defn._script_get(section_name)


    def __setitem__(self, section_name: str, text: str):
        if not text:
            raise ValueError("Cannot set script section to nothing; "
                             f"Try 'del defn.scripts[{section_name!r}]'")
        if not isinstance(text, str):
            raise TypeError("Text section must be a string")

        return self._defn._script_set(section_name, text)


    def __delitem__(self, section_name: str):
        return self._defn._script_set(section_name, None)


    def keys(self) -> Sequence[str]:
        """
        Defined script section names
        """
        return self._defn._script_keys()


    def __iter__(self) -> Iterable[str]:
        return iter(self.keys())

#===============================================================================
# PSCAD Component
#===============================================================================
# pylint: disable=too-many-lines

"""
=========
Component
=========
"""

#===============================================================================
# Imports
#===============================================================================

from __future__ import annotations

import logging
import csv
from typing import (cast, Any, Dict, List, NewType, Optional, Tuple,
                    TYPE_CHECKING)

from mhi.common.cache import cached_property, timed_cached_property
from mhi.common.remote import RemoteException

from .remote import Remotable, rmi, rmi_property, deprecated, requires
from .resource import RES_ID
from .types import NodeType, Electrical, Signal, Point, Port, AnyPoint
from .types import Parameters, Rect
from .form import FormCodec, ParameterCodec

if TYPE_CHECKING:
    from .canvas import Canvas
    from .definition import Definition
    from .project import Project


#===============================================================================
# Logging
#===============================================================================

LOG = logging.getLogger(__name__)


#===============================================================================
# MovableMixin Mixin
#===============================================================================

class MovableMixin:
    """
    Things that may be moved
    """

    #---------------------------------------------------------------------------
    # Properties
    #---------------------------------------------------------------------------

    @rmi_property
    def parent(self):
        """
        Canvas this component is located on (read-only)

        :type: Canvas
        """

    @timed_cached_property(secs=5)
    def location(self) -> Tuple[int, int]:
        """
        Component (X, Y) location, in grid units
        """

        return self._rmi_getprop('location')


    @location.setter                                    # type: ignore[no-redef]
    def location(self, location: Tuple[int, int]):

        self._rmi_setprop('location', location)
        del self.bounds


    @timed_cached_property(secs=5)
    def bounds(self):
        """
        The left, top, right and bottom bounds of the component, in grid units
        (read only)

        :type: Rect
        """

        return Rect(*self._rmi_getprop('bounds'))


    #---------------------------------------------------------------------------
    # Getter/Setter
    #---------------------------------------------------------------------------

    @deprecated("Use .location = (x, y)")
    def set_location(self, x, y):

        """
        Set the component's (x,y) location

        Parameters:
            x (int): The new x location for this component
            y (int): The new y location for this component
        """

        self.location = (x, y)

    @deprecated("Use .location")
    def get_location(self):

        """
        Get this component's (x,y) location

        Returns:
            Tuple[int, int]: The x,y location of the component, in grid units
        """

        return self.location


    #---------------------------------------------------------------------------
    # Copy/Cut/Paste/Delete
    #---------------------------------------------------------------------------

    def copy(self) -> bool:
        """
        Copy this component to the clipboard.
        """

        return self.parent.copy(self)

    def cut(self) -> bool:
        """
        Cut this component to the clipboard
        """

        # Clear position/bound cache
        del self.bounds

        return self.parent.cut(self)

    def delete(self) -> bool:
        """
        Delete this component.
        """

        return self.parent.delete(self)


#===============================================================================
# Sizeable Mixin
#===============================================================================

class SizeableMixin:
    """
    Things that can be resized
    """

    size = rmi_property(True, True, name='size',
                        doc="Set/get width & height of a sizeable component")

    @deprecated("Use .size = (width, height)")
    def set_size(self, width: int, height: int) -> None: # pylint: disable=missing-function-docstring
        self.size = (width, height)

    @deprecated("Use .size")
    def get_size(self) -> Tuple[int, int]: # pylint: disable=missing-function-docstring
        return self.size


#===============================================================================
# PSCAD ZComponent
#===============================================================================

class ZComponent(Remotable):
    """
    All ZSLibrary components
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
        The name of the project this component exists in (read-only)

        :type: str
        """

        return self._identity['project']


    def project(self) -> Project:
        """
        The project this component exists in

        :type: Project
        """

        return self._pscad.project(self.project_name)


    @property
    def iid(self) -> int:
        """
        The id of the component in the project (read-only)

        :type: int
        """

        return self._identity['iid']


    #---------------------------------------------------------------------------
    # Definition
    #---------------------------------------------------------------------------

    @rmi_property
    def _defn_name(self):
        pass


    @cached_property
    def defn_name(self) -> str:
        """
        The name of the definition (read-only)
        """

        defn_name = self._defn_name
        if isinstance(defn_name, str):
            return defn_name
        scope, name = defn_name
        return f'{scope}:{name}'


    #===========================================================================
    # Commands & Generic Events
    #===========================================================================

    @rmi
    def _event(self,
               event_id: int, wparam: int = 0, lparam: int = 0,
               delta: int = 0, action=None) -> bool:
        pass


    def _command_id(self, cmd_id: int, *, action: Optional[str] = None) -> bool:
        WM_COMMAND = 0x0111                       # pylint: disable=invalid-name
        return self._event(WM_COMMAND, cmd_id, 0, 0, action)


    def _command(self, cmd: str) -> bool:
        return self._command_id(RES_ID[cmd])


    def _command_wait(self, cmd: str) -> None:
        self._command(cmd)
        self._pscad.wait_for_idle()


    def command(self, cmd_name):    # pylint: disable=missing-function-docstring
        raise NotImplementedError("Use official documented methods.")


    #---------------------------------------------------------------------------
    # Clone (with new location)
    #---------------------------------------------------------------------------

    @rmi
    def _clone(self, x, y):
        pass

    def clone(self, x: int, y: int) -> Component:
        """
        Copy this component and place the copy at the given location.

        Parameters:
            x (int): x-coordinate for the cloned component (in grid units)
            y (int): y-coordinate for the cloned component (in grid units)

        Returns:
            Component: the cloned component
        """

        return self._clone(x, y)

    #---------------------------------------------------------------------------
    # Z-Order
    #---------------------------------------------------------------------------

    def to_back(self) -> bool:
        """
        Put at the start (back) of the Z-Order on the canvas.
        """

        return self._command('IDZ_CMP_FIRST')

    def to_front(self) -> bool:
        """
        Put at the front (end) of the Z-Order on the canvas.
        """

        return self._command('IDZ_CMP_LAST')

    def to_next(self) -> bool:
        """
        Move the component one position forward in the Z-Order relative to the
        current Z-Order position.
        """

        return self._command('IDZ_CMP_NEXT')

    def to_prev(self) -> bool:
        """
        Move the component one position backward in the Z-Order relative to the current
        current Z-Order position.
        """

        return self._command('IDZ_CMP_PREV')


    #===========================================================================
    # Layer
    #===========================================================================

    layer = rmi_property(True, True, name="layer",
                         doc="The layer the component is on")

    def add_to_layer(self, name: str) -> None:
        """
        Add this component to the given layer.

        The layer must exist, but need not be enabled or visible.

        Parameters:
            name (str): The layer to add the component to.
        """

        self.layer = name

    def remove_from_layer(self, name: str) -> None:
        """
        Remove this component from the given layer.

        The layer must exist, but need not be enabled or visible.

        Parameters:
            name (str): The layer to remove the component from.
        """

        if self.layer == name:
            self.layer = None


    enabled = rmi_property(True, False, name="enabled", requires="5.0.2",
                           doc="The component's enable/disable status.\n\n"
                           "This is independent of whether the component is "
                           "on a layer that is enabled or disabled.\n\n"
                           ".. versionadded:: 2.8.1")

    def enable(self, enable: bool = True) -> None:
        """
        Enable this component.

        With no argument, or if given a `True` value, this will enable a
        disabled component.  If the component is disabled via layers it will
        remain disabled.

        Parameters:
            enable (bool): If set to `False`, disables the component (optional)
        """

        if enable:
            self._command('IDM_ENABLE')
        else:
            self._command('IDM_DISABLE')


    def disable(self) -> None:
        """
        Disable this component.

        This component will be disabled regardless of the layer states.
        To re-enable this component use the :meth:`.enable` function.
        """

        self.enable(False)

    @rmi
    def _custom_state(self, state_name, state):
        pass

    def custom_state(self, state_name: str, state: str) -> None:
        """
        Set a custom layer state for this component.

        The component must already be part of a layer, and that layer must
        already have the named custom state :meth:`added <.Layer.add_state>`
        to it.  This component will be set to the given state when the
        component's layer is set to the given custom state name.

        Parameters:
            state_name (str): The component's layer's custom state name
            state (str): One of 'Enabled', 'Disabled' or 'Invisible'
        """

        if state not in ('Enabled', 'Disabled', 'Invisible'):
            raise ValueError("Invalid state.  Must be 'Enabled', 'Disabled', "
                             "or 'Invisible'")

        self._custom_state(state_name, state)


    #===========================================================================
    # Parameters
    #===========================================================================

    @rmi
    def _parameters(self, scenario, link_id, parameters):
        pass


    @rmi
    def _get_parameter(self, parameters):
        pass


    @rmi
    def _form_xml(self):
        pass


    def _param_codec(self):

        codecs = self._pscad._zcmp_codec
        key = self.__class__
        codec = codecs.get(key)
        if codec is None:
            try:
                xml = self._form_xml()
            except ValueError:
                xml = None

            if xml:
                codec = FormCodec(xml)
            else:
                codec = ParameterCodec.DEFAULT

            codecs[key] = codec

        return codec


    def parameters(self, *, parameters: Optional[Parameters] = None, **kwargs
                   ) -> Optional[Parameters]:
        """
        Set or get the component's parameters.

        Parameters:
            parameters (dict): A dictionary of parameter values. (optional)
            **kwargs: name=value keyword parameters.

        Returns:
            A dictionary of parameter values (if no parameters are being set),
            or None.
        """

        codec = self._param_codec()

        parameters = dict(parameters, **kwargs) if parameters else kwargs
        if parameters:
            parameters = codec.encode(parameters)

            # Component boundaries can change when parameters change
            if isinstance(self, MovableMixin):
                del self.bounds

        parameters = self._parameters(None, -1, parameters)
        parameters = codec.decode(parameters)

        return parameters


    @deprecated("Use component.parameters(...)")
    def set_parameters(self, **parameters): # pylint: disable=missing-function-docstring
        if not parameters:
            raise ValueError("No parameters given")

        return self.parameters(parameters=parameters)


    @deprecated("Use component.parameters()")
    def get_parameters(self):               # pylint: disable=missing-function-docstring
        return self.parameters()


    def __getitem__(self, key: str) -> Any:
        val = self._get_parameter(key)
        val = self._param_codec()._decode(key, val)
        return val


    def __setitem__(self, key: str, value: Any) -> None:
        self.parameters(parameters={key: value})


    def range(self, parameter: str):
        """
        Get legal values for a parameter

        Parameters:
            parameter (str): A component parameter name

        Returns:
            * a ``tuple``, or ``frozenset`` of legal values, or
            * a ``range`` of legal values (integer setttings only), or
            * a ``Tuple[float, float]`` defining minimum & maximum values, or
            * an exception if the parameter does not have a defined range.
        """

        codec = self._param_codec()
        try:
            return codec.range(parameter)
        except KeyError:
            raise ValueError("No such parameter") from None
        except AttributeError:
            raise ValueError("No defined range for parameter") from None


    def view_parameter_grid(self) -> bool:
        """
        View the parameter grid for this component
        """

        return self._command('IDM_VIEW_PARAMETERSGRID')


    #---------------------------------------------------------------------------
    # Import / export
    #---------------------------------------------------------------------------

    def import_parameters(self, csvfile: str) -> None:
        """
        Import component parameters from a CSV file

        Read component parameters from a two-line CSV file,
        where the first row contains the parameter names and the second row
        contains the parameter values.  The first column represents the
        component identifier and the parameter name must be blank.
        """

        def to_param_name(label: str) -> str:
            idx = label.rfind('(')
            if idx >= 0 and label[-1] == ')':
                name = label[idx+1:-1]
            else:
                name = label

            if not name.isidentifier():
                raise ValueError(f"Invalid column label: {label}")

            return name

        with open(csvfile, encoding='utf8', newline='') as file:
            reader = csv.reader(file)
            headers = next(reader)
            values = next(reader)
            if len(headers) != len(values) or next(reader, None) is not None:
                raise ValueError("Unexpected data in parameter CSV file\n"
                                 f"#headers={len(headers)}, "
                                 f"#values={len(values)}")

        if headers.pop(0) != '':
            raise ValueError("Invalid parameter file format")
        values.pop(0)

        params = {to_param_name(hdr): val for hdr, val in zip(headers, values)}
        self.parameters(parameters=params)


    def export_parameters(self, csvfile: str) -> None:
        """
        Export component parameters to a CSV file

        Write component parameters to a two-line CSV file.
        The first row will contains the parameter names and the second row
        will contain the parameter values.
        The first column contains the component identifier and the
        parameter name will be blank.
        """

        params = self._parameters(None, -1, {})
        header = [''] + list(params.keys())
        values = [self.iid] + list(map(str, params.values()))

        with open(csvfile, 'w', encoding='utf8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerow(values)


    #===========================================================================
    # Repr
    #===========================================================================

    def __repr__(self):
        return f"{self.defn_name}#{self.iid}"


#===============================================================================
# Module
#===============================================================================

class ModuleMixin(ZComponent):                 # pylint: disable=abstract-method
    """
    Modules (Components containing a canvas with more components)
    """

    @property
    def definition(self) -> Definition:
        """
        Retrieve module definition
        """
        scope, name = self._defn_name
        return self._pscad.project(scope).definition(name)


    def canvas(self) -> Canvas:
        """
        Get the module's canvas

        Returns:
            :class:`.Canvas` : The canvas containing this module's subcomponents
        """

        scope, name = self._defn_name
        return self._pscad.project(scope).canvas(name)


#===============================================================================
# Ports
#===============================================================================

def _to_port(port):
    x, y, name, dim, node_type, subtype = port

    if ':' in name:
        name = name[:name.find(':')]

    node_type = NodeType(node_type)
    if node_type in (NodeType.INPUT, NodeType.OUTPUT):
        electrical = Electrical.FIXED
        signal = Signal(subtype)
    else:
        electrical = Electrical(subtype)
        signal = Signal.UNKNOWN

    return Port(x, y, name, dim, node_type, electrical, signal)


#===============================================================================
# PSCAD Component
#===============================================================================

class Component(ZComponent, MovableMixin):     # pylint: disable=abstract-method
    """
    Components which can be moved & rotated on a Canvas.
    They might also be modules.
    """

    #---------------------------------------------------------------------------
    # Orientable
    #---------------------------------------------------------------------------

    def mirror(self) -> bool:
        """
        Mirror the component along the horizontal axis
        """

        return self._command('IDM_MIRROR')


    def flip(self) -> bool:
        """
        Flip the component along the vertical axis
        """

        return self._command('IDM_FLIP')


    def rotate_right(self) -> bool:
        """
        Rotate the component 90 degrees to the right (clockwise)
        """

        return self._command('IDM_ROTATERIGHT')


    def rotate_left(self) -> bool:
        """
        Rotate the component 90 degrees to the left (counter-clockwise)
        """

        return self._command('IDM_ROTATELEFT')


    def rotate_180(self) -> bool:
        """
        Rotate the component 90 degrees to the right
        """

        return self._command('IDM_ROTATE180')


    orient = rmi_property(True, True, name='orient', requires="5.1",
                          doc="Set/get orientation of an orientable component")


    #---------------------------------------------------------------------------
    # Module?
    #---------------------------------------------------------------------------

    @rmi
    def is_module(self):
        """
        Check to see if this component has its own canvas, with in turn,
        can contain additional components.

        :class:`Transmission lines <.TLine>`, :class:`cables <.Cable>`,
        and some :class:`user components <.UserCmp>` are modules with
        their own canvas.

        Returns:
            bool: ``True`` if the component has an internal canvas,
            ``False`` otherwise.
        """


#===============================================================================
# PSCAD Wire
#===============================================================================

class Wire(Component):                         # pylint: disable=abstract-method

    """
    An electrical wire or control signal.

    Wires are continuous lines which connect 2 or more vertices.
    Each segment must be horizontal or vertical.

    To construct a new wire, use :meth:`.UserCanvas.create_wire()`.
    """

    @rmi
    def _vertices(self, vertices: Optional[List[Tuple[int, int]]] = None
                  ) -> List[Tuple[int, int]]:
        pass

    def vertices(self, *vertices: AnyPoint) -> List[Point]:
        """Wire.vertices([vertices])

        Set or get the vertices of the wire

        Parameters:
            vertices (List[x,y]): a list of (x,y) coordinates (optional)

        Returns:
            List[x,y]: A list of (x,y) coordinates.
        """

        if len(vertices) == 0:                  # pylint: disable=no-else-return
            vertexes = list(map(Point._make, self._vertices()))
            return vertexes
        else:
            # List of vanilla (x, y) tuples
            if len(vertices) == 1 and isinstance(vertices[0], list):
                vertices = cast(Tuple[Tuple[int, int]], vertices[0])

            vtxs = [(vtx[0], vtx[1]) for vtx in vertices]
            self._vertices(vtxs)
            return []

    def endpoints(self) -> Tuple[Point, Point]:
        """
        Get the end-points of the wire.  Internal vertices are not returned.

        Returns:
            List[Point]: The wire's end-points
        """

        vtx = self.vertices()
        return vtx[0], vtx[-1]

    def decompose(self):
        """
        Break the wire down into deperate wires
        """

        self._command('IDM_DECOMPOSEWIRE')


    def __repr__(self):
        return f"{self.__class__.__name__}#{self.iid}"


#===============================================================================
# PSCAD Sticky Wire
#===============================================================================

class StickyWire(Wire):                        # pylint: disable=abstract-method
    """
    A "Sticky Wire" is an electrical wire or control signal,
    which stretches to maintain connection to a component it is attached to.

    Unlike all other wires, a "Sticky Wire" may have more than two end-points.
    Each pair of vertices form a horizontal or vertical line segment,
    which is then attached to a central point by diagonal line segments.

    To construct a new sticky wire, use :meth:`.UserCanvas.create_sticky_wire()`.
    """


#===============================================================================
# PSCAD Bus
#===============================================================================

class Bus(Wire):                               # pylint: disable=abstract-method

    """
    Bus Component

    A Bus is a 3-phase electrical :class:`.wire`.
    It addition to :meth:`vertices <.vertices>`,
    it has :meth:`parameters <.UserCmp.parameters>` which can be set and
    retrieved.

    To construct a new bus, use :meth:`.UserCanvas.create_bus()`.

    .. table:: Bus Parameters

        =========== ===== ==============================================
        Parameter   Type  Description
        =========== ===== ==============================================
        Name        str   Name of the Bus
        BaseKV      float Bus Base Voltage, in kV. May be zero.
        VA          float Bus Base Angle, in degrees
        VM          float Bus Base Magnitude, in degrees
        type        int   0=Auto, 1=Load, 2=Generator or 3=Swing
        =========== ===== ==============================================
    """

    def __repr__(self):
        return f"Bus({self['Name']!r}, {self.iid})"


#===============================================================================
# PSCAD Travelling Wave Model Wires
#===============================================================================

class ACLine(Wire, ModuleMixin):               # pylint: disable=abstract-method
    """
    Travelling Wave Model lines (T-Line & Cables)
    """

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.defn_name}", {self.iid})'


    def compile(self) -> None:
        """
        Solve the constants for this T-Line/Cable page
        """
        self._command_wait('IDM_SOLVECONSTANTS')


class TLine(ACLine):       # pylint: disable=abstract-method, too-many-ancestors
    """
    Transmission Line Component

    A Transmission Line component is defined by 4 :meth:`vertices <.vertices>`,
    which form a 3 line segments.
    The first and last segments must be horizontal or vertical segments;
    the middle segment may be diagonal.

    It addition to vertices, a transmission line will also have a collection
    of :meth:`parameters <.UserCmp.parameters>` as well as a
    :meth:`canvas <.UserCmp.canvas>` containing additional components
    defining the transmission line.
    """

class Cable(ACLine):       # pylint: disable=abstract-method, too-many-ancestors
    """
    Cable Component

    A Cable component is defined by 4 :meth:`vertices <.vertices>`,
    which form a 3 line segments.
    The first and last segments must be horizontal or vertical segments;
    the middle segment may be diagonal.

    It addition to vertices, a cable will also have a collection
    of :meth:`parameters <.UserCmp.parameters>` as well as a
    :meth:`canvas <.UserCmp.canvas>` containing additional components
    defining the cable.
    """


#===============================================================================
# PSCAD UserCmp
#===============================================================================

class UserCmp(Component, ModuleMixin):         # pylint: disable=abstract-method
    """
    Non-builtin components (a.k.a User Components)
    """

    #===========================================================================
    # Repr
    #===========================================================================

    def __repr__(self):
        return f"{self.defn_name}#{self.iid}"


    #===========================================================================
    # Parameter Codec
    #===========================================================================

    _form_codecs: Dict[str, FormCodec] = {}

    def _param_codec(self):
        if self.defn_name not in self._form_codecs:
            try:
                xml = self._form_xml()
            except ValueError:
                xml = None

            if xml:
                codec = FormCodec(xml)
            else:
                codec = ParameterCodec.DEFAULT

            self._form_codecs[self.defn_name] = codec

        return self._form_codecs[self.defn_name]


    #===========================================================================
    # Definition
    #===========================================================================

    definition = rmi_property(True, True,             # type: ignore[assignment]
                              name="definition",
                              doc="The User Component's definition")

    @deprecated("Use the UserCmp.definition property")
    def get_definition(self):       # pylint: disable=missing-function-docstring
        return self.definition

    @deprecated("Use Component.copy() and Canvas.paste_transfer()")
    def copy_transfer(self):        # pylint: disable=missing-function-docstring
        return self.copy()


    #===========================================================================
    # Navigate
    #===========================================================================

    def navigate_in(self):
        """
        Navigate into a page module or definition
        """

        self._command('IDM_EDITDEFINITION')

        return self.canvas()


    #===========================================================================
    # Parameters
    #===========================================================================

    def parameters(self,
                   scenario: Optional[str] = None, *,
                   parameters: Optional[Parameters] = None,
                   **kwargs) -> Optional[Parameters]:
        """
        Set or get the component's parameters.

        Parameters:
            scenario (str): Name of scenario to set parameters for. (optional)
            parameters (dict): A dictionary of parameter values. (optional)
            **kwargs: name=value keyword parameters.

        Returns:
            A dictionary of parameter values (if no parameters are being set),
            or None.
        """

        codec = self._param_codec()

        parameters = dict(parameters, **kwargs) if parameters else kwargs
        if parameters:
            parameters = codec.encode(parameters)
            # Component boundaries can change when parameters change
            del self.bounds

        parameters = self._parameters(scenario, -1, parameters)
        parameters = codec.decode(parameters)
        return parameters

    @deprecated("Use component.parameters(...)")
    def set_parameters(self,
                       scenario: Optional[str] = None,
                       **kwargs) -> None:
        """set_parameters([scenario], name=value [, ...])
        Set the component's parameters.

        Parameters:
            scenario (str): Name of scenario to set parameters for. (optional)
            **kwargs: One or more name=value keyword parameters

        All parameters are converted to strings.  No checks are made to
        determine if a value is valid or not.
        """

        if not kwargs:
            raise ValueError("No parameters to set")

        self.parameters(scenario=scenario, parameters=kwargs)


    @deprecated("Use component.parameters()")
    def get_parameters(self,
                       scenario: Optional[str] = None
                       ) -> Optional[Parameters]:
        """
        Get the component's parameters.

        The parameters contained in the component are determined by the
        component definition.

        Parameters:
            scenario (str): Name of scenario to get parameters from. (optional)

        Returns:
            A dictionary of parameter name="value" pairs.
        """

        return self.parameters(scenario=scenario)

    @deprecated("Use component.view_parameter_grid()")
    def view_ParameterGrid(self):   # pylint: disable=invalid-name, missing-function-docstring
        return self.view_parameter_grid()


    #===========================================================================
    # Ports
    #===========================================================================

    @rmi
    def _ports(self):
        pass

    def ports(self) -> Dict[str, Port]:
        """
        Retrieve the active ports of a component.

        Returns:
            Dict[str, Port]: A dictionary of ports, by port name.
        """
        return {port.name: port for port in map(_to_port, self._ports())}

    def port(self, name: str) -> Optional[Port]:
        """
        Based on the location of this component, taking into account any
        any rotation and/or mirroring, return the location and type of the
        named component port.

        Returns:
            tuple: The x, y location, name, dimension and type of the port.
        """
        port = next((p for p in self._ports() if p[2] == name), None)
        if port:
            return _to_port(port)
        return None

    @deprecated("Use UserCmp.port()")
    def get_port_location(self, name): # pylint: disable=missing-function-docstring
        ports = self.ports()
        if name in ports:
            return ports[name]
        return None


    #===========================================================================
    # Compiling
    #===========================================================================

    sequence = rmi_property(True, True, name="sequence",
                            doc="Component Sequence Number")

    def compile(self) -> None:
        """
        Compile this component page
        """
        self._command_wait('IDM_PAGECOMPILE')


    @rmi
    def _blackbox(self, *args, **kwargs):
        pass

    def blackbox(self,
                 x: Optional[int] = None,
                 y: Optional[int] = None,
                 sub_prefix: Optional[str] = None,
                 instance_data: Optional[bool] = None
                 ) -> Component:
        """
        Convert this component page into a blackboxed module

        .. versionchanged:: 2.7
            Added ``x``, ``y``, ``sub_prefix`` & ``instance_data`` parameters.
        """

        args = []
        if x is not None and y is not None:
            args = [x, y]
        elif x is not None or y is not None:
            raise ValueError("Both x & y must be given if either is")
        kwargs = {'sub_prefix': sub_prefix, 'instance_data': instance_data}
        kwargs = {key: val for key, val in kwargs.items() if val is not None}

        try:
            return self._blackbox(*args, component_create=True, **kwargs)
        except RemoteException as ex:
            if not str(ex).startswith("Unknown method"):
                raise

        if args or kwargs:
            raise NotImplementedError("Blackbox with arguments requires"
                                      " version >= 5.0.2")

        self._command_wait('IDM_BLACKBOX')
        return None # type: ignore[return-value]


    @requires("5.0.2")
    def blackbox_defn(self) -> Definition:
        """
        Convert this component page into a blackboxed module definition

        .. versionadded:: 2.7
        """
        return self._blackbox(component_create=False)


#===============================================================================
# PGB
#===============================================================================

PGB = NewType("PGB", Component)

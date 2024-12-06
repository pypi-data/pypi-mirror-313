#===============================================================================
# PSCAD Canvas
#===============================================================================
# pylint: disable=too-many-lines

"""
======
Canvas
======
"""

#===============================================================================
# Imports
#===============================================================================

from __future__ import annotations

import logging
from warnings import warn
import itertools
import re

from typing import (Any, Dict, Iterator, List, Optional, Set, Sequence, Tuple,
                    Union, cast, TYPE_CHECKING)

from .remote import Remotable, rmi, deprecated, requires
from .form import FormCodec
from .resource import RES_ID
from .definition import Definition

from .types import BUILTIN_COMPONENTS as _BUILTIN_COMPONENTS
from .types import BUILTIN_COMPONENT_ALIAS as _BUILTIN_COMPONENT_ALIAS
from .types import Point, Port, Rect

if TYPE_CHECKING:
    from .annotation import Divider, GroupBox, Sticky
    from .component import Component, Bus, PGB, StickyWire, Wire
    from .control import Control, ControlFrame
    from .graph import GraphFrame, OverlayGraph, PlotFrame, PolyGraph, Curve
    from .instrument import Oscilloscope, PhasorMeter, PolyMeter
    from .types import AnyPoint


#===============================================================================
# Logging
#===============================================================================

LOG = logging.getLogger(__name__)


#===============================================================================
# PSCAD Canvas
#===============================================================================

class Canvas(Remotable):

    """
    A canvas is a surface where components can be placed and arranged.
    A "user canvas" is the most general version of a canvas.
    (T-Line and Cable canvases are more restrictive, permitting only certain
    types of components.)

    The main page of a project is typically retrieved with::

        main = project.canvas('Main')
    """

    #===========================================================================
    # Properties
    #===========================================================================

    @property
    def scope(self) -> str:
        """
        The name of the project (read-only)

        .. versionadded:: 2.0
        """

        return self._identity['scope']


    @property
    def name(self) -> str:
        """
        The name of the definition (read-only)

        .. versionadded:: 2.0
        """

        return self._identity['name']


    #===========================================================================
    # Repr
    #===========================================================================

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.scope}:{self.name}")'


    #===========================================================================
    # Parameters
    #===========================================================================

    @rmi
    def _parameters(self, parameters):
        pass


    def _parameters_codec(self) -> Optional[FormCodec]:
        return None


    #===========================================================================
    # Parameters
    #===========================================================================

    def parameters(self, parameters=None, **kwargs) -> Dict[str, Any]:

        """
        Get or set canvas parameters

        .. table:: Canvas Parameters

            =================== ===== ==========================================
            Param Name          Type  Description
            =================== ===== ==========================================
            auto_sequence       str   'MANUAL', 'AUTOMATIC'
            show_border         bool  Display re-sizing border
            monitor_bus_voltage bool  Display dynamic voltage levels on buses
            show_grid           bool  Show connection grid
            show_signal         bool  Show all locations tracked in signal table
            show_terminals      bool  Show where equipment ports are terminated
            show_sequence       bool  Display sequence order numbers
            show_virtual        bool  Show virtual wired signal relations
            virtual_filter      str   Comma separated signal names to show
            animation_freq      int   How often components are redrawn (msec)
            orient              str   'LANDSCAPE', 'PORTRAIT'
            size                str   '85X11', '11X17', '17X22', '22X34',
                                      '34X44', '100X100'
            =================== ===== ==========================================

        .. versionadded:: 2.1
        """

        def unsettable(kind, *keys):
            params = ", ".join(key for key in keys
                               if parameters.pop(key, None) is not None)
            if params:
                warn(f"Unable to set {kind} parameter(s): {params}",
                     stacklevel=3)

        codec = self._parameters_codec() # pylint: disable=assignment-from-none

        # Combined **kwargs in parameters dictionary
        parameters = dict(parameters, **kwargs) if parameters else kwargs

        unsettable("obsolete", 'bus_expand_x', 'bus_expand_y', 'bus_length', )

        if codec and parameters:
            parameters = codec.encode(parameters)
        parameters = self._parameters(parameters)
        if codec and parameters:
            parameters = codec.decode(parameters)

        return parameters


    def parameter_range(self, parameter: str):
        """
        Get legal values for a setting

        .. versionadded:: 2.1
        """
        codec = self._parameters_codec() # pylint: disable=assignment-from-none
        if not codec:
            raise ValueError("No defined ranges for parameters")

        try:
            return codec.range(parameter)
        except KeyError:
            raise ValueError("No such parameter") from None
        except AttributeError:
            raise ValueError("No defined range for parameter") from None


    #===========================================================================
    # Canvas dimensions
    #===========================================================================

    _SIZE = {'85X11': (68, 88),
             '11X17': (88, 136),
             '17X22': (136, 176),
             '22X34': (176, 272),
             '34X44': (272, 352),
             '100X100': (800, 800)}


    @property
    def size(self):
        """
        Canvas size, in grid units

        .. versionadded:: 2.9.6
        """

        params = self.parameters()
        width, height = self._SIZE[params['size']]
        if params['orient'] == 'LANDSCAPE':
            width, height = height, width

        return width, height


    #===========================================================================
    # Commands & Generic Events
    #===========================================================================

    @rmi
    def _event(self, event_id: int, wparam: int = 0, lparam: int = 0,
               delta: int = 0, **kwargs) -> bool:
        pass


    def _command(self, cmd: Union[int, str], **kwargs) -> bool:
        if isinstance(cmd, str):
            cmd_id = RES_ID[cmd]
        else:
            cmd_id = cmd

        WM_COMMAND = 0x0111  # pylint: disable=invalid-name
        return self._event(WM_COMMAND, cmd_id, **kwargs)


    #---------------------------------------------------------------------------
    # Navigate Up
    #---------------------------------------------------------------------------

    def navigate_up(self) -> None:
        """
        Navigate to parent page
        """

        self._pscad.navigate_up()


    #===========================================================================
    # Find Components
    #===========================================================================

    @deprecated('XML fragments are not supported.  Use Canvas.components()')
    def list_components(self): # pylint: disable=missing-function-docstring
        raise NotImplementedError()


    def _find(self, *names: Optional[str], **params) -> List[Component]:

        if len(names) >= 2 and params:
            namespace, defn_name, *_ = names

            if namespace and defn_name:
                try:
                    prj = self._pscad.project(namespace)
                    defn = prj.definition(defn_name)
                    codec = defn.form_codec
                    params = codec.encode(params)
                except ValueError:
                    pass

        return self._rmi('_find', *names, **params)


    #---------------------------------------------------------------------------
    # List all components
    #---------------------------------------------------------------------------

    def components(self) -> List[Component]:
        """
        Get a list of all components on the canvas.

        This is equivalent to calling ``Project.find_all()``,
        where no filter criteria is used to select a subset of components.

        Returns:
            List[Component]: The list of components

        .. versionadded:: 2.0
        """
        return self._find()


    #---------------------------------------------------------------------------
    # Find all
    #---------------------------------------------------------------------------

    def find_all(self, *name: str, layer: Optional[str] = None,
                 **params) -> List[Component]:
        """
        find_all( [[definition,] name,] [layer=name,] [key=value, ...])

        Find all components that match the given criteria.
        If no criteria is given, all components on the canvas are returned.

        Parameters:
            definition (str): One of "Bus", "TLine", "Cable", "GraphFrame",
                "Sticky", or a colon-seperated definition name, such as
                "master:source3" (optional)
            name (str): the component's name, as given by a parameter
                called "name", "Name", or "NAME".
                If no definition was given, and if the provided name is
                "Bus", "TLine", "Cable", "GraphFrame", "Sticky", or
                contains a colon, it is treated as the definition name.
                (optional)
            layer (str): only return components on the given layer (optional)
            key=value: A keyword list specifying additional parameters
               which must be matched.  Parameter names and values must match
               exactly. For example, Voltage="230 [kV]" will not match
               components with a Voltage parameter value of "230.0 [kV]".
               (optional)

        Returns:
            List[Component]: The list of matching components,
            or an empty list if no matching components are found.

        Examples::

           c = find_all('Bus'                # all Bus components
           c = find_all('Bus10')             # all components named "Bus10"
           c = find_all('Bus', 'Bus10')      # all Bus component named "Bus10"
           c = find_all('Bus', BaseKV='138') # all Buses with BaseKV="138"
           c = find_all(BaseKV='138')        # all components with BaseKV="138"
        """

        if len(name) > 2:
            raise ValueError("Too many names")

        namespace = None
        defn = name[0] if len(name) > 0 else None
        named = name[1] if len(name) > 1 else None

        if defn:
            if defn in _BUILTIN_COMPONENTS:
                pass
            elif defn in _BUILTIN_COMPONENT_ALIAS:
                defn = _BUILTIN_COMPONENT_ALIAS[defn]
            elif ':' in defn:
                namespace, defn = defn.split(':', 1)
            elif not named:
                named = defn
                defn = None

        return self._find(namespace, defn, named, layer, **params)


    #---------------------------------------------------------------------------
    # Find first
    #---------------------------------------------------------------------------

    def find_first(self, *names: str, layer: Optional[str] = None,
                   **params) -> Optional[Component]:
        """
        find_first( [[definition,] name,] [layer=name,] [key=value, ...])

        Find the first component that matches the given criteria,
        or ``None`` if no matching component can be found.
        """

        components = self.find_all(*names, layer=layer, **params)
        return components[0] if components else None


    #---------------------------------------------------------------------------
    # Find (singular)
    #---------------------------------------------------------------------------

    def find(self, *names, layer=None, **params) -> Optional[Component]:
        """
        find( [[definition,] name,] [layer=name,] [key=value, ...])

        Find the (singular) component that matches the given criteria,
        or ``None`` if no matching component can be found.
        Raises an exception if more than one component matches
        the given criteria.
        """

        components = self.find_all(*names, layer=layer, **params)
        if len(components) > 1:
            raise ValueError("Multiple components found")

        return components[0] if components else None


    #===========================================================================
    # Names in Use
    #===========================================================================

    @rmi(fallback=True)
    def _param_values(self, param_name, namespace, defn, named, **params):

        if param_name == 'Name':
            param_names = ['name', 'Name', 'NAME']
        else:
            param_names = [param_name]

        components = self._find(namespace, defn, named, **params)

        if self.main.minimum_version('5.1'):
            # Slower
            values = {value for param in param_names
                      for value in self.main.map_call(components,
                                                      '_get_parameter',
                                                      param)
                      if isinstance(value, str)}
        else:
            # Slowest
            values = set()
            for cmp in components:
                parameters = cmp.parameters()
                for param in param_names:
                    value = parameters.get(param_name)
                    if value is not None:
                        values.add(value)

        return values


    def names_in_use(self, defn: Optional[str] = None, **params) -> Set[str]:
        """
        Return the set of "Name" parameter values, for all components on the
        canvas that have a "Name" parameter.
        """

        namespace = None
        if defn:
            if defn in _BUILTIN_COMPONENTS:
                pass
            elif defn in _BUILTIN_COMPONENT_ALIAS:
                defn = _BUILTIN_COMPONENT_ALIAS[defn]
            else:
                namespace, defn = defn.split(':', 1)

        return self._param_values('Name', namespace, defn, None, **params)


    #===========================================================================
    # Bounds
    #===========================================================================

    @requires('5.1')
    def bounds(self, components: Sequence[Component]
               ) -> List[Rect]:
        """
        Return a list of the bounds of the given components.

        Equivalent to ``[cmp.bounds for cmp in components]`` but without
        the round trip to the server for each component.

        .. versionadded:: 2.9.6
        """

        bounds = self._pscad.map_property(components, "bounds")
        return [Rect(*bound) for bound in bounds]


    # ===========================================================================
    # Get empty spaces
    # ===========================================================================

    @requires("5.1")
    def _get_empty_matrix(self) -> List[List[bool]]:
        """
        Returns a matrix of True and False values, each representing a point on
        the canvas grid. True means empty.
        """

        w, h = self.size
        matrix = [[True] * (w + 1) for _ in range(h + 1)]
        bounds = self.bounds(self.components())
        for left, top, right, bottom in bounds:
            for i, j in itertools.product(
                range(top, bottom + 1), range(left, right + 1)
            ):
                matrix[i][j] = False

        return matrix


    def _get_empty_rects(self, w: int, h: int) -> Iterator[Rect]:
        matrix = self._get_empty_matrix()
        ncols = len(matrix[0])
        ver = [0] * ncols
        for r, row in enumerate(matrix, 1 - h):
            ver = [cnt + 1 if cell else 0 for cnt, cell in zip(ver, row)]
            s = 0
            hor = [0] * ncols
            for i, cnt in enumerate(ver):
                if cnt >= h:
                    s += 1
                else:
                    s = 0
                hor[i] = s
            for c, (v_cnt, h_cnt) in enumerate(zip(ver, hor), 1 - w):
                if v_cnt >= h and h_cnt >= w:
                    yield Rect(c, r, c + w - 1, r + h - 1)


    @requires("5.1")
    def get_empty_rects(self, w: int, h: int) -> List[Rect]:
        """
        Returns empty rectangle spaces on the canvas.

        Parameters
        ----------
        w: int
            Width of the empty rectangles.
        h: int
            Height of the empty rectangles.

        Returns
        ----------
        List[Rect]
            List of empty rectangles.


        .. versionadded:: 2.9.6
        """

        return list(self._get_empty_rects(w, h))


    @requires("5.1")
    def closest_empty_rect(
            self, w: int, h: int, point: Union[Tuple[int, int], Point]
    ) -> Rect:
        """
        Returns an empty rectangle with the size provided, closest to
        the given point.

        Parameters
        ----------
        w: int
            Width of the empty rectangle.
        h: int
            Height of the empty rectangle.
        point: Union[Tuple[int, int], Point]
            The point to which the nearest empty rectangle is found.

        Returns
        ----------
        Rect
            Closest empty rectangle to the given point.


        .. versionadded:: 2.9.6
        """

        # Make sure type(point) == Point
        point = Point(*point)

        def key(rect):
            return rect.mid.distance(point)

        return min(self._get_empty_rects(w, h), key=key)


    #===========================================================================
    # Get Component By Id
    #===========================================================================

    @rmi
    def component(self, iid) -> Component:
        """
        Retrieve a component by ID.

        Parameters:
            iid (int): The ID attribute of the component.

        .. versionadded:: 2.0
            This command replaces all of the type specific versions.
        """


    #===========================================================================
    # Clipboard / Selection
    #===========================================================================

    @rmi
    def _select(self, *args):
        pass


    def clear_selection(self):
        """
        Reset the selection so that no components are selected.
        """

        return self._select()


    def select(self, *components: Component):
        """
        Place specific components in the current selection.

        Parameters:
            components (list): the components to be selected.

        .. versionadded:: 2.0
        """

        return self._select(*components)


    def select_components(self,
                          x1: int, y1: int,
                          x2: Optional[int] = None,
                          y2: Optional[int] = None,
                          width: Optional[int] = None,
                          height: Optional[int] = None):
        """
        Select components in a rectangular area.

        If width and height are used, the x1,y1 values are interpreted as the
        lower-left corner of the region.  If both x1,y1 and x2,y2 are given,
        any opposite corners may be used and the rectangle will be normalized
        for the user automatically.

        All values are in grid coordinates.

        Parameters:
            x1 (int): lower left corner of the selection region
            y1 (int): lower left corner of the selection region
            x2 (int): upper right corner of the selection region (optional)
            y2 (int): upper right corner of the selection region (optional)
            width (int): width of the selection region (optional)
            height (int): height of the selection region (optional)
        """

        if (x2 is None) == (width is None):
            LOG.error("select_components: x2=%r and width=%r", x2, width)
            raise ValueError("Specify either x2 or width (but not both)")
        if (y2 is None) == (height is None):
            LOG.error("select_components: y2=%r and height=%r", y2, height)
            raise ValueError("Specify either y2 or height (but not both)")

        if x2 is None and width is not None:
            x2 = x1 + width
        if y2 is None and height is not None:
            y2 = y1 - height

        return self._select((x1, y1), (x2, y2))


    @rmi
    def _selection(self):
        pass


    @requires("5.0.1")
    def selection(self) -> List[Component]:
        """
        Retrieve the components which are selected on the canvas.

        .. versionadded:: 2.3.2
        """

        return self._selection()


    #---------------------------------------------------------------------------
    # Copy/Cut/Paste
    #---------------------------------------------------------------------------

    def copy(self, *components: Component) -> bool:
        """
        Copy the given list of components, or currently selected components
        if no components are given, to the clipboard.

        Parameters:
            *components (List[Component]): Components to be copied (optional)

        .. versionchanged:: 2.1
            Added optional list of ``components``
        """

        if components:
            self.select(*components)

        return self._command('IDM_COPY')


    def cut(self, *components: Component) -> bool:
        """
        Cut the given list of components, or currently selected components
        if no components are given, to the clipboard.

        Parameters:
            *components (List[Component]): Components to be cut (optional)

        .. versionchanged:: 2.1
            Added optional list of ``components``
        """

        if components:
            self.select(*components)

        return self._command('IDM_CUT')


    def delete(self, *components: Component) -> bool:
        """
        Delete the given list of components, or currently selected components
        if no components are given.

        Parameters:
            *components (List[Component]): Components to be deleted (optional)

        .. versionchanged:: 2.1
            Added optional list of ``components``
        """

        if components:
            self.select(*components)

        return self._command('IDM_DELETE')


    def paste(self, mouse_x: int, mouse_y: int) -> bool:
        """
        Paste the contents of the clipboard into this canvas at the
        indicated mouse location.

        .. versionchanged:: 2.1
            Added ``mouse_x`` and ``mouse_y``
        """

        self._event(0x0200, mx=mouse_x, my=mouse_y)
        return self._command('IDM_PASTE')


    #===========================================================================
    # Rotate and Mirror a selection of component
    #===========================================================================

    def mirror(self, *components: Component) -> bool:
        """
        Mirror the given list of components, or the currently selected
        components if no components are given, along the horizontal axis.

        Parameters:
            *components (List[Component]): Components to be mirrored (optional)
        """

        if components:
            self.select(*components)

        return self._command('IDM_MIRROR')


    def flip(self, *components: Component) -> bool:
        """
        Flip the given list of components, or the currently selected
        components if no components are given, along the vertical axis.

        Parameters:
            *components (List[Component]): Components to be flipped (optional)
        """

        if components:
            self.select(*components)

        return self._command('IDM_FLIP')


    def rotate_right(self, *components: Component) -> bool:
        """
        Rotate the given list of components, or the currently selected
        components if no components are given, 90 degrees clockwise.

        Parameters:
            *components (List[Component]): Components to be rotated (optional)
        """

        if components:
            self.select(*components)

        return self._command('IDM_ROTATERIGHT')


    def rotate_left(self, *components: Component) -> bool:
        """
        Rotate the given list of components, or the currently selected
        components if no components are given, 90 degrees counter-clockwise.

        Parameters:
            *components (List[Component]): Components to be rotated (optional)
        """

        if components:
            self.select(*components)

        return self._command('IDM_ROTATELEFT')


    def rotate_180(self, *components: Component) -> bool:
        """
        Rotate the given list of components, or the currently selected
        components if no components are given, 180 degrees.

        Parameters:
            *components (List[Component]): Components to be rotated (optional)
        """

        if components:
            self.select(*components)

        return self._command('IDM_ROTATE180')


    #===========================================================================
    # add_component
    #===========================================================================

    @rmi
    def _create(self, defn, x, y, orient):
        pass


    def create_component(self, defn: Union[str, Definition],
                         x: int = 1, y: int = 1, orient: int = 0,
                         **parameters) -> Component:
        """
        Create a new component and add it to the canvas.

        Parameters:
            defn (Union[str, Definition]): Type of component to create
            x (int): X location of the component (in grid units).
            y (int): Y location of the component (in grid units).
            orient (int): Rotation/mirroring of the component
            parameters: key=value pairs

        Returns:
            The created :class:`.Component`.

        .. versionadded:: 2.0

        .. versionchanged:: 2.2
            ``defn`` accepts a :class:`.Definition` or a string.
        """

        if isinstance(defn, Definition):
            defn = defn.scoped_name

        component = self._create(defn, x, y, orient)
        if component and parameters:
            component.parameters(parameters=parameters)

        return component


    def add_component(self,
                      library: str, name: str,
                      x: int = 1, y: int = 1, orient: int = 0,
                      **parameters) -> Component:
        """
        Create a new user component and add it to the canvas.

        Parameters:
            library (str): Library the definition may be found in.
            name (str): Name of the component definition in the library.
            x (int): X location of the component (in grid units).
            y (int): Y location of the component (in grid units).

        Returns:
            The created :class:`.Component`.

        .. versionchanged:: 2.0
            Added ``orient`` and ``**parameters``
        """

        defn = f"{library}:{name}"

        return self.create_component(defn, x, y, orient, **parameters)


#===============================================================================
# PSCAD UserCanvas
#===============================================================================

class UserCanvas(Canvas):

    """
    A user canvas is a surface where components can be placed and arranged.

    The main page of a project is typically retrieved with::

        main = project.canvas('Main')
    """

    #===========================================================================
    # Parameters
    #===========================================================================

    def _parameters_codec(self):
        return FormCodec.user_canvas(self)


    def parameters(self, parameters: Optional[Dict[str, Any]] = None,
                   **kwargs):

        """
        Get or set User Canvas parameters

        .. table:: User Canvas Settings

           =================== ======= ================================================
           Param Name          Type    Description
           =================== ======= ================================================
           auto_sequence       Choice  Sequence Ordering: MANUAL, AUTOMATIC
           show_border         Boolean Bounds
           monitor_bus_voltage Boolean Bus Monitoring
           show_grid           Boolean Grids
           show_signal         Boolean Signals
           show_terminals      Boolean Terminals
           show_sequence       Boolean Sequence Order Numbers
           show_virtual        Boolean Virtual Wires
           size                Choice  Size: 85X11, 11X17, 17X22, 22X34, 34X44, 100X100
           orient              Choice  Orientation: PORTRAIT, LANDSCAPE
           virtual_filter      Text    Virtual Wires Filter
           animation_freq      Integer Animation Update Frequency
           =================== ======= ================================================

        .. versionadded:: 2.1
        """

        def unsettable(kind, *keys):
            params = ", ".join(key for key in keys
                               if parameters.pop(key, None) is not None)
            if params:
                warn(f"Unable to set {kind} parameter(s): {params}",
                     stacklevel=3)

        codec = self._parameters_codec()

        # Combined **kwargs in parameters dictionary
        parameters = dict(parameters, **kwargs) if parameters else kwargs

        unsettable("obsolete", 'bus_expand_x', 'bus_expand_y', 'bus_length', )

        if codec and parameters:
            parameters = codec.encode(parameters)

        missing_keys = []
        while True:
            try:
                parameters = self._parameters(parameters)
                break
            except KeyError as err:
                m = re.match('"No such entry name: \'(\\w+)\'"', str(err))
                if m:
                    key = m[1]
                    if key in {'show_terminals', 'virtual_filter',
                               'animation_freq'}:
                        del parameters[key]           # type: ignore[union-attr]
                        missing_keys.append(key)
                        continue
                raise
        if missing_keys:
            warn("Failed to set: " + ', '.join(missing_keys) + "\n"
                 "See: Known Issues V5 Automation #503\n"
                 "     https://www.pscad.com/knowledge-base/article/830",
                 stacklevel=2)

        if codec and parameters:
            parameters = codec.decode(parameters)

        return parameters


    #===========================================================================
    # Copy/Cut/Paste
    #===========================================================================

    def paste_transfer(self, mouse_x: int, mouse_y: int) -> bool:
        """
        Paste a component and its definition from the clipboard,
        so it can be used in this project.

        .. versionchanged:: 2.0
            ``Component.copy_transfer()`` is deprecated; simply
            :meth:`.Canvas.copy()` the component(s) to the smart clipboard.
        """

        self._event(0x0200, mx=mouse_x, my=mouse_y)
        return self._command('IDM_PASTE_COPYTRANSFER')

    def paste_rename(self, mouse_x: int, mouse_y: int) -> bool:
        """
        Paste the contents of the clipboard and rename all the components
        to unique names.  All references to the original name will be

        .. versionadded:: 2.0
        """

        self._event(0x0200, mx=mouse_x, my=mouse_y)
        return self._command('IDM_PASTE_SPECIAL1')


    @deprecated("Use canvas.copy()")
    def copy_as_bitmap(self): # pylint: disable=missing-function-docstring
        return self.copy()


    @deprecated("Use canvas.copy()")
    def copy_as_metafile(self): # pylint: disable=missing-function-docstring
        return self.copy()


    def copy_controls(self, *controls): # pylint: disable=missing-function-docstring
        raise NotImplementedError()


    def cut_controls(self, *controls): # pylint: disable=missing-function-docstring
        raise NotImplementedError()


    #===========================================================================
    # Graphs & Meters
    #===========================================================================

    def create_graph_frame(self, x: int = 1, y: int = 1) -> GraphFrame:
        """
        Create an empty Graph Frame

        Parameters:
            x (int): X location of the graph frame (in grid units).
            y (int): Y location of the graph frame (in grid units).

        Returns:
            GraphFrame: The graph frame
        """

        cmp = self.create_component('GraphFrame', x, y)

        return cast(GraphFrame, cmp)


    def create_graph(self, pgb: Optional[PGB] = None,
                     x: int = 1, y: int = 1
                     ) -> Tuple[GraphFrame, OverlayGraph, Optional[Curve]]:
        """
        Create an Graph Frame containing an Overlay Graph with a Signal

        Parameters:
            pgb (Component): the PGB for the signal to add to the graph.
            x (int): X location of the graph frame (in grid units).
            y (int): Y location of the graph frame (in grid units).

        Returns:
            Tuple[GraphFrame,OverlayGraph,Curve]: The new graph frame, \
            Overlay Graph, and Curve.
        """

        if pgb and pgb.defn_name != 'master:pgb':
            raise TypeError("PGB required")

        graph_frame = self.create_graph_frame(x, y)
        overlay_graph, _ = graph_frame.add_overlay_graph()
        curve = None
        if pgb:
            curve = overlay_graph.create_curve(pgb)

        return graph_frame, overlay_graph, curve


    def create_polygraph(self, pgb: Optional[PGB] = None,
                         x: int = 1, y: int = 1,
                         digital: bool = False
                         ) -> Tuple[GraphFrame, PolyGraph, Optional[Curve]]:
        """
        Create an Stacked PolyGraph with a Signal

        Parameters:
            pgb (Component): the PGB for the signal to add to the graph.
            x (int): X location of the graph frame (in grid units).
            y (int): Y location of the graph frame (in grid units).
            digital (bool): Set to ``True`` to create a digital polygraph

        Returns:
            Tuple[GraphFrame,PolyGraph,Curve]: The new graph frame, \
            PolyGraph, and Curve.
        """

        if pgb and pgb.defn_name != ('master', 'pgb'):
            raise TypeError("PGB required")

        graph_frame = self.create_graph_frame(x, y)
        poly_graph, _ = graph_frame.add_poly_graph()
        curve = None
        if pgb:
            curve = poly_graph.create_curve(pgb, digital=digital)

        return graph_frame, poly_graph, curve


    def create_xy_plot(self, x: int = 1, y: int = 1, polar: bool = False
                       ) -> PlotFrame:
        """
        Create an XY PlotFrame

        Parameters:
            x (int): X location of the plot frame (in grid units).
            y (int): Y location of the plot frame (in grid units).
            polar (bool): Set to ``True`` to for the polar variant.

        Returns:
            PlotFrame: The plot frame
        """

        cmp = self.create_component('PlotFrame', x, y)
        plot_frame = cast(PlotFrame, cmp)

        if polar:
            plot_frame.polar = True

        return plot_frame

    @rmi
    def _create_meter(self, pgb: PGB, x: int, y: int, meter_type: int
                      ) -> Union[PolyMeter, PhasorMeter, Oscilloscope]:
        pass


    def create_poly_meter(self, pgb: Optional[Component] = None,
                          x: int = 1, y: int = 1) -> PolyMeter:
        """
        Create a polymeter from a PGB component

        Parameters:
            pgb (Component): a PGB component.
            x (int): X location of the polymeter (in grid units).
            y (int): Y location of the polymeter (in grid units).

        Returns:
            PolyMeter: the polymeter component.
        """

        return self._create_meter(pgb, x, y, 1)


    def create_phasor_meter(self, pgb: PGB, x: int = 1, y: int = 1,
                            angle: Optional[str] = None) -> PhasorMeter:
        """
        Create a phasor meter from a PGB component

        Parameters:
            pgb (Component): a PGB component.
            x (int): X location of the phasor meter (in grid units).
            y (int): Y location of the phasor meter (in grid units).
            angle (str): The input angle format ``"degrees"`` or ``"radians"``

        Returns:
            PhasorMeter: the phasor meter component.
        """

        phase_mtr: PhasorMeter = self._create_meter(pgb, x, y, 2)

        if angle is not None:
            if angle in {True, "d", "deg", "degree", "degrees"}:
                phase_mtr.degrees = True
            elif angle in {False, "r", "rad", "radian", "radians"}:
                phase_mtr.degrees = False
            else:
                raise ValueError("Invalid angle: "+angle)

        return phase_mtr


    def create_oscilloscope(self, pgb: PGB, x: int = 1, y: int = 1
                            ) -> Oscilloscope:
        """
        Create an oscilloscope from a PGB component

        Parameters:
            pgb (Component): a PGB component.
            x (int): X location of the oscilloscope (in grid units).
            y (int): Y location of the oscilloscope (in grid units).

        Returns:
            Oscilloscope: the oscilloscope component.
        """

        return self._create_meter(pgb, x, y, 3)


    #===========================================================================
    # Control Frame
    #===========================================================================

    def create_control_frame(self,   # pylint: disable=keyword-arg-before-vararg
                             x: int = 1, y: int = 1,
                             *control_components: Component
                             ) -> Tuple[ControlFrame, List[Control]]:
        """
        Create a control frame

        Parameters:
            x (int): X location of the control frame (in grid units).
            y (int): Y location of the control frame (in grid units).

        Returns:
            Tuple[ControlFrame,List[Controls]]: the control frame & any controls
        """

        cmp = self.create_component("ControlFrame", x, y)
        control_frame = cast(ControlFrame, cmp)
        controls = control_frame.create_controls(*control_components)

        return control_frame, controls


    #===========================================================================
    # Wires & Buses
    #===========================================================================

    @staticmethod
    def _orthogonal(vertices):
        """
        Turn a list of [x,y] pairs into a list of [x,y] pairs where
          - successive vertices are different
          - successive vertices are either horizontal or vertical
        """

        if not vertices:
            raise ValueError("At least one vertex must be supplied")

        vertexes = []

        itr = iter(vertices)
        vtx = next(itr)
        x_prev, y_prev = vtx[0], vtx[1]
        vertexes.append((x_prev, y_prev))

        for vtx in itr:
            x, y = vtx[0], vtx[1]
            if x != x_prev or y != y_prev:
                if x != x_prev and y != y_prev:
                    vertexes.append((x_prev, y))
                vertexes.append((x, y))
                x_prev, y_prev = x, y

        return vertexes


    def create_wire(self, *vertices: Tuple[int, int]) -> Wire:
        """create_wire( (x1,y1), (x2,y2), [... (xn,yn) ...])
        Create a new wire and add it to the canvas.

        If more than two vertices are given, a multi-vertex wire will be
        created.
        If any segment is neither horizontal or vertical, additional vertices
        will be inserted.

        Parameters:
            *vertices: A series of (X, Y) pairs, in grid units

        Returns:
            Wire: The created wire.

        Note:
            Use :meth:`.UserCmp.port()` to determine the locations to connect
            the wires to.

        .. versionchanged:: 2.0
            Replaces ``UserCanvas.add_wire(...)``
        """

        if len(vertices) == 1 and isinstance(vertices[0], list):
            vertices = cast(Tuple[Tuple[int, int]], vertices[0])

        vertices = self._orthogonal(vertices)
        x0, y0 = vertices[0]

        cmp = self.create_component('WireOrthogonal', x0, y0)
        wire = cast('Wire', cmp)
        wire.vertices(*vertices)

        return wire


    @deprecated("Use canvas.create_wire(...)")
    def add_wire(self, *vertices): # pylint: disable=missing-function-docstring
        return self.create_wire(*vertices)


    def create_bus(self, *vertices: Tuple[int, int]) -> Bus:
        """create_bus( (x1,y1), (x2,y2), [... (xn,yn) ...])
        Create a new bus and add it to the canvas.

        If more than two vertices are given, a multi-vertex bus will be
        created.
        If any segment is neither horizontal or vertical, additional vertices
        will be inserted.

        Parameters:
            *vertices: A series of (X, Y) pairs, in grid units

        Returns:
            Bus: The created bus.

        Note:
            Use :meth:`.UserCmp.port()` to determine the locations to connect
            the wires to.
        """

        vertices = self._orthogonal(vertices)
        x0, y0 = vertices[0]

        cmp = self.create_component('Bus', x0, y0)
        bus = cast(Bus, cmp)
        bus.vertices(*vertices)

        return bus


    def create_sticky_wire(self, *vertices: Tuple[int, int]) -> StickyWire:
        """create_sticky_wire( (x1,y1), (x2,y2), [... (xn,yn) ...])
        Create a sticky wire between two or more vertices.

        All vertices will be connected to a central point via a short
        one grid unit horizontal or vertical segment, followed by a
        diagonal segment.

        Parameters:
            *vertices: A series of (X, Y) pairs, in grid units

        Returns:
            StickyWire: The created sticky wire.
        """

        def nudge(vtx, ctr_x, ctr_y):
            x, y = vtx
            d_x = x - ctr_x
            d_y = y - ctr_y
            if abs(d_x) > abs(d_y):             # pylint: disable=no-else-return
                return (x + 1, y) if d_x < 0 else (x - 1, y)
            else:
                return (x, y + 1) if d_y < 0 else (x, y - 1)

        if vertices:
            x1, y1 = vertices[0]
        else:
            x1, y1 = 1, 1

        cmp = self.create_component("WireDiagonal", x1, y1)
        wire = cast('StickyWire', cmp)

        n_vtx = len(vertices)
        if n_vtx > 1:
            ctr_x = sum(vtx[0] for vtx in vertices) // n_vtx
            ctr_y = sum(vtx[1] for vtx in vertices) // n_vtx

            vtxs = [(0, 0)] * (n_vtx * 2)
            vtxs[1::2] = vertices
            vtxs[0::2] = [nudge(vtx, ctr_x, ctr_y) for vtx in vertices]
            vtxs[0:2] = vtxs[1::-1]     # Swap first two vertices

            wire.vertices(*vtxs)

        return wire


    def create_connection(
            self,
            p1: AnyPoint,
            p2: AnyPoint,
            *,
            label: Optional[str] = None,
            electrical: Optional[bool] = None,
    ) -> Optional[str]:
        """
        Creates a connection between two points. If ``label`` is not
        provided (default), the connection is made using wires; otherwise,
        ``electrical`` must be set to True/False to create electrical/data
        labels to connect points.

        Parameters
        ----------
        p1 : AnyPoint
            One of the two ends of connection
        p2 : AnyPoint
            The other end of connection
        label: str, optional
            Specifies the node label. A suffix, starting from "_2" is added to
            ``label`` until it is unique on canvas. Defaults to ``None``.
        electrical: bool, optional
            Set ``True``, for electrical and ``False`` for data node labels.
            Must be provided if ``label`` is specified. Defaults to ``None``.

        Returns
        -------
        Optional[str]
            Name of the node labels created if ``label`` is provided;
            otherwise, ``None``.


        .. versionadded:: 2.9.6

        .. versionchanged:: 3.0.2
            PSCAD 5.1 requirement is removed.
        """

        # In case they are not Points
        p1 = Point(*p1[:2]) if isinstance(p1, (Port, tuple)) else p1
        p2 = Point(*p2[:2]) if isinstance(p2, (Port, tuple)) else p2

        if (label is None) and (electrical is None):
            self.create_wire(p1, p2)

        elif (label is not None) and (electrical is not None):
            label = self._unique_label(label)
            comp = ["master:datalabel", "master:nodelabel"]
            self.create_component(comp[electrical], x=p1.x, y=p1.y, Name=label)
            self.create_component(comp[electrical], x=p2.x, y=p2.y, Name=label)

        else:
            raise ValueError("If label or electrical is specified, the other"
                             "one must be given as well.")

        return label


    def _unique_label(self, label: str) -> str:
        used_names = self.names_in_use()
        if label not in used_names:
            return label

        suffix = 2
        while f'{label}_{suffix}' in used_names:
            suffix += 1

        return f'{label}_{suffix}'


    #===========================================================================
    # Compose/decompose wires
    #===========================================================================

    def compose_wires(self, *wires: Wire) -> bool:
        """
        Join connected wire segments into multisegment wires
        """

        self.select(*wires)
        return self._command('ID_SELECTION_JOINWIRES')


    def decompose_wires(self, *wires: Wire) -> bool:
        """
        Split all of the segments of the wires into multiple simple wires
        """

        self.select(*wires)
        return self._command('ID_SELECTION_FORKWIRES')


    #===========================================================================
    # Group (Compose/Decompose components)
    #===========================================================================

    @rmi
    def group(self, *components: Component) -> Component:
        """
        Group the given list of components into one group component.

        Parameters:
            *components (List[Component]): Components to be grouped

        Returns:
            Component: the Aggregate component
        """


    #===========================================================================
    # Annotations, etc
    #===========================================================================

    def create_annotation(self, x: int = 1, y: int = 1,
                          line1: Optional[str] = None,
                          line2: Optional[str] = None) -> Component:
        """
        Create a two-line annotation component.

        Parameters:
            x (int): x-coordinate of the annotation (in grid units)
            y (int): y-coordinate of the annotation (in grid units)
            line1 (str): first line of text
            line2 (str): second line of text

        Returns:
            Component: the created annotation

        .. versionchanged:: 2.1
            Added ``line1`` and ``line2`` parameters
        """

        annotation = self.create_component("master:annotation", x, y)
        if line1 or line2:
            if line1 is not None:
                annotation['AL1'] = line1
            if line2 is not None:
                annotation['AL2'] = line2

        return annotation


    @requires("5.1")
    def create_group_box(self, x: int = 1, y: int = 1,
                         name: Optional[str] = None) -> GroupBox:
        """
        Create a group box.

        Parameters:
            x (int): x-coordinate of the group box (in grid units).
            y (int): y-coordinate of the group box (in grid units).
            name (str): Name (or caption) of group box.

        Returns:
            GroupBox: The created group box.

        .. versionadded:: 2.9
        """

        cmp = self.create_component("GroupBox", x, y)
        group_box = cast(GroupBox, cmp)
        if name is not None:
            group_box['name'] = name

        return group_box


    def create_sticky_note(self, x: int = 1, y: int = 1,
                           text: Optional[str] = None) -> Sticky:
        """
        Create a sticky note.

        Parameters:
            x (int): x-coordinate of the sticky note (in grid units).
            y (int): y-coordinate of the sticky note (in grid units).
            text (str): Content of sticky note.

        Returns:
            Sticky: The created sticky note.
        """

        cmp = self.create_component("Sticky", x, y)
        note = cast(Sticky, cmp)
        if text:
            note.text = text
        return note


    def create_divider(self, x: int = 1, y: int = 1, *,
                       width=None, height=None) -> Divider:
        """
        Create a divider component.

        Parameters:
            x (int): x-coordinate of the divider (in grid units).
            y (int): y-coordinate of the divider (in grid units).
            width (int): horizontal length of the divider, or
            height (int): vertical height of the divider

        Returns:
            Divider: the divider component

        .. versionchanged:: 2.1
            Added ``line1`` and ``line2`` parameters
        """

        if width and height:
            raise ValueError("Width and height cannot both be specified")

        cmp = self.create_component("Divider", x, y)
        divider = cast(Divider, cmp)
        if width:
            divider.horizontal(width)
        elif height:
            divider.vertical(height)

        return divider


    def create_divider_box(self, x: int, y: int, width: int, height: int
                           ) -> Tuple[Divider, Divider, Divider, Divider]:
        """
        Create a rectangular box using a divider for each side

        Parameters:
            x (int): left coordinate of the divider box (in grid units).
            y (int): top coordinate of the divider box (in grid units).
            width (int): horizontal length of the divider box.
            height (int): vertical height of the divider box.

        Returns:
            Tuple[Divider, ...]: the top, left, bottom and right dividers

        .. versionadded:: 2.1
        """

        top = self.create_divider(x, y, width=width)
        left = self.create_divider(x, y, height=height)
        bottom = self.create_divider(x, y+height, width=width)
        right = self.create_divider(x+width, y, height=height)

        return top, left, bottom, right


    def create_file(self, x: int = 1, y: int = 1, name: Optional[str] = None,
                    path: Optional[str] = None) -> Component:
        """
        Create a file link component

        Parameters:
            x (int): x-coordinate of the file link (in grid units).
            y (int): y-coordinate of the file link (in grid units).
            name (str): name to display on the file link
            path (str): path to the linked file

        Returns:
            Component: the file link component

        .. seealso:: :py:meth:`.Project.create_resource`
        """

        file = self.create_component("FileCmp", x, y)
        params = {}
        if name:
            params['name'] = name
        if path:
            params['filepath'] = path
        if params:
            file.parameters(parameters=params)
        return file


    @deprecated
    def create_case_link(self, x=1, y=1, name=None, hyperlink=None): # pylint: disable=missing-function-docstring
        link = self.create_component("CaseCmp", x, y)
        params = {}
        if name:
            params['display'] = name
        if hyperlink:
            params['location'] = hyperlink
        if params:
            link.parameters(parameters=params)
        return link


    def create_hyper_link(self, x: int = 1, y: int = 1,
                          name: Optional[str] = None,
                          hyperlink: Optional[str] = None) -> Component:
        """
        Create a hyper-link component

        Parameters:
            x (int): x-coordinate of the hyper-link (in grid units).
            y (int): y-coordinate of the hyper-link (in grid units).
            name (str): name to display on the hyper-link
            hyperlink (str): URL to the linked resource

        Returns:
            Component: the hyper-link component
        """

        link = self.create_component("UrlCmp", x, y)
        params = {}
        if name:
            params['display'] = name
        if hyperlink:
            params['hyperlink'] = hyperlink
        if params:
            link.parameters(parameters=params)
        return link


    #===========================================================================
    # Bookmark Link
    #===========================================================================

    @rmi
    def _create_bookmark(self, bookmark, x, y):
        pass


    def create_bookmark_link(self, bookmark, x: int = 1, y: int = 1
                             ) -> Component:
        """
        Create a bookmark link, which can be used to navigate to a bookmarked
        location.

        Parameters:
            bookmark: value returned from :meth:`.Project.bookmark`
            x (int): x-coordinate of the bookmark link (in grid units).
            y (int): y-coordinate of the bookmark link (in grid units).

        Returns:
            Component: the bookmark link component
        """

        return self._create_bookmark(bookmark, x, y)


    #===========================================================================
    # Get Component By Id (deprecated functions)
    #===========================================================================

    @deprecated('Use Canvas.component(iid)')
    def user_cmp(self, iid): # pylint: disable=missing-function-docstring
        return self.component(iid)

    bus = user_cmp
    tline = user_cmp
    cable = user_cmp
    graph_frame = user_cmp


    @deprecated('Use Canvas.component(iid), with just the last id')
    def _get_by_last_id(self, *iid):
        return self.component(iid[-1])

    overlay_graph = _get_by_last_id
    slider = _get_by_last_id
    switch = _get_by_last_id
    button = _get_by_last_id
    selector = _get_by_last_id

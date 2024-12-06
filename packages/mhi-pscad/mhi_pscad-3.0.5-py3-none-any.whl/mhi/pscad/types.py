#===============================================================================
# PSCAD Automation Library Types
#===============================================================================

"""
=========
Types
=========
"""


#===============================================================================
# Imports
#===============================================================================

from __future__ import annotations

from enum import IntEnum
from typing import Any, Dict, NamedTuple, Tuple, Union
from math import sqrt


#===============================================================================
# Ports
#===============================================================================

class NodeType(IntEnum):
    """
    Node Input/Output/Electrical Type
    """

    UNKNOWN = 0
    INPUT = 1
    OUTPUT = 2
    ELECTRICAL = 3
    SHORT = 4

class Electrical(IntEnum):
    """
    Electrical Node Types
    """

    FIXED = 0
    REMOVABLE = 1
    SWITCHED = 2
    GROUND = 3

class Signal(IntEnum):
    """
    Data Signal Types
    """

    ELECTRICAL = 0
    LOGICAL = 1
    INTEGER = 2
    REAL = 3
    COMPLEX = 4
    UNKNOWN = 15

class Point(NamedTuple):
    """
    Point class that supports Euclidean distance calculation.

    Examples
    ---------
        >>> Point(10, 20) + Point(5, 7)
        Point(x=15, y=27)

        It also works with tuple coordinates.

        >>> p = Point(4, 6) - (2, 3)
        >>> p.x, p.y
        (2, 3)


    .. versionchanged:: 2.9.6
        Now support addition, substraction, and calculation of Euclidian
        distance between points.
    """

    x: int
    y: int

    def __add__(self, other) -> Point:
        x, y = other
        return Point(self.x + x, self.y + y)

    def __sub__(self, other) -> Point:
        x, y = other
        return Point(self.x - x, self.y - y)

    def distance(self, other: Union[Tuple[int, int], 'Point']) -> float:
        """
        Measures the Euclidean distance to a given point.

        Parameters
        ----------
        other: Union[Tuple[int, int], Point]
            The point to which the Euclidean distance is measured.

        Returns
        -------
        float
            Euclidean Distance


        Examples
        --------
            >>> p1 = Point(10, 10)
            >>> p2 = Point(13, 14)
            >>> p1.distance(p2)
            5.0

        .. versionadded:: 2.9.6
        """

        x, y = other
        return sqrt((self.x - x) ** 2 + (self.y - y) ** 2)


class Port(NamedTuple):
    """
    A named Port (input, output, or electrical connection) for a Component
    """

    x: int
    y: int
    name: str
    dim: int
    type: NodeType
    electrical: Electrical
    signal: Signal

    @property
    def location(self) -> Point:
        """
        Location of the Port.

        .. versionadded:: 3.0.2
        """

        return Point(self.x, self.y)


AnyPoint = Union[Point, Port, Tuple[int, int]]

# ==============================================================================
# Rect
# ==============================================================================

class Rect(NamedTuple):
    """
    A class to represent rectangles on the canvas that supports mid-point
    calculation.

    Examples
    ---------
        >>> rect = Rect(10, 10, 20, 20)
        >>> rect
        Rect(left=10, top=10, right=20, bottom=20)
        >>> rect.mid
        Point(x=15, y=15)

    .. versionadded:: 2.9.6
    """

    left: int
    top: int
    right: int
    bottom: int

    @classmethod
    def from_mid(
        cls, mid_point: Union[Tuple[int, int], Point], w: int, h: int
    ) -> Rect:
        """
        Initializes a rectangle given mid-point, width and height.
        For even ``w`` and/or ``h``, mid-point would not be exactly at the
        centre but closer to top left corner.

    Examples
    ---------
        >>> mid = (10, 10)
        >>> Rect.from_mid(mid, 6,4)
        Rect(left=8, top=9, right=13, bottom=12)

        """

        x, y = mid_point
        right = x + w // 2
        left = right - w + 1
        bottom = y + h // 2
        top = bottom - h + 1

        return cls(left, top, right, bottom)

    @property
    def width(self) -> int:
        """
        Width of the rectangle
        """
        return self.right - self.left + 1

    @property
    def height(self) -> int:
        """
        Height of the rectangle
        """
        return self.bottom - self.top + 1

    @property
    def mid(self) -> Point:
        """
        Returns the mid-point of rectangle. For even ``w`` and/or ``h``,
        mid-point would not be exactly at the centre but closer to top left corner.
        """
        x, y = (self.right + self.left) // 2, (self.bottom + self.top) // 2
        return Point(x, y)



#===============================================================================
# Graphics
#===============================================================================

class Align(IntEnum):
    """
    Text Alignment
    """

    LEFT = 0
    CENTER = 1
    RIGHT = 2

class Side(IntEnum):
    """
    Annotation Side
    """

    NONE = 0
    LEFT = 1
    TOP = 2
    RIGHT = 3
    BOTTOM = 4
    AUTO = 5

class LineStyle(IntEnum):
    """
    Line Styles
    """

    SOLID = 0
    DASH = 1
    DOT = 2
    DASHDOT = 3

class FillStyle(IntEnum):
    """
    Fill Styles
    """

    HOLLOW = 0
    SOLID = 1
    BACKWARD_DIAGONAL = 2
    FORWARD_DIAGONAL = 3
    CROSS = 4
    DIAGONAL_CROSS = 5
    HORIZONTAL = 6
    VERTICAL = 7
    GRADIENT_HORZ = 8
    GRADIENT_VERT = 9
    GRADIENT_BACK_DIAG = 10
    GRADIENT_FORE_DIAG = 11
    GRADIENT_RADIAL = 12


#===============================================================================
# Parameters
#===============================================================================

Parameters = Dict[str, Any]


#===============================================================================
# Project Type, Message, LookIn
#===============================================================================

class ProjectType(IntEnum):
    """
    Project Types
    """

    CASE = 1
    LIBRARY = 2

Message = NamedTuple('Message', [('text', str),
                                 ('label', str),
                                 ('status', str),
                                 ('scope', str),
                                 ('name', str),
                                 ('link', int),
                                 ('group', int),
                                 ('classid', str)])


class LookIn(IntEnum):
    """
    Look In - for search
    """

    MODULE = 0
    PROJECT = 1
    WORKSPACE = 2
    WORKSPACE_NO_MASTER_LIBRARY = 3


#===============================================================================
# Definition Views
#===============================================================================

class View(IntEnum):
    """
    View Tabs
    """

    SCHEMATIC = 1
    CIRCUIT = 1
    FORTRAN = 2
    DATA = 3
    GRAPHIC = 4
    PARAMETERS = 5
    PARAMETER = 5
    SCRIPT = 6


#===============================================================================
# Components & Aliases
#===============================================================================

BUILTIN_COMPONENTS = frozenset((
    'Bus', 'TLine', 'Cable',
    'GraphFrame', 'PlotFrame', 'ControlFrame',
    'OverlayGraph', 'PolyGraph', 'Curve',
    'Button', 'Switch', 'Selector', 'Slider',
    'Oscilloscope', 'PhasorMeter', 'PolyMeter',
    'Sticky', 'Divider', 'GroupBox',
    'BookmarkCmp', 'FileCmp', 'CaseCmp', 'UrlCmp',
    'WireOrthogonal', 'WireDiagonal',
    ))

BUILTIN_COMPONENT_ALIAS = {
    'Wire': 'WireOrthogonal',
    'StickyWire': 'WireDiagonal',
    'Bookmark': 'BookmarkCmp',
    }

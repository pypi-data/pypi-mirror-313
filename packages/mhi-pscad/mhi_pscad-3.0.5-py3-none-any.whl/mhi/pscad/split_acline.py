# ==============================================================================
# Utilities for splitting AClines
# ==============================================================================
# pylint: disable=too-many-lines

"""
===========
AClineSplit
===========
"""
# .. versionadded:: 3.0.3

# ==============================================================================
# Imports
# ==============================================================================

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import cast, Dict, Optional, Tuple, TYPE_CHECKING, ClassVar

from .types import Point
from .unit import Value
from .wizard import UserDefnWizard

if TYPE_CHECKING:
    from .canvas import UserCanvas
    from .component import ACLine, Component
    from .definition import Definition
    from .project import Project


# ==============================================================================
# ACLine Split
# ==============================================================================

class SplitACLine(ABC):
    # pylint: disable=missing-function-docstring, missing-class-docstring,
    # pylint: disable=too-many-instance-attributes

    INTERFACE_NAME: ClassVar[str]
    # Constants:
    _PHASE_VIEW = 0
    _SINGLE_VIEW = 1

    def __init__(self, line: ACLine, dist_percent: float):
        self.line = line
        self.dist_percent = dist_percent
        self.line_name = self.line['Name']
        self.module_name = self.line_name + '_AB'
        self.end_type, self.dim = self.line['Mode'], self.line['Dim']
        self.org_vertices = self.line.vertices()
        self.main_canvas = self.line.parent

        wizard = self.create_wizard()
        left, mid, right = self.create_base_schematic(wizard)
        self.create_line_schematic(wizard, left, mid, right)

        self.defn = wizard.create_definition(
            self.line.project(), create_leads=False
        )
        self.main_canvas.create_component(
            self.defn,
            self.org_vertices[0].x,
            self.org_vertices[1].y,
            Name=self.module_name
        )
        self.canvas = cast('UserCanvas', self.defn.canvas())
        self.mid_x = self.canvas.size[0] // 2 - 2
        self.mid_y = self.canvas.size[1] // 2 - 2

    @abstractmethod
    def create_line_schematic(
            self, wizard: UserDefnWizard, left: Point, mid: Point, right: Point
    ) -> None:
        ...

    @abstractmethod
    def split(self) -> Dict[str, Point]:
        ...

    def create_base_schematic(
            self, wizard: UserDefnWizard
    ) -> Tuple[Point, Point, Point]:
        p1, p2, p3, p4 = self.org_vertices
        # To get locs relative to p1. p1 will be (0,0) on graphics canvas.
        p2 -= p1
        p3 -= p1
        p4 -= p1
        p1 = Point(0, 0)

        # Convert to pt units
        p2 = Point(p2.x * 18, p2.y * 18)
        p3 = Point(p3.x * 18, p3.y * 18)
        p4 = Point(p4.x * 18, p4.y * 18)

        grx = wizard.graphics

        grx.line(*p1, *p2)
        grx.line(*p2, *p3)
        grx.line(*p3, *p4)

        mid_x, mid_y = p2 + p3
        mid_x //= 2
        mid_y //= 2

        return p1, Point(mid_x, mid_y), p4

    def create_wizard(self) -> UserDefnWizard:
        wizard = UserDefnWizard(self.module_name, module=True)
        wizard.description = f"Split {self.line_name} module"

        return wizard

    def get_line_lengths(self) -> Tuple[Value, Value]:
        length_org = self.line['Length']
        length_a = length_org * (self.dist_percent / 100.0)
        length_b = length_org - length_a
        unit = length_org.units

        return Value(length_a, unit), Value(length_b, unit)

    @staticmethod
    def tidy_vertices(line: ACLine, horizontal: bool = False) -> None:
        x, y = line.endpoints()[0]
        if horizontal:
            tidy_vertices = ((x, y), (x + 2, y), (x + 4, y), (x + 6, y))
        else:
            tidy_vertices = ((x, y), (x + 2, y), (x + 4, y + 2), (x + 6, y + 2))

        line.vertices(*tidy_vertices)

    def create_line_pair(
            self, horizontal: bool, end_type: Optional[str] = None
    ) -> Tuple[ACLine, ACLine]:
        # pylint: disable = too-many-locals
        offset_x, offset_y = 10, 1
        if not end_type:
            end_type = self.end_type

        loc_a = Point(self.mid_x - offset_x, offset_y)
        loc_b = Point(self.mid_x + offset_x, offset_y)
        length_a, length_b = self.get_line_lengths()
        name_a, name_b = self.line_name + '_A', self.line_name + '_B'

        xml = self.line.definition.xml
        xml.set('name', name_a)
        defn_a = self.line.project().create_definition(xml)
        line_a = self.canvas.create_component(
            defn_a,
            loc_a.x,
            loc_a.y,
            Name=name_a,
            Length=length_a,
            Mode=end_type,
        )
        xml.set('name', name_b)
        defn_b = self.line.project().create_definition(xml)
        line_b = self.canvas.create_component(
            defn_b,
            loc_b.x,
            loc_b.y,
            Name=name_b,
            Length=length_b,
            Mode=end_type,
        )

        line_a = cast('ACLine', line_a)
        line_b = cast('ACLine', line_b)

        self.tidy_vertices(line_a, horizontal)
        self.tidy_vertices(line_b, horizontal)

        return line_a, line_b

    def calculate_interface_locs(self) -> Tuple[Point, Point]:
        x_a, x_b = self.mid_x - 2, self.mid_x + 8
        y = 5  # To account for line pair components above

        if self.INTERFACE_NAME == 'master:tline_interface':
            y += self.dim // 2 + 1
        else:
            y += 5

        return Point(x_a, y), Point(x_b, y)

    def get_org_intfc_pair(self) -> Tuple[Component, Component]:
        """Returns a and b original interfaces in that order"""
        intfcs = self.main_canvas.find_all(
            self.INTERFACE_NAME, Name=self.line_name
        )
        if len(intfcs) != 2:
            raise ValueError(f"Exactly 2 interfaces are required but "
                             f"{len(intfcs)} were found.")

        return intfcs[0], intfcs[1]

    def rename_org_intfc_pair(
            self, intfc_pair: Tuple[Component, Component]
    ) -> None:
        intfc_pair[0]['Name'] = self.line_name + '_A'
        intfc_pair[1]['Name'] = self.line_name + '_B'

    def create_intfc_pair(
            self, org_intfc_pair: Optional[Tuple[Component, Component]] = None
    ) -> Tuple[Component, Component]:

        intfc_a_loc, intfc_b_loc = self.calculate_interface_locs()
        intfc_a = self.canvas.create_component(
            self.INTERFACE_NAME, intfc_a_loc.x, intfc_a_loc.y
        )
        intfc_b = self.canvas.create_component(
            self.INTERFACE_NAME, intfc_b_loc.x, intfc_b_loc.y
        )

        if org_intfc_pair:
            # A receives original B parameters, B receives that of A's.
            intfc_a.parameters(parameters=org_intfc_pair[1].parameters())
            intfc_b.parameters(parameters=org_intfc_pair[0].parameters())

        # Only happens in case of local remote when dim is not 1 or 3.
        if self.end_type == 'LOCAL_CONNECTION':
            intfc_a['NC'] = self.dim
            intfc_b['NC'] = self.dim

        intfc_a['Name'] = self.line_name + '_A'
        intfc_a.mirror()
        intfc_b['Name'] = self.line_name + '_B'

        return intfc_a, intfc_b

    def create_schematic_endpoints(
            self, wizard: UserDefnWizard, left: Point, right: Point
    ) -> None:

        grx = wizard.graphics
        x, y = left
        grx.line(x, y, x + 4, y - 6, thickness=0)
        grx.line(x, y, x + 4, y + 6, thickness=0)
        x, y = right
        grx.line(x, y, x - 4, y - 6, thickness=0)
        grx.line(x, y, x - 4, y + 6, thickness=0)


# ==============================================================================
# SplitTLine
# ==============================================================================

class SplitTLine(SplitACLine):
    # pylint: disable=missing-function-docstring, missing-class-docstring,
    # too-many-instance-attributes

    INTERFACE_NAME = 'master:tline_interface'

    def create_line_schematic(
            self, wizard: UserDefnWizard, left: Point, mid: Point, right: Point
    ) -> None:
        grx = wizard.graphics
        x, y = mid
        # Create line schematic
        grx.line(x - 4, y + 11, x - 4, y - 11, thickness=1)
        grx.line(x - 6, y - 11, x + 6, y - 11, thickness=1)
        grx.line(x - 6, y - 13, x + 6, y - 13, thickness=0)
        grx.line(x + 4, y - 11, x + 4, y + 11, thickness=1)
        grx.line(x - 4, y - 4, x + 4, y + 4, thickness=0)
        grx.line(x - 4, y + 4, x + 4, y - 4, thickness=0)
        grx.text('%Name', x=x, y=y + 25)

        if self.end_type == 'REMOTE_ENDS':
            self.create_schematic_endpoints(wizard, left, right)

    def split(self) -> Dict[str, Point]:
        if self.end_type == 'LOCAL_CONNECTION':
            if self.dim in [1, 3]:
                line_a, line_b = self.create_line_pair(horizontal=True)
                left, mid, right = self.connect_lines(line_a, line_b)
                self.create_xnode_pair(left, right)
                connection_ports = {'N1': mid}

            else:
                _ = self.create_line_pair(
                    horizontal=False, end_type='REMOTE_ENDS'
                )
                intfc_a, intfc_b = self.create_intfc_pair()
                connection_ports = self.connect_intfc_pair(intfc_a, intfc_b)
                left, right = self.make_auxilary_intfcs()
                self.create_xnode_pair(left, right)

            self.add_schematic_ports()

        elif self.end_type == 'REMOTE_ENDS':
            _ = self.create_line_pair(horizontal=False)
            org_intfc_pair = self.get_org_intfc_pair()
            intfc_a, intfc_b = self.create_intfc_pair(org_intfc_pair)
            self.set_phase_view(intfc_a, intfc_b)
            connection_ports = self.connect_intfc_pair(intfc_a, intfc_b)
            self.rename_org_intfc_pair(org_intfc_pair)

        else:
            raise ValueError(
                "Only local connection and remote end types are supported."
            )

        self.line.delete()

        return connection_ports

    def connect_lines(self, line_a, line_b) -> Tuple[Point, Point, Point]:
        # line_a is on the left, line_b is on right
        x_offset = 3
        wire_a_end = line_a.vertices()[-1]
        wire_b_end = line_b.vertices()[0]
        self.canvas.create_wire(wire_a_end, wire_b_end)

        left = line_a.vertices()[0]
        mid = Point(self.mid_x + x_offset, left.y)
        right = line_b.vertices()[-1]

        return left, mid, right

    def set_phase_view(self, intfc_a, intfc_b) -> None:
        v = self._SINGLE_VIEW if self.dim in [1, 3] else self._PHASE_VIEW
        intfc_a['View'] = v
        intfc_b['View'] = v

    def connect_intfc_pair(self, intfc_a, intfc_b) -> Dict[str, Point]:
        x_offset = 3
        ports_a = [(p[0], p[1].location) for p in intfc_a.ports().items()]
        ports_a.sort(key=lambda p: p[1].y)
        ports_b = intfc_b.ports()

        connection_ports = {}
        counter = 1
        for name, p_a in ports_a:
            if name == 'send':
                p_b = ports_b['recv'].location
                name = 'B_TO_A'
                self.canvas.create_component(
                    'master:datalabel', *p_a, Name=name
                )
                self.canvas.create_component(
                    'master:datalabel', *p_b, Name=name
                )
                connection_ports[name] = p_a
            elif name == 'recv':
                p_b = ports_b['send'].location
                name = 'A_to_B'
                self.canvas.create_component(
                    'master:datalabel', *p_a, Name=name
                )
                self.canvas.create_component(
                    'master:datalabel', *p_b, Name=name
                )
                connection_ports[name] = p_a
            else:
                p_b = ports_b[name].location
                name = f'N{counter}'
                counter += 1
                self.canvas.create_wire(p_a, p_b)
                connection_ports[name] = Point(
                    self.mid_x + x_offset, p_b.y
                )

        return connection_ports

    def create_xnode_pair(self, p_a: Point, p_b: Point) -> None:
        self.canvas.create_component('master:xnode', *p_a, Name='A')
        self.canvas.create_component('master:xnode', *p_b, Name='B')

    def make_auxilary_intfcs(self) -> Tuple[Point, Point]:
        intfc_a_loc, intfc_b_loc = self.calculate_interface_locs()

        aux_a_loc = intfc_a_loc - (10, 0)
        aux_b_loc = intfc_b_loc + (10, 0)

        aux_a = self.canvas.create_component(  # pylint: disable=unused-variable
            self.INTERFACE_NAME,
            aux_a_loc.x,
            aux_a_loc.y,
            Name=self.line_name + '_A',
            NC=self.dim,
            View=self._SINGLE_VIEW,
        )
        aux_b = self.canvas.create_component(
            self.INTERFACE_NAME,
            aux_b_loc.x,
            aux_b_loc.y,
            Name=self.line_name + '_B',
            NC=self.dim,
            View=self._SINGLE_VIEW,
        )
        aux_b.mirror()

        return aux_a_loc - (1, 0), aux_b_loc + (1, 0)

    def add_schematic_ports(self):
        right_x, right_y = self.org_vertices[-1] - self.org_vertices[0]
        grx = self.defn.graphics()
        grx.add_electrical((0, 0), name='A', dim=self.dim)
        grx.add_electrical((right_x, right_y), name='B', dim=self.dim)


# ==============================================================================
# Cable Split
# ==============================================================================

class SplitCable(SplitACLine):
    # pylint: disable=missing-function-docstring, missing-class-docstring,
    # too-many-instance-attributes

    INTERFACE_NAME = 'master:cable_interface'

    def create_line_schematic(
            self, wizard: UserDefnWizard, left: Point, mid: Point, right: Point
    ) -> None:
        grx = wizard.graphics
        x, y = mid
        # Create line schematic
        grx.line(x + 8, y + 4, x + 8, y - 4, thickness=0)
        grx.line(x + 8, y - 4, x - 8, y, thickness=0)
        grx.line(x - 8, y, x + 8, y + 4, thickness=0)
        grx.line(x + 8, y - 6, x - 12, y, thickness=0, color='gray')
        grx.line(x - 12, y, x + 8, y + 6, thickness=0, color='gray')
        grx.text('%Name', x=x, y=y + 25)

        self.create_schematic_endpoints(wizard, left, right)

    def split(self) -> Dict[str, Point]:
        self.create_line_pair(horizontal=False)
        org_intfc_pair = self.get_org_intfc_pair()
        intfc_a, intfc_b = self.create_intfc_pair(org_intfc_pair)
        connection_ports = self.connect_intfc_pair(intfc_a, intfc_b)
        self.rename_org_intfc_pair(org_intfc_pair)

        self.line.delete()

        return connection_ports

    def connect_intfc_pair(self, intfc_a, intfc_b) -> Dict[str, Point]:
        x_offset = 3
        ports_a = intfc_a.ports()
        ports_b = intfc_b.ports()

        port_names = intfc_a.ports().keys()
        connection_ports = {}
        for name in port_names:
            p_a = ports_a[name].location
            if name == 'send':
                p_b = ports_b['recv'].location
                name = 'B_TO_A'
                self.canvas.create_component(
                    'master:datalabel', *p_a, Name=name
                )
                self.canvas.create_component(
                    'master:datalabel', *p_b, Name=name
                )
                connection_ports[name] = p_a

            elif name == 'recv':
                p_b = ports_b['send'].location
                name = 'A_TO_B'
                self.canvas.create_component(
                    'master:datalabel', *p_a, Name=name
                )
                self.canvas.create_component(
                    'master:datalabel', *p_b, Name=name
                )
                connection_ports[name] = p_a
            # Ground
            elif name == 'G':
                pass
            elif name[0] == 'S':
                p_b = ports_b[name].location
                self.canvas.create_wire(
                    p_a, p_a + (0, 1), p_b + (0, 1), p_b
                )
                connection_ports[name] = Point(
                    self.mid_x + x_offset, p_b.y + 1
                )

            elif name[0] == 'A':
                p_b = ports_b[name].location
                self.canvas.create_wire(
                    p_a, p_a + (0, 2), p_b + (0, 2), p_b
                )
                connection_ports[name] = Point(
                    self.mid_x + x_offset, p_b.y + 2)

            elif name[0] == 'O':
                p_b = ports_b[name].location
                self.canvas.create_wire(p_a, p_a + (0, 1))
                self.canvas.create_component(
                    'master:nodelabel', *(p_a + (0, 1)), Name=name
                )

                self.canvas.create_wire(p_b, p_b + (0, 1))
                self.canvas.create_component(
                    'master:nodelabel', *(p_b + (0, 1)), Name=name
                )
                connection_ports[name] = p_a + (0, 1)
            elif name[0] == 'G':
                p_b = ports_b[name].location
                self.canvas.create_component(
                    'master:nodelabel', *p_a, Name=name
                )
                self.canvas.create_component(
                    'master:nodelabel', *p_b, Name=name
                )
                connection_ports[name] = p_a
            else:
                p_b = ports_b[name].location
                self.canvas.create_wire(p_a, p_b)
                connection_ports[name] = Point(
                    self.mid_x + x_offset, p_b.y)

        return connection_ports

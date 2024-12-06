#===============================================================================
# PSCAD Settings Form Parser
#===============================================================================

"""
==========
Form Codec
==========
"""

#===============================================================================
# Imports
#===============================================================================

from __future__ import annotations

import re
import warnings

from typing import Any, Dict, List, Sequence, Tuple, Union
from warnings import warn
from xml.etree import ElementTree as ET

from mhi.common.codec import Codec, BooleanCodec, MapCodec
from mhi.common.colour import Colour

from .resource import RES_ID
from .unit import Value, ComplexValue, UnknownUnitError


#===============================================================================
# DefaultCodec
#===============================================================================

class DefaultCodec(Codec):
    """
    Codec for unknown parameter forms
    """

    def encode(self, value: Any) -> str:
        """
        Encode all values to strings for PSCAD.

        Booleans are encoded using lowercase.
        """

        if isinstance(value, bool):
            return "true" if value else "false"

        return str(value)


    def decode(self, value: str) -> Any:
        """
        'Indentity' decoder; all values are returned unchanged.
        """

        return value


    def range(self) -> Any:
        """
        Any value is accepted as input for encoding, and (theoretically)
        returned by decoding.
        """

        return Any


#===============================================================================
# Int Codec
#===============================================================================

class IntCodec(Codec):
    """
    Encode/Decode an integer
    """

    __slots__ = ('_range', '_variable')

    def __init__(self, minimum=-2**31, maximum=2**31-1, step=1,
                 variable=False):
        self._range = range(minimum, maximum + step, step)
        self._variable = variable

    def encode(self, value) -> str:
        """Encode integer to a string"""

        if isinstance(value, str):
            if self._variable and value.isidentifier():
                return value
            value = int(value)
        if value in self._range:
            return str(value)
        raise ValueError("Out of range")

    def decode(self, value: str) -> Union[str, int]:
        """Decode string to an integer (unless it is a variable identifier"""

        if self._variable and value.isidentifier():
            return value
        return int(value)

    def range(self) -> range:
        """Acceptable range of integer values"""

        return self._range

    def __repr__(self):
        return f"IntCodec({repr(self._range)[6:-1]}, {self._variable})"


class BitMaskCodec(IntCodec):
    """
    Encode/Decode a BitMask (Integer)
    """
    _CACHE: Dict[int,BitMaskCodec] = {}

    @classmethod
    def of(cls, num_bits):
        """Create a bitmask codec for the given number of bits"""
        if num_bits not in cls._CACHE:
            cls._CACHE[num_bits] = cls(num_bits)
        return cls._CACHE[num_bits]

    def __init__(self, bits):
        super().__init__(0, (1 << bits) - 1)

    def __repr__(self):
        return f"BitMaskCodec({(self._range.stop - 1).bit_length()})"


class Boolean01Codec(Codec):
    """
    Encode/Decode a boolean as a 1/0
    """

    def encode(self, value) -> str:

        flag = None
        if isinstance(value, bool):
            flag = value
        elif isinstance(value, str):
            if value.lower() in {"false", "no", "0"}:
                flag = False
            elif value.lower() in {"true", "yes", "1"}:
                flag = True
        elif isinstance(value, int):
            if value == 0:
                flag = False
            elif value == 1:
                flag = True

        if flag is None:
            raise ValueError(f"Not a boolean value: {value!r}")

        if not isinstance(value, bool):
            warn(f"Not a boolean value: {value!r}", stacklevel=6)

        return "1" if flag else "0"

    def decode(self, value: str) -> bool:
        return value != '0'

    def range(self):
        return False, True

    def __repr__(self):
        return "Boolean01Codec"


#===============================================================================
# Real Codec
#===============================================================================

class RealCodec(Codec):
    """
    Encode/Decode a float number, possibly with units
    """

    __slots__ = ('_min', '_max', '_units', '_variable')

    def __init__(self, minimum=-1E+308, maximum=+1E+308, units=None,
                 variable=False):
        self._min = minimum
        self._max = maximum
        self._units = units
        self._variable = variable

    def encode(self, value) -> str:
        try:
            if isinstance(value, str):
                if self._variable and value.isidentifier():
                    return value
                value = Value(value, self._units)
            if self._min <= value <= self._max:
                return str(value)

            raise ValueError("Out of range")

        except ValueError:
            return str(value)


    def decode(self, value: str) -> Union[Value, float, str]:
        if self._variable and value.isidentifier():
            return value
        try:
            if self._units:
                return Value(value, self._units)
            return float(value)
        except ValueError:
            return value
        except UnknownUnitError as uue:
            warnings.warn(str(uue), stacklevel=2)
            return value

    def range(self):
        return self._min, self._max

    def __repr__(self):
        if self._units is None:
            return f"RealCodec({self._min}, {self._max})"
        return f"RealCodec({self._min}, {self._max}, {self._units!r})"


#===============================================================================
# Complex Codec
#===============================================================================

class ComplexCodec(Codec):
    """
    Encode/Decode a complex number, possibly with units
    """

    __slots__ = ('_min', '_max')

    def __init__(self, minimum=-1E+308, maximum=+1E+308, units=None):
        self._min = minimum
        self._max = maximum
        self._units = units

    def encode(self, value) -> str:
        try:
            if isinstance(value, (complex, str)):
                value = ComplexValue(value, self._units)
            if (self._min <= value.real <= self._max and
                    self._min <= value.imag <= self._max):
                return str(value)

            raise ValueError("Out of range")

        except ValueError:
            return str(value)


    def decode(self, value: str) -> Union[ComplexValue, str]:
        try:
            return ComplexValue(value, self._units)
        except ValueError:
            return value
        except UnknownUnitError as uue:
            warnings.warn(f"Unknown unit {uue!r}", stacklevel=2)
            return value

    def range(self):
        return self._min, self._max

    def __repr__(self):
        if self._units is None:
            return f"ComplexCodec({self._min}, {self._max})"
        return f"ComplexCodec({self._min}, {self._max}, {self._units!r})"


#===============================================================================
# String Codec
#===============================================================================

class StringCodec(Codec):
    """
    Strings encode & decode as themselves
    """

    def encode(self, value) -> str:
        """Encode a string as a string"""

        return str(value)

    def decode(self, value: str) -> str:
        """Decode a string as a string"""

        return value

    def range(self) -> None:
        """No valid range"""

        return None

    def __repr__(self):

        return "StringCodec()"


#===============================================================================
# Table Codec
#===============================================================================

class TableCodec(Codec):
    """
    Strings encode & decode as themselves
    """

    def encode(self, value) -> str:
        """Encode a table into a string"""

        table = value

        if len(table) < 1:
            raise ValueError("Table requires at least 1 row")
        columns = len(table[0])
        if columns < 1:
            raise ValueError("Table requires at least 1 column")
        if any(len(row) != columns for row in table):
            raise ValueError("Table must be rectangular")

        for row in table:
            for val in row:
                if not isinstance(val, (int, float)):
                    try:
                        float(val)
                    except ValueError:
                        raise ValueError(f"Invalid value: {val!r}") from None

        return "\n".join(",".join(map(str, row)) for row in table)

    def decode(self, value: str) -> List[List[Union[int, float, str]]]:
        """Decode a table from a string"""

        def int_float(val) -> Union[int, float, str]:
            try:
                return int(val)
            except ValueError:
                pass

            try:
                return float(val)
            except ValueError:
                return val

        return [list(map(int_float, row.split(",")))
                for row in value.split("\n") if row]

    def __repr__(self):

        return "TableCodec()"

    def range(self) -> None:
        """No valid range"""

        return None



#===============================================================================
# ParameterCodec
#===============================================================================

class ParameterCodec:
    """
    PSCAD Parameter Coder-Decoders
    """

    DEFAULT: ParameterCodec


    def __init__(self, coding):

        self._coding = coding


    def encode(self, parameters):
        """
        Encode key-value dictionaries with Human-Readable/Pythonic values into
        key-value dictionaries with strings values used to serialize
        data in PSCAD's XML file formats.

        The dictionary keys are used to select the encoding method.
        """

        return {key: self._encode(key, val) for key, val in parameters.items()}


    def decode(self, parameters):
        """
        Decode key-value dictionaries string values used to serialize
        data in PSCAD's XML file format into dictionaries with
        Human-Readable/Pythonic values

        The dictionary keys are used to select the encoding method.
        """

        if parameters is None:
            return None

        return {key: self._decode(key, val)
                for key, val in parameters.items() if key in self._coding}


    def _encode(self, key, val):

        codec = self._coding.get(key, None)
        if codec:
            try:
                return codec.encode(val)
            except (KeyError, ValueError):
                msg = f"{key}: cannot be assigned {val!r}"
                raise ValueError(msg) from None

        raise ValueError(f"No such parameter: {key}")

    def _decode(self, key, val):

        codec = self._coding.get(key, None)
        if codec:
            try:
                return codec.decode(val)
            except (KeyError, ValueError) as err:
                return err

        raise ValueError(f"No such parameter: {key}")


    def range(self, key: str) -> Any:
        """
        Valid input for a given parameter
        """

        return self._coding[key].range()


    def __repr__(self):

        if self is ParameterCodec.DEFAULT:
            return "ParameterCodec[*]"

        params = ", ".join(f"{key}:{val.__class__.__name__.replace('Codec', '')}"
                           for key, val in self._coding.items())
        return f"{self.__class__.__name__}[{params}]"


class _DefaultCodecMap(dict):
    """
    A dictionary-ish class that returns DefaultCodec (singleton) for every key.
    """

    _default = DefaultCodec()

    def __missing_key__(self, key):            # pylint: disable=unused-argument
        return self._default


ParameterCodec.DEFAULT = ParameterCodec(_DefaultCodecMap())


#===============================================================================
# Form Parser
#===============================================================================

# Global, dataless, stateless parsers
_boolean_codec = BooleanCodec()
_boolean01_codec = Boolean01Codec()
_string_codec = StringCodec()
_table_codec = TableCodec()
_colour_codec = Colour()
_yes_no = MapCodec({'YES': '1', 'NO': '0'},
                   extras={'0': (False, 0), '1': (True, 1)})
_line_style_codec = MapCodec({'SOLID': '0', 'DASH': '1', 'DOT': '2',
                              'DASHDOT': '3'})
_fill_style_codec = MapCodec({'HOLLOW': '0', 'SOLID': '1',
                              'BACKWARD_DIAGONAL': '2', 'FORWARD_DIAGONAL': '3',
                              'CROSS': '4', 'DIAGONAL_CROSS': '5',
                              'HORIZONTAL': '6', 'VERTICAL': '7',
                              'GRADIENT_HORZ': '8', 'GRADIENT_VERT': '9',
                              'GRADIENT_BACK_DIAG': '10',
                              'GRADIENT_FORE_DIAG': '11',
                              'GRADIENT_RADIAL': '12',
                              })

def cleanup_choices(choices: List[str]) -> Dict[str, str]: # pylint: disable=missing-function-docstring

    def remove_word(key: Sequence[str], word: str) -> Tuple[str, ...]:
        return tuple(term for term in key if term != word)

    def remove_redundant(keys: List[Tuple[str, ...]], *words: str):
        size = len(keys)

        for word in words:
            new_keys = [remove_word(key, word) for key in keys]
            if len(set(new_keys)) == size:
                keys[:] = new_keys

    def remove_common_words(keys: List[Tuple[str, ...]]):
        # Don't remove any words if all words are common,
        # or if some key is a reordering of words of another key:
        # eg) "INDEX_PATH_VALUE_UNIT" -vs- "INDEX_VALUE_UNIT_PATH"
        if len(set(map(frozenset, keys))) < len(keys):  # type: ignore
            return

        common_words = set(keys[0])
        for key in keys[1:]:
            common_words &= set(key)

        if common_words:
            size = len(keys)

            for word in common_words:
                new_keys = [remove_word(key, word) for key in keys]
                shortest_key = min(sum(len(term) for term in key)
                                   for key in new_keys)
                if shortest_key > 4:
                    if len(set(new_keys)) == size:
                        keys[:] = new_keys

    def simplify(keys: List[str], *funcs):
        size = len(keys)

        for func in funcs:
            new_keys = [func(key) for key in keys]
            if len(set(new_keys)) == size:
                keys[:] = new_keys

    def defaults(key: str) -> str:
        match = re.search(r"\((.+\))", key)
        return match.group(1) if match else key

    keys = []
    values = []

    for choice in choices:
        val, key = choice.split("=", 1)
        key = key.strip().upper().replace(" (DEFAULT)", "")
        keys.append(key)
        values.append(val.strip())

    if len(keys) > 0:
        simplify(keys, defaults)

        keys = [key.replace("+VE", "POS") for key in keys]
        keys = [key.replace("-VE", "NEG") for key in keys]
        keys = [re.sub("[-()+.']", "", key) for key in keys]
        key_lists = [tuple(re.split("[^0-9A-Z%]+", key)) for key in keys]

        remove_redundant(key_lists, "A", "IS", "THE", "WITH", "GENERATE",
                         "USE", "CREATE")
        remove_common_words(key_lists)
        keys = ["_".join(key_list) for key_list in key_lists]

    return dict(zip(keys, values))


def _form_parse(codecs, root):

    def parse_choice(param):
        return cleanup_choices(choice.text for choice in param.iter('choice'))

    def boolean(param):                        # pylint: disable=unused-argument
        return _boolean_codec

    def bit(param):
        name = param.get('name')
        limit = 2 ** int(param.get('index'))
        codec = codecs.get(name, None)
        if not codec:
            codec = IntCodec(0, limit-1)
        elif limit > codec._range.stop:
            codec._range = range(0, limit)
        return codec

    def integer(param):
        minimum = param.get('min')
        maximum = param.get('max')
        content_type = param.get('content_type', '')
        minimum = int(minimum) if minimum else -2**31
        maximum = int(maximum) if maximum else 2**31 - 1
        allow_variable_name = content_type in ('Constant', 'Variable')

        return IntCodec(minimum, maximum, variable=allow_variable_name)

    def line_style(param): # pylint: disable=unused-argument
        return _line_style_codec

    def fill_style(param): # pylint: disable=unused-argument
        return _fill_style_codec

    def choice(param):
        choices = parse_choice(param)
        if len(choices) < 2:
            return _string_codec
        if len(choices) == 2:
            if choices == {'TRUE': 'true', 'FALSE': 'false'}:
                return _boolean_codec
            if choices == {'YES': '1', 'NO': '0'}:
                return _yes_no
            if 'NOT_DISPLAYED' in choices:
                return _boolean_codec
        return MapCodec(choices)

    def real(param):
        minimum = float(param.get('min') or '-inf')
        maximum = float(param.get('max') or '+inf')
        unit = param.get('unit')
        content_type = param.get('content_type', '')
        allow_variable_name = content_type in ('Constant', 'Variable')

        return RealCodec(minimum, maximum, unit, variable=allow_variable_name)

    def cmplx(param):
        minimum = float(param.get('min') or "-inf")
        maximum = float(param.get('max') or "+inf")
        unit = param.get('unit')
        return ComplexCodec(minimum, maximum, unit)

    def text(param): # pylint: disable=unused-argument
        return _string_codec

    def colour(param): # pylint: disable=unused-argument
        return _colour_codec

    def table(param): # pylint: disable=unused-argument
        return _table_codec

    codec = {
        'Boolean': boolean,
        'Bit': bit,
        'Integer': integer,
        'LineStyle': line_style,
        'FillStyle': fill_style,
        'Choice': choice,
        'Color': colour,
        'Real': real,
        'Complex': cmplx,
        'Text': text,
        'Password': text,
        'Filename': text,
        'MultiFile': text,
        'RelativePath': text,
        'Table': table,
        }

    # Not supported types: Default to 'text':
    #   Logical,Foldername, Font, LargeText,
    #   TextComboEx, RealComboEx, IntegerComboEx, LogicalComboEx,
    #   InnerText, InnerMText, AttrDrawingPoint, AttrDrawingSize

    def _parse_parameter(param):
        name = param.get('name')
        kind = param.get('type')

        codecs[name] = codec.get(kind, text)(param)

    if root.tag == 'form':
        for param in root.findall('category/parameter'):
            _parse_parameter(param)
    elif root.tag == 'category':
        for param in root.findall('parameter'):
            _parse_parameter(param)


#===============================================================================
# Form Codec
#===============================================================================

class FormCodec(ParameterCodec):
    """
    Form Parameter Coder/Decoder
    """

    _cache: Dict[str, FormCodec] = {}

    @staticmethod
    def application(remote):        # pylint: disable=missing-function-docstring
        codec = FormCodec._load(remote, 'IDR_{}_SETTINGS_FORM',
                                'GRAPHICS', 'LICENSE')
        codec._coding['cl_use_advanced'] = _boolean01_codec
        return codec

    @staticmethod
    def project(remote):            # pylint: disable=missing-function-docstring
        codec = FormCodec._load(remote, 'IDR_{}_OPTIONS', 'COMPILER')
        coding = codec._coding

        for name in ('startup_filename', 'output_filename', 'snapshot_filename',
                     'description', 'labels', 'Preprocessor'):
            coding[name] = _string_codec

        coding['Advanced'] = BitMaskCodec.of(14)
        coding['Build'] = BitMaskCodec.of(5)
        coding['Check'] = BitMaskCodec.of(4)
        coding['Debug'] = BitMaskCodec.of(3)
        coding['Options'] = BitMaskCodec.of(6)
        coding['Warn'] = BitMaskCodec.of(3)

        coding['Mruns'] = IntCodec(minimum=1)
        coding['sparsity_threshold'] = IntCodec(minimum=1)

        coding['branch_threshold'] = RealCodec()
        coding['chatter_threshold'] = RealCodec()
        coding['SnapTime'] = RealCodec(0.0, 1e100, '')
        coding['time_duration'] = RealCodec(1e-100, 1e100, '')
        coding['time_step'] = RealCodec(1e-100, 1e100, '')
        coding['sample_step'] = RealCodec(1e-100, 1e100, '')

        coding['PlotType'] = MapCodec({'NONE': '0', 'OUT': '1', 'PSOUT': '2'},
                                      extras={'0': ('NO',), '1': ('LEGACY',),
                                              '2': ('ADVANCED',)})
        coding['StartType'] = MapCodec({'STANDARD': '0', 'FROM_SNAP_FILE': '1'})
        coding['SnapType'] = MapCodec({'NONE': '0', 'ONLY_ONCE': '1',
                                       'INCREMENTAL_SAME_FILE': '2',
                                       'INCREMENTAL_MANY_FILES': '3'})
        coding['MrunType'] = MapCodec({'STANDALONE': '0', 'MASTER': '1',
                                      'SLAVE': '2'})


        return codec

    @staticmethod
    def bus(remote):                # pylint: disable=missing-function-docstring
        return FormCodec._load(remote, 'IDR_{}_PARAMETERS', 'BUS')

    @classmethod
    def layer_options(cls, remote): # pylint: disable=missing-function-docstring
        return cls._fetch(remote, 'layer_options',
                          'IDR_LAYER_OPTIONS')

    @classmethod
    def user_canvas(cls, remote):   # pylint: disable=missing-function-docstring
        codec = cls._fetch(remote, 'user_canvas',
                          'IDR_SCHEMATIC_FORM')
        coding = codec._coding
        for name in ('show_signal', 'show_virtual', 'show_sequence',
                     'auto_sequence', 'monitor_bus_voltage', 'show_grid',
                     'show_border', 'show_terminals'):
            coding[name] = _boolean01_codec

        return codec

    @classmethod
    def group_box(cls, remote): # pylint: disable=missing-function-docstring
        return cls._fetch(remote, 'group_box',
                          'IDR_GROUPBOX_FORM')

    @classmethod
    def sticky_note(cls, remote):   # pylint: disable=missing-function-docstring
        codec = cls._fetch(remote, 'sticky_note',
                           'IDR_STICKY_SETTINGS_FORM')
        if 'arrows' not in codec._coding:
            codec._coding['arrows'] = IntCodec(0, 255)
        return codec

    @classmethod
    def divider(cls, remote):       # pylint: disable=missing-function-docstring
        return cls._fetch(remote, 'divider',
                          'IDR_DIVIDER_SETTINGS')

    @classmethod
    def graph_frame(cls, remote):   # pylint: disable=missing-function-docstring
        return cls._fetch(remote, 'graph_frame',
                          'IDR_GRAPHFRAME_SETTINGS_FORM')

    @classmethod
    def plot_frame(cls, remote):    # pylint: disable=missing-function-docstring
        return cls._fetch(remote, 'plot_frame',
                          'IDR_PLOTFRAME_SETTINGS_FORM')

    @classmethod
    def overlay_graph(cls, remote): # pylint: disable=missing-function-docstring
        return cls._fetch(remote, 'overlay_graph',
                          'IDR_OVERLAYGRAPH_SETTINGS_FORM')

    @classmethod
    def simulation_set(cls, remote): # pylint: disable=missing-function-docstring
        return cls._fetch(remote, 'simulation_set',
                          'IDR_SIMULATION_SETTINGS_FORM')

    @classmethod
    def simset_project_task(cls, remote): # pylint: disable=missing-function-docstring
        return cls._fetch(remote, 'simset_project_task',
                          'IDR_SIMULATION_FORM')

    @classmethod
    def simset_project_overrides(cls, remote): # pylint: disable=missing-function-docstring
        return cls._fetch(remote, 'simset_project_overrides',
                          'IDR_SIMULATIONSET_PROJECTOVERRIDES')

    @classmethod
    def simset_external_task(cls, remote): # pylint: disable=missing-function-docstring
        return cls._fetch(remote, 'simset_external_task',
                          'IDR_EXTERNALSIM_SETTINGS_FORM')

    @classmethod
    def gfx_text(cls, remote):      # pylint: disable=missing-function-docstring
        return cls._fetch(remote, 'gfx_text', 'IDR_GRAPHICS_LABEL_FORM')

    @classmethod
    def gfx_line(cls, remote):      # pylint: disable=missing-function-docstring
        return cls._fetch(remote, 'gfx_line', 'IDR_GRAPHICS_LINE_FORM')

    @classmethod
    def gfx_rect(cls, remote):      # pylint: disable=missing-function-docstring
        return cls._fetch(remote, 'gfx_rect', 'IDR_GRAPHICS_BOX_FORM')

    @classmethod
    def gfx_oval(cls, remote):      # pylint: disable=missing-function-docstring
        return cls._fetch(remote, 'gfx_oval', 'IDR_GRAPHICS_OVAL_FORM')

    @classmethod
    def gfx_arc(cls, remote):       # pylint: disable=missing-function-docstring
        return cls._fetch(remote, 'gfx_arc', 'IDR_GRAPHICS_ARC_FORM')

    @classmethod
    def gfx_port(cls, remote):      # pylint: disable=missing-function-docstring
        return cls._fetch(remote, 'gfx_port', 'IDR_GRAPHICS_PORT_FORM')

    @classmethod
    def gfx_shape(cls, remote):     # pylint: disable=missing-function-docstring
        return cls._fetch(remote, 'gfx_shape', 'IDR_GRAPHICS_PATHEX_FORM')

    @classmethod
    def _fetch(cls, remote, key, *args, fmt=None):

        if key not in cls._cache:

            if fmt:
                args = [fmt.format(arg) for arg in args]

            xml = [remote._pscad._xml(RES_ID[arg]) for arg in args]
            codec = cls(*xml)
            cls._cache[key] = codec

        return cls._cache[key]

    @staticmethod
    def _load(remote, fmt, *args):

        xml_parts = []

        for iid in args:
            name = fmt.format(iid)
            try:
                res_id = RES_ID[name]
                xml = remote._pscad._xml(res_id)
                xml_parts.append(xml)
            except ValueError:
                # Not every PSCAD version supports every code used
                # in the Automation Library
                pass

        return FormCodec(*xml_parts)


    #==========================================================================
    # Constructor
    #==========================================================================

    def __init__(self, *args):

        coding = {}

        for xml in args:
            form = ET.fromstring(xml) if isinstance(xml, str) else xml
            _form_parse(coding, form)

        super().__init__(coding)

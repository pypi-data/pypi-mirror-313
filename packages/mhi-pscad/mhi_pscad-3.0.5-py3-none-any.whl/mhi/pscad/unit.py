#===============================================================================
# Unit Conversion
#===============================================================================

"""
The Unit Conversion
"""

#===============================================================================
# Imports
#===============================================================================

import re
from xml.etree import ElementTree as ET
from collections import namedtuple
from typing import Dict


#===============================================================================
# Unknown Unit Error
#===============================================================================

class UnknownUnitError(KeyError):
    """
    Unknown Unit exception
    """

#===============================================================================
# Unit System
#===============================================================================

class UnitSystem:
    """
    The system of units to use for conversions.

    The individual units which are supported must be provided externally,
    such as via XML to the :meth:`.UnitSystem.parse` method.

    SI prefixes from Yotta (:math:`10^{24}`) to Yocto (:math:`10^{-24}`) are supported.
    Additionally, both "da" and "D" may be used to indicate "Deka" (:math:`10^{1}`),
    and both "µ" and "u" may be used to indicated "micro" (:math:`10^{-6}`).
    """

    Unit = namedtuple("Unit", "symbol, base, factor, alias, inverse")

    Prefix = {prefix: 10.0 ** int(exp)
              for prefix, exp in (pair.split(':') for pair in (
                  "y:-24,z:-21,a:-18,p:-15,f:-12,n:-9,µ:-6,m:-3,c:-2,d:-1,"
                  "da:1,h:2,k:3,M:6,G:9,T:12,P:15,E:18,Z:21,Y:24,"
                  "D:1,u:-6").split(","))}

    _unit: Dict[str, Unit] = {}

    @classmethod
    def parse(cls, xml):
        """
        Extract units from an XML string of the form::

            <unit_system>
              <Domain>
                <Unit symbol="V" base="V" alias="" inverse="" multiplier="1.0" />
                <Unit symbol="A" base="A" alias="" inverse="" multiplier="1.0" />
                ...
              </Domain>
              <Domain> ... </Domain>
              ...
            </unit_system>
        """

        root = ET.fromstring(xml)

        for unit in root.findall('Domain/Unit'):
            cls._add_unit(unit)

    @classmethod
    def _add_unit(cls, unit):

        symbol = unit.get('symbol')
        base = unit.get('base')
        factor = float(unit.get('multiplier'))
        alias = unit.get('alias')
        inverse = unit.get('inverse')

        cls._unit[symbol] = cls.Unit(symbol, base, factor, alias, inverse)

    @classmethod
    def _get_unit_factor(cls, name):
        if not name or name == "1":
            return 1

        unit = cls._unit.get(name)
        if unit:
            return unit.factor

        if len(name) >= 2:
            prefix = cls.Prefix.get(name[:1])
            unit = cls._unit.get(name[1:])
            if prefix and unit:
                return unit.factor / prefix

        if len(name) >= 3:
            prefix = cls.Prefix.get(name[:2])
            unit = cls._unit.get(name[2:])
            if prefix and unit:
                return unit.factor / prefix

        raise UnknownUnitError(name)

    @classmethod
    def _get_units_factor(cls, units):
        factor = 1
        if units:
            for unit in units.split("*"):
                factor *= cls._get_unit_factor(unit)
        return factor

    @classmethod
    def _get_units_ratio(cls, units):
        try:
            if units and "/" in units:
                top, btm = units.split("/", 1)
                return cls._get_units_factor(top) / cls._get_units_factor(btm)
            return cls._get_units_factor(units)
        except UnknownUnitError as uue:
            raise UnknownUnitError(f"Unknown unit {uue!s} in {units!r}"
                                   ) from None

    @classmethod
    def convert(cls, from_value, from_units, to_units):
        """
        Convert a value from one unit into a different unit.

        With appropriate unit definitions:

            >>> UnitSystem.convert(100, "km/hr", "mi/hr")
            62.1371192237334


        If a unit is not recognized, Not-a-Number is returned.

        The result will be nonsensical if the unit dimensions do not agree.
        Converting "km" to "min" will result in multiplication by 16.67,
        since "km" is 1000 "m" base units, and "min" is 60 "s" base units,
        this the conversion multiplies by 1000 then divides by 60.
        """

        if from_units == to_units:
            return from_value

        from_factor = cls._get_units_ratio(from_units)
        to_factor = cls._get_units_ratio(to_units)

        return from_value / from_factor * to_factor



#===============================================================================
# Value
#===============================================================================

class Value(float):
    """
    A floating point value, with units.

    A parameter typically has a unit associated with it, such as "km".
    The user may enter the parameter value with their own units,
    such as "100.0 [mi]".
    A `Value` holds the text which has been entered for the parameter,
    but when used in calculations, it will reflect the numerical value
    converted to the parameter's expected units, ie ``160.9344``.

    The value's unit does not propogate through calculations;
    to attach units to the calculated value, create a new ``Value``.

    Example:

        >>> user_input = "100.0 [mi]"
        >>> parameter_units = "km"
        >>> length = Value(user_input, parameter_units)
        >>> length.real
        160.9344
        >>> length * 2
        321.8688
        >>> str(length)
        '100.0 [mi]'
        >>> double_length = Value(length * 2, "km")
        >>> str(double_length)
        '321.8688 [km]'
    """

    __slots__ = ('_original', '_units', '_str')

    _FORMAT = re.compile(r"(.*?)(?:\s*\[(.+)]\s*)?")

    def __new__(cls, value, units=None):

        if isinstance(value, Value):
            val = value.real
            val_units = value.units
            text = value.normalized()
        elif isinstance(value, (float, int)):
            val = float(value)
            val_units = units
            if units:
                text = f"{value} [{units}]"
            else:
                text = str(val)
        elif isinstance(value, str):
            text = value
            val, val_units = cls._FORMAT.fullmatch(text).group(1, 2)
            val = float(val)
        else:
            raise ValueError(f"Unexpected value: {value!r}")

        try:
            if units and val_units:
                value = UnitSystem.convert(val, val_units, units)
            else:
                value = val
        except ValueError:
            value = float("nan")

        self = super().__new__(cls, value)

        self._original = (val, val_units)
        self._units = units
        self._str = text

        return self

    #---------------------------------------------------------------------------
    # Representations
    #---------------------------------------------------------------------------

    def __str__(self):
        return self._str

    def __repr__(self):
        return f"Value({self._str!r})"

    def normalized(self, fmt: str = "f") -> str:
        """
        Return the converted value as a string, along with the expected units.

        Parameters
        ----------
        fmt: str
            a format specifier, such as ``'.2f'`` (optional)

        Returns
        -------
        str
            The converted value.
        """

        val = (f"{{:{fmt}}}").format(self.real)
        if self.units:
            val += f" [{self.units}]"

        return val


    #---------------------------------------------------------------------------
    # units
    #---------------------------------------------------------------------------

    @property
    def units(self) -> str:
        """
        The units this value is expressed in.
        """

        return self._units                                        # type: ignore


#===============================================================================
# Value
#===============================================================================

class ComplexValue(complex):
    """
    A complex value, with units.

    A parameter typically has a unit associated with it, such as "km".
    The user may enter the parameter value with their own units,
    such as "(100.0, -12.0) [kV]".
    A `Value` holds the text which has been entered for the parameter,
    but when used in calculations, it will reflect the numerical value
    converted to the parameter's expected units.

    The value's unit does not propogate through calculations;
    to attach units to the calculated value, create a new ``ComplexValue``.

    Example:

        >>> user_input = "(1.0, -0.012) [kV]"
        >>> parameter_units = "V"
        >>> voltage = ComplexValue(user_input, parameter_units)
        >>> voltage.real
        1000.0
        >>> voltage.imag
        -12.0
        >>> voltage * 2
        (2000-24j)
        >>> str(voltage)
        '(1.0, -0.012) [kV]'
        >>> double_voltage = ComplexValue(voltage * 2, "V")
        >>> str(double_voltage)
        '(2000.0, -24.0) [V]'
    """

    __slots__ = ('_original', '_units', '_str')

    _FORMAT = re.compile(r"\(?(.*?)(?:\s*,(.*?))?\)?(?:\s*\[(.+)]\s*)?")

    def __new__(cls, value, units=None):

        if isinstance(value, Value):
            val = value.real
            val_units = value.units
            text = value.normalized()
        elif isinstance(value, ComplexValue):
            val = complex(value)
            val_units = value.units
            text = value.normalized()
        elif isinstance(value, (complex, float, int)):
            val = complex(value)
            val_units = units
            if units:
                text = f"{(value.real, value.imag)} [{units}]"
            else:
                text = str((value.real, value.imag))
        elif isinstance(value, str):
            text = value
            real, imag, val_units = cls._FORMAT.fullmatch(text).group(1, 2, 3)
            val = complex(float(real), float(imag))
        else:
            raise ValueError(f"Unexpected value: {value!r}")

        try:
            if units and val_units:
                value = UnitSystem.convert(val, val_units, units)
            else:
                value = val
        except ValueError:
            nan = float("nan")
            value = complex(nan, nan)

        self = super().__new__(cls, value)

        self._original = (val, val_units)
        self._units = units
        self._str = text

        return self

    #---------------------------------------------------------------------------
    # Representations
    #---------------------------------------------------------------------------

    def __str__(self):
        return self._str

    def __repr__(self):
        return f"ComplexValue({self._str!r})"

    def normalized(self, fmt: str = "f") -> str:
        """
        Return the converted value as a string, along with the expected units.

        Parameters
        ----------
        fmt: str
            a format specifier, such as ``'.2f'`` (optional)

        Returns
        -------
        str
            The converted value.
        """

        val = (f"({{:{fmt}}}, {{:{fmt}}})").format(self.real, self.imag)
        if self.units:
            val += f" [{self.units}]"

        return val


    #---------------------------------------------------------------------------
    # units
    #---------------------------------------------------------------------------

    @property
    def units(self) -> str:
        """
        The units this value is expressed in.
        """

        return self._units                                        # type: ignore

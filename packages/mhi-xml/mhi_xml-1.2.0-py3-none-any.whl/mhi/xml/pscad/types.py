"""
=====
Types
=====
"""

#===============================================================================
# Imports
#===============================================================================

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Flag
from typing import Any, NamedTuple


from mhi.xml.types import ParamEnum


#===============================================================================
# Exports
#===============================================================================

__all__ = ['IntBool', 'Choice', 'UnitValue',
           'ResourceType',
           'NodeType', 'SignalType', 'ElectricalType',
           'BusType',
           'Align', 'LineStyle', 'FillStyle',
           'Point',
           'XY', 'UP', 'DOWN', 'LEFT', 'RIGHT',
           'Arrows',
           ]


#===============================================================================
# PSCAD Booleans
#===============================================================================

TRUES = frozenset({True, 'TRUE', 'True', 'true', '1'})
FALSES = frozenset({False, 'FALSE', 'False', 'false', '0'})

class IntBool:
    """
    Representation of 'Boolean' values in a PSCAD parameter ('1' or '0')
    """

    def __new__(cls, value):

        if value in TRUES:
            return True
        if value in FALSES:
            return False
        raise ValueError(f"Expected '1' or '0', got {value!r}")

    @staticmethod
    def encode_to_str(value):
        """
        Encode the given (boolean) value to the PSCAD parameter ('1' or '0')
        """

        return str(int(value))


#===============================================================================
# Choices
#===============================================================================

class Choice:
    """
    Representation of 'Choice' values in a PSCAD parameter
    """


    @classmethod
    def enum(cls, *values, start: int = 0):
        """
        Convert a list of values into an 'enumeration', by assigning
        each to a sequencial integer value
        """

        choices = {str(idx): value for idx, value in enumerate(values, start)}
        return cls(choices)

    @classmethod
    def ints(cls, *values):
        """
        Convert a list of integers into a PSCAD Choice parameter',
        by assigning each one to its string representation.
        """

        choices = {str(value): value for value in values}
        return cls(choices)

    def __init__(self, choices: dict[str, Any]):
        self._decode = choices
        self._encode = {v: k for k, v in choices.items()}

    def __call__(self, value: str):
        return self._decode[value]

    def encode_to_str(self, value: Any) -> str:
        """
        Encode the given choice value to the PSCAD parameter string
        """

        if value not in self._encode:
            valid = ', '.join(map(repr, self._encode))
            raise ValueError(f"Invalid value for parameter: {value!r}\n"
                             f"Valid values: {valid}")
        return self._encode[value]


#===============================================================================
# UnitValue
#===============================================================================

class UnitValue:                        # pylint: disable=too-few-public-methods
    """
    Representation of a 'Real' value with units in a PSCAD parameter
    """


    def __new__(cls, value):

        if not isinstance(value, str):
            if isinstance(value, (int, float)):
                value = str(value)
            else:
                raise ValueError(f"Expected <str>, got {value!r}")

        if m := re.fullmatch(r"(\S+)\s*\[[^]]+\]", value):
            num = m[1]
        else:
            num = value

        try:
            float(num)
        except ValueError:
            raise ValueError(f"Expected 'value [units]' string, got {value!r}"
                             ) from None
        return value



#===============================================================================
# Resource Types
#===============================================================================

class ResourceType(ParamEnum):
    """
    Types of Resource for a PSCAD Project
    """

    UNKNOWN = '0'
    TEXT = '1'
    BINARY = '2'


#===============================================================================
# Ports
#===============================================================================

class NodeType(ParamEnum):
    """
    Node Input/Output/Electrical Type
    """

    UNKNOWN = '0'
    INPUT = '1'
    OUTPUT = '2'
    ELECTRICAL = '3'
    SHORT = '4'


class SignalType(ParamEnum):
    """
    Signal Types
    """

    ELECTRICAL = '0'
    LOGICAL = '1'
    INTEGER = '2'
    REAL = '3'
    COMPLEX = '4'
    UNKNOWN = '15'


class ElectricalType(ParamEnum):
    """
    Electrical Node Types
    """

    FIXED = '0'
    REMOVABLE = '1'
    SWITCHED = '2'
    GROUND = '3'


#===============================================================================
# BusType
#===============================================================================

class BusType(ParamEnum):
    """
    Bus Types
    """

    AUTO = '0'
    LOAD_PQ = '1'
    GENERATOR_PV = '2'
    SWING = '3'

    # Some aliases
    LOAD = '1'
    PQ = '1'
    GENERATOR = '2'
    PV = '2'


#===============================================================================
# Graphics
#===============================================================================

class Align(ParamEnum):
    """
    Text Alignment
    """

    LEFT = '0'
    CENTER = '1'
    RIGHT = '2'


class LineStyle(ParamEnum):
    """
    Line Styles
    """

    SOLID = '0'
    DASH = '1'
    DOT = '2'
    DASHDOT = '3'


class FillStyle(ParamEnum):
    """
    Fill Styles
    """

    HOLLOW = '0'
    SOLID = '1'
    BACKWARD_DIAGONAL = '2'
    FORWARD_DIAGONAL = '3'
    CROSS = '4'
    DIAGONAL_CROSS = '5'
    HORIZONTAL = '6'
    VERTICAL = '7'
    GRADIENT_HORZ = '8'
    GRADIENT_VERT = '9'
    GRADIENT_BACK_DIAG = '10'
    GRADIENT_FORE_DIAG = '11'
    GRADIENT_RADIAL = '12'


#===============================================================================
# Coordinate
#===============================================================================

Point = NamedTuple("Point", [('x', int), ('y', int)])


#===============================================================================
# XY
#===============================================================================

@dataclass(frozen=True)
class XY:
    """
    Two dimensional position or size, used to specify `Component` locations
    on a `Schematic` canvas.
    """

    x: int
    y: int


    def __add__(self, other: XY):
        return XY(self.x + other.x, self.y + other.y)


    def __sub__(self, other: XY):
        return XY(self.x - other.x, self.y - other.y)


    def __mul__(self, scale: int):
        return XY(self.x * scale, self.y * scale)


DOWN = XY(0, 18)
UP = XY(0, -18)
LEFT = XY(-18, 0)
RIGHT = XY(18, 0)


#===============================================================================
# Arrows (for Sticky Notes)
#===============================================================================

class Arrows(int, Flag):                    # type: ignore[misc]
    """
    Stick Note arrow direction flags
    """

    _orig_new: Any

    NONE = 0
    N = 1 << 0
    S = 1 << 1
    W = 1 << 2
    E = 1 << 3
    NW = 1 << 4
    NE = 1 << 5
    SW = 1 << 6
    SE = 1 << 7


    @classmethod
    def encode_to_str(cls, value: Any) -> str:
        """
        Encode the given arrow value to the PSCAD parameter string
        """

        return str(cls(value))


    @classmethod
    def _int_or_str_new(cls, clz, value):
        if isinstance(value, str):
            if value.isdecimal():
                value = int(value)
            else:
                value = value.replace(',', ' ')
                value = sum(cls[flag].value for flag in value.split())
        return cls._orig_new(clz, value)


    def __str__(self):
        return str(self.value)


# In addition to Arrows(int), allow Arrows(str) to yield proper flags
Arrows._orig_new = Arrows.__new__             # pylint: disable=protected-access
Arrows.__new__ = Arrows._int_or_str_new       # type: ignore[method-assign,assignment] # pylint: disable=protected-access

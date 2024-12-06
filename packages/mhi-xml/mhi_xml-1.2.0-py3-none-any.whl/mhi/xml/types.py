"""
=========
Types
=========
"""


#===============================================================================
# Imports
#===============================================================================

from __future__ import annotations
from enum import Enum, EnumMeta


#===============================================================================
# Exports
#===============================================================================

__all__ = ['ParamEnum',
           ]


#===============================================================================
# Parameter Enum Metatype
#===============================================================================

class ParamEnumType(EnumMeta):
    """
    Meta class for ParamEnum

    Enables `Enum`-like `ParamEnum('SOME_IDENTIFIER')` syntax
    as well as `ParamEnum(7)`
    """

    def __call__(cls, value):               # pylint: disable=signature-differs

        if isinstance(value, cls):
            return value

        if isinstance(value, str):
            if param_enum := cls.__members__.get(value.upper()):
                return param_enum

        if isinstance(value, int):
            value = str(value)

        return super().__call__(value)


#===============================================================================
# Parameter Enum
#===============================================================================

class ParamEnum(str, Enum, metaclass=ParamEnumType):
    """
    Base class for Parameter Enum

    Usage:

        class MyParamEnum(ParamEnum):
            MODE_A = '1'
            MODE_B = '2'
            NO_MODE = '-1'
    """

    def __new__(cls, value):

        if isinstance(value, int):
            value = str(value)

        return str.__new__(cls, value)


    def __str__(self):
        return self.value

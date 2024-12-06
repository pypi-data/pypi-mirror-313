"""
XML entities for PSCAD TLines/Cables
"""

#===============================================================================
# Imports
#===============================================================================

from __future__ import annotations

from functools import cached_property
import re
from typing import List, Optional, Type, Tuple, Union
from typing import cast, TypeVar

from mhi.xml.node import ParamNode
from mhi.xml.pscad._project import project_lookup

from mhi.xml.pscad.definition import Definition
from mhi.xml.pscad.twm_types import (
    TWMCmp,
    BergOptions, FreDepOptions, FrePhaseOptions, ManualYZ, OutDisp, Ground,
    Tower1, Tower2Flat,
    Tower3Flat, Tower3Delta, Tower3Concent, Tower3Offset, Tower3Vert,
    Tower6Vert1, Tower6Concent, Tower6Offset, Tower6Vert, Tower6Flat,
    Tower6Delta,
    Tower12Vert,
    TowerUniversal,
    )


#===============================================================================
# Exports
#===============================================================================

__all__ = ['RowDefn']



#===============================================================================
# Distance
#===============================================================================

Distance = Union[float, str]


#===============================================================================
# To meters
#===============================================================================

VALUE_UNIT = re.compile(r'([-+0-9.eE]+)\s*(\[[^]]\])?')

def value_unit(x: Distance, dflt_unit='[m]') -> Tuple[float, str]:
    """
    Parse a distance to a value & unit string
    """

    if isinstance(x, (int, float)):
        return float(x), dflt_unit
    if match := VALUE_UNIT.fullmatch(x):
        return float(match[1]), match[2] or dflt_unit
    raise ValueError("Unrecognized value")


def m(x: Distance, dflt_unit='[m]') -> Distance:
    """
    Convert a distance measurement into a 'ValueUnit' string
    """

    value, unit = value_unit(x, dflt_unit)

    return f'{value} {unit}'


def add(a: Distance, b: Distance) -> Distance:
    """
    Add compatible distance values
    """

    v1, u1 = value_unit(a)
    v2, u2 = value_unit(b)

    if u1 != u2:
        raise ValueError("Units must exactly match")

    return f'{v1+v2} {u1}'


def m_abs(x: Distance) -> Distance:
    """
    Convert a signed distance to an unsigned distance
    """

    value, unit = value_unit(x)

    return f'{abs(value)} {unit}'


#===============================================================================
# Definition
#===============================================================================

TwmCmp = TypeVar('TwmCmp', bound=TWMCmp)

@project_lookup.classid('RowDefn')
class RowDefn(Definition):             # pylint: disable=too-many-public-methods
    """
    Travelling Wave Model (TLine/Cable) Definition node
    """

    # pylint: disable=line-too-long
    _XML = (
 """<Definition classid="RowDefn" name="{name}" group="" build="" id="0" view="false" instance="0" crc="0">
      <paramlist>
        <param name="Description" value="" />
        <param name="type" value="{type}" />
      </paramlist>
      <schematic classid="RowCanvas" zoomlevel="6" scrollx="0" scrolly="0">
        <paramlist>
          <param name="show_grid" value="1" />
          <param name="size" value="0" />
          <param name="orient" value="1" />
          <param name="show_border" value="0" />
        </paramlist>
        <grouping />
      </schematic>
    </Definition>""")
    # pylint: enable=line-too-long

    @cached_property
    def type(self) -> str:
        """
        Is this TWM a TLine or Cable?
        """

        param = cast(ParamNode, self.find('paramlist/param[@name="type"]'))
        return param.value


    @cached_property
    def _canvas(self):

        return self.schematic


    def _find(self, cls: Type[TwmCmp]) -> Optional[TwmCmp]:

        xpath = f'User[@defn="{cls._defn}"]'  # pylint: disable=protected-access
        node = self._canvas.find(xpath)

        return cast(TwmCmp, node)


    def _get(self, cls: Type[TwmCmp]) -> TwmCmp:

        cmp = self._find(cls)
        if cmp is None:
            raise ValueError(f"{cls._defn} not found on TWM canvas!") # pylint: disable=protected-access
        return cmp


    def _create(self, cls: Type[TwmCmp], x: int, y: int) -> TwmCmp:

        canvas = self._canvas
        cmp = canvas.create(cls._defn)        # pylint: disable=protected-access
        cmp.parameters.set_defaults()
        canvas.add(cmp, x*18, y*18, orient=0)

        return cmp


    def _find_and_remove(self, *classes: Type[TWMCmp]) -> None:

        for cls in classes:
            cmp = self._find(cls)
            if cmp is not None:
                cmp.delete()


    def _find_or_create(self, cls: Type[TwmCmp], x, y) -> TwmCmp:

        if (cmp := self._find(cls)) is None:
            cmp = self._create(cls, x, y)

        return cmp


    #---------------------------------------------------------------------------
    # Bergeron Options (cannot be used with FreqPhase)
    #---------------------------------------------------------------------------

    @property
    def bergeron_options(self) -> BergOptions:
        """
        Retrieve the Bergeron Options component, creating it if necessary
        """

        self._find_and_remove(FreDepOptions, FrePhaseOptions)

        return self._find_or_create(BergOptions, 32, 10)


    #---------------------------------------------------------------------------
    # Frequency (Phase) Dependent Options (cannot be used with BergOptions)
    #---------------------------------------------------------------------------

    @property
    def freq_phase_options(self) -> FrePhaseOptions:
        """
        Retrieve the Freq/Phase Options component, creating it if necessary
        """

        self._find_and_remove(FreDepOptions, BergOptions, ManualYZ)

        return self._find_or_create(FrePhaseOptions, 33, 10)


    #---------------------------------------------------------------------------
    # Additional Display Options
    #---------------------------------------------------------------------------

    @property
    def additional_options(self) -> OutDisp:
        """
        Retrieve the Additional Options component, creating it if necessary
        """

        return self._find_or_create(OutDisp, 56, 5)


    #---------------------------------------------------------------------------
    # Ground (cannot be used with Manual Entry)
    #---------------------------------------------------------------------------

    @property
    def ground(self) -> Ground:
        """
        Retrieve the Ground component, creating it if necessary
        """

        return self._find_or_create(Ground, 23, 39)


    #---------------------------------------------------------------------------
    # Manual Entry of Y, Z (cannot be used with FreqDep models, & Ground cmp)
    #---------------------------------------------------------------------------

    @property
    def manual_yz(self) -> ManualYZ:
        """
        Retrieve the Manual YZ component, creating it if necessary
        """

        self._find_and_remove(FreDepOptions, FrePhaseOptions, ManualYZ, Ground)

        return self._find_or_create(ManualYZ, 32, 19)


    #---------------------------------------------------------------------------
    # Towers
    #---------------------------------------------------------------------------

    def towers(self) -> List[TWMCmp]:
        """
        List of the towers
        """

        towers = [cmp for cmp in self._canvas
                  if cmp.defn.startswith('master:Line_Tower_')]
        return cast(List[TWMCmp], towers)


    _TOWER_Y = {'1': 29,
                '2_Flat': 29,
                '3-Flat': 29, '3_Delta': 29, '3_Concent': 27, '3_Offset': 29,
                '3_Vert': 25,
                '6_Vert1': 22, '6_Concent': 27, '6_Offset': 29, '6_Vert': 25,
                '6_Flat': 29, '6_Delta': 29,
                '12_Vert': 22,
                }

    def _create_tower(self, cls: Type[TwmCmp], **kwargs) -> TwmCmp:
        towers = self.towers()
        last_tower = max(towers, key=lambda twr: twr.location.x, default=None)
        if last_tower is not None:
            x = last_tower.location.x // 18
            x += 17
            if last_tower.defn == 'master:Line_Tower_Universal':
                x += 8
        else:
            x = 9

        defn = cls._defn                      # pylint: disable=protected-access
        if defn == 'master:Line_Tower_Universal':
            x += 10
        y = self._TOWER_Y.get(defn[18:], 22)

        tower = self._create(cls, x, y)

        params = tower.parameters
        for key, value in kwargs.items():
            setattr(params, key, value)

        return tower


    #---------------------------------------------------------------------------
    # 1 conductor towers
    #---------------------------------------------------------------------------

    def tower_1(self, x: Distance, y: Distance, **kwargs) -> Tower1:
        """
        Add a single conductor tower

        The conductor is located at the given (x, y) coordinate.
        """

        x = m(x)
        y = m(y)

        return self._create_tower(Tower1, X=x, Y=y, **kwargs)


    #---------------------------------------------------------------------------
    # 2 conductor towers
    #---------------------------------------------------------------------------

    def tower_2_flat(self, x: Distance, y: Distance, xc: Distance,
                     **kwargs) -> Tower2Flat:
        """
        Add a 2-conductor tower

        The conductors are located at (x - xc / 2, y) and (x + xc / 2, y).
        """

        x = m(x)
        y = m(y)
        xc = m(xc)

        return self._create_tower(Tower2Flat, X=x, Y=y, XC=xc, **kwargs)


    #---------------------------------------------------------------------------
    # 3 conductor towers
    #---------------------------------------------------------------------------

    def tower_3_flat(self, x: Distance, y: Distance, xc: Distance,
                     **kwargs) -> Tower3Flat:
        """
        Add a 3-conductor tower

        The conductors are located at (x - xc, y), (x, y), and (x + xc, y).
        """

        x = m(x)
        y = m(y)
        xc = m(xc)

        return self._create_tower(Tower3Flat, X=x, Y=y, XC=xc, **kwargs)


    def tower_3_delta(self, x: Distance, y: Distance,
                      xc: Distance, y2: Distance, **kwargs) -> Tower3Delta:
        """
        Add a 3-conductor tower

        The conductors are at (x - xc, y), (x, y + y2), and (x + xc, y).
        """

        x = m(x)
        y = m(y)
        xc = m(xc)
        y2 = m(y2)

        return self._create_tower(Tower3Delta, X=x, Y=y, XC=xc, Y2=y2,
                                  **kwargs)


    def tower_3_concent(self, x: Distance, y: Distance,
                        x2: Distance, y2: Distance, **kwargs) -> Tower3Concent:
        """
        Add a 3-conductor tower

        The conductors are at (x, y), (x + x2, y + y2), and (x, y + 2 y2).
        If x2 is negative, the second conductor is to left of the other two.
        """

        x = m(x)
        y = m(y)
        x2 = m(x2)
        y2 = m(y2)

        v, _ = value_unit(x2)
        x2 = m_abs(x2)
        side = "the right" if v > 0 else "the left"

        return self._create_tower(Tower3Concent, X=x, Y=y, X2=x2, Y2=y2,
                                  side=side, **kwargs)


    def tower_3_offset(self, x: Distance, y: Distance,
                       x2: Distance, y2: Distance, **kwargs) -> Tower3Offset:
        """
        Add a 3-conductor tower

        The conductors are at (x, y), (x + x2, y), and (x, y + y2).
        If x2 is negative, the second conductor is to left of the other two.
        """

        x = m(x)
        y = m(y)
        x2 = m(x2)
        y2 = m(y2)

        v, _ = value_unit(x2)
        x2 = m_abs(x2)
        side = "the right" if v > 0 else "the left"

        return self._create_tower(Tower3Offset, X=x, Y=y, X2=x2, Y2=y2,
                                  side=side, **kwargs)


    def tower_3_vert(self, x: Distance, y: Distance, y2: Distance,
                     **kwargs) -> Tower3Vert:
        """
        Add a 3-conductor tower

        The conductors are at (x, y), (x, y + y2), and (x, y + 2 y2).
        """

        x = m(x)
        y = m(y)
        y2 = m(y2)

        return self._create_tower(Tower3Vert, X=x, Y=y, Y2=y2, **kwargs)


    #---------------------------------------------------------------------------
    # 6 conductor towers
    #---------------------------------------------------------------------------

    def tower_6_vert1(self, x: Distance, y: Distance, y2: Distance,
                      y3: Distance, **kwargs) -> Tower6Vert1:
        """
        Add a 6-conductor tower

        The first 3 conductors are at (x, y), (x, y + y2), and (x, y + 2 y2).
        The next 3 conductors are an additional y3 higher.
        """

        y2 = m(y2)
        y3 = m(y3)
        if value_unit(y3)[0] < 3 * value_unit(y2)[0]:
            raise ValueError("y3 should be at least triple y2")

        return self._create_tower(Tower6Vert1, X=x, Y=y, Y2=y2, Y3=y3,
                                  **kwargs)

    def tower_6_concent(self,
                        x: Distance, y: Distance, xc: Distance,
                        x2: Distance, y2: Distance, **kwargs) -> Tower6Concent:
        """
        Add a 6-conductor tower

        The conductors are at
        (x - xc/2, y), (x - xc/2 - x2, y + y2), (x - xc/2, y + 2 y2),
        (x + xc/2, y), (x + xc/2 + x2, y + y2), and (x + xc/2, y + 2 y2).
        """

        return self._create_tower(Tower6Concent, X=x, Y=y, XC=xc, X2=x2, Y2=y2,
                                  **kwargs)


    def tower_6_offset(self,
                       x: Distance, y: Distance, xc: Distance,
                       x2: Distance, y2: Distance, **kwargs) -> Tower6Offset:
        """
        Add a 6-conductor tower

        The conductors are arranged in a two mirrored L-shape.
        """

        return self._create_tower(Tower6Offset, X=x, Y=y, XC=xc, X2=x2, Y2=y2,
                                  **kwargs)


    def tower_6_vert(self, x: Distance, y: Distance, xc: Distance, y2: Distance,
                     **kwargs) -> Tower6Vert:
        """
        Add a 6-conductor tower

        The conductors are at
        (x - xc/2, y), (x - xc/2, y + y2), (x - xc/2, y + 2 y2).
        (x + xc/2, y), (x + xc/2, y + y2), and (x + xc/2, y + 2 y2).
        """

        return self._create_tower(Tower6Vert, X=x, Y=y, XC=xc, Y2=y2,
                                  **kwargs)


    def tower_6_flat(self, x: Distance, y: Distance, xc: Distance, y2: Distance,
                     **kwargs) -> Tower6Flat:
        """
        Add a 6-conductor tower

        The first 3 conductors are at (x, y), (x + xc, y), and (x + 2 xc, y).
        The next 3 conductors are an additional y2 higher.
        """

        return self._create_tower(Tower6Flat, X=x, Y=y, XC=xc, Y2=y2,
                                  **kwargs)


    def tower_6_delta(self,
                      x: Distance, y: Distance, xc: Distance,
                      x2: Distance, y2: Distance, **kwargs) -> Tower6Delta:
        """
        Add a 6-conductor tower

        The conductors are arranged in a two delta shape.
        """

        return self._create_tower(Tower6Delta, X=x, Y=y, XC=xc, X2=x2, Y2=y2,
                                  **kwargs)


    #---------------------------------------------------------------------------
    # 12 conductor towers
    #---------------------------------------------------------------------------

    def tower_12_vert(self,
                      x: Distance, y: Distance, xc: Distance,
                      y2: Distance, y3: Distance, **kwargs) -> Tower12Vert:
        """
        Add a 12-conductor tower
        """

        y2 = m(y2)
        y3 = m(y3)
        if value_unit(y3)[0] < 3 * value_unit(y2)[0]:
            raise ValueError("y3 should be at least triple y2")


        return self._create_tower(Tower12Vert, X=x, Y=y, XC=xc, Y2=y2, Y3=y3,
                                  **kwargs)


    #---------------------------------------------------------------------------
    # universal tower
    #---------------------------------------------------------------------------

    def tower_universal(self,
                        tower_x: Distance,
                        conductors: List[Tuple[float, float]],
                        ground_wires: List[Tuple[float, float]],
                        **kwargs) -> TowerUniversal:
        """
        Add a tower with between 1 and 12 conductors, and between 0 and 2
        grounds wires.

        Both the conductors and the ground wires must be given as lists
        of (x,y) pairs:
        """

        nc = len(conductors)
        ng = len(ground_wires)

        xc = m(tower_x)

        if nc < 1 or nc > 12:
            raise ValueError("Requires 1-12 conductors")

        if len(ground_wires) > 2:
            raise ValueError("Maximum 2 ground wires")

        coords = {}
        for i, (x, y) in enumerate(conductors, 1):
            coords[f'XC{i}'] = m(x)
            coords[f'YC{i}'] = m(y)
        for i, (x, y) in enumerate(ground_wires, 1):
            coords[f'XG{i}'] = m(x)
            coords[f'YG{i}'] = m(y)

        return self._create_tower(TowerUniversal, X=xc, Nc=nc, NG=ng,
                                  **kwargs, **coords)


    #---------------------------------------------------------------------------
    # Representation
    #---------------------------------------------------------------------------

    def __repr__(self) -> str:

        return f"{self.type}<{self.name}>"

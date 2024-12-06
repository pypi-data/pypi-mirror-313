"""
XML entities for vertices

Note: <vertex> can appears as child node of:
   - Definition/graphics/Gfx
   - Definition/schematic/Wire
"""

#===============================================================================
# Imports
#===============================================================================

from __future__ import annotations

from mhi.xml.node import XmlNode
from mhi.xml.pscad._project import project_lookup
from mhi.xml.pscad.types import XY


#===============================================================================
# Exports
#===============================================================================

__all__ = ['Vertex', ]


#===============================================================================
# Graphics
#===============================================================================

@project_lookup.tag('vertex')
class Vertex(XmlNode):
    """
    A `<vertex/>` node


    .. versionadded:: 1.2.0
    """


    @property
    def x(self) -> int:
        """The X coordinate"""

        return int(self.get('x', '0'))


    @x.setter
    def x(self, new_x: int):

        self.set('x', str(new_x))


    @property
    def y(self) -> int:
        """The Y coordinate"""

        return int(self.get('y', '0'))


    @y.setter
    def y(self, new_y: int):

        self.set('y', str(new_y))


    @property
    def xy(self) -> XY:
        """
        The XY coordinates

        .. versionadded:: 1.2.0
        """

        return XY(self.x, self.y)


    @xy.setter
    def xy(self, xy: XY):

        self.x = xy.x
        self.y = xy.y


    def __iadd__(self, other: XY):

        self.x = self.x + other.x
        self.y = self.y + other.y


    def __isub__(self, other: XY):

        self.x = self.x - other.x
        self.y = self.y - other.y


    def __repr__(self):
        return f"Vertex[{self.x}, {self.y}]"

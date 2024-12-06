"""
XML entities for PSCAD graphic definitions

Lines, Ports, etc
"""

#===============================================================================
# Imports
#===============================================================================

from __future__ import annotations

from functools import cached_property
from typing import Iterator, Mapping, cast, Any, Optional, Protocol, Union

from lxml import etree as ET

from mhi.xml.node import (XmlNode, ParamNode, ParamListNode, ParametersBase)
from mhi.xml.pscad.colour import Colour
from mhi.xml.pscad.vertex import Vertex
from mhi.xml.pscad.types import (NodeType, SignalType, ElectricalType,
                                 Align, LineStyle, FillStyle)
from mhi.xml.pscad._project import project_lookup, ProjectMixin


#===============================================================================
# Exports
#===============================================================================

__all__ = ['Graphics',
           'GfxText', 'GfxLine', 'GfxRectangle', 'GfxEllipse',
           'Port', 'PortMapping']


#===============================================================================
# Graphics
#===============================================================================

@project_lookup.tag('graphics')
class Graphics(XmlNode, ProjectMixin):
    """
    A `<graphics/>` container node
    """


    #-----------------------------------------------------------------------

    _GFX_PARAM = {'color': Colour,
                  'fill_fg': Colour,
                  'fill_bg': Colour,
                  'align': Align,
                  'fill_style': FillStyle,
                  'dasharray': LineStyle,
                  }

    def _add_gfx(self, kind, **kwargs):

        attrs = {key: str(val) for key, val in kwargs.items()
                 if key in {'x', 'y', 'w', 'h'}}
        params = {key: val for key, val in kwargs.items()
                  if key not in {'x', 'y', 'w', 'h'}}

        for name, param_type in self._GFX_PARAM.items():
            if name in params:
                params[name] = param_type(params[name])

        gfx = self.makeelement('Gfx', classid=f"Graphics.{kind}",
                               id=str(self._file.make_id()), **attrs)

        self.append_indented(gfx)
        paramlist = cast(ParamListNode, gfx.makeelement('paramlist'))
        gfx.append_indented(paramlist)
        paramlist.create_params(params)

        return cast(GfxNode, gfx)


    #-----------------------------------------------------------------------

    def add_text(self,
                 *coords, text: str, color: str = 'Black',
                 full_font: str = 'Tahoma, 12world',
                 font_size: int = 0,
                 align: Union[str, Align, int] = Align.CENTER,
                 angle: int = 0,
                 cond: str = 'true'):
        """
        Add a line of text to the definition graphics
        """

        if len(coords) == 2:
            x, y = coords
        elif len(coords) == 1:
            (x, y), = coords
        else:
            raise TypeError(f"Unexpected coordinate: {coords!r}")

        gfx = self._add_gfx('Text', x=x, y=y, text=text, color=color,
                            full_font=full_font, font_size=font_size,
                            anchor=align, angle=angle, cond=cond)

        return gfx


    #-----------------------------------------------------------------------

    def add_line(self,
                 *coords, color: str = 'Black',
                 line_style: Union[str, LineStyle, int] = LineStyle.SOLID,
                 thickness: int = 0, port: str = '',
                 cond: str = 'true'):
        """
        Add a line to the definition graphics
        """

        if len(coords) == 4:
            x1, y1, x2, y2 = coords
        elif len(coords) == 2:
            (x1, y1), (x2, y2) = coords
        else:
            raise TypeError(f"Unexpected coordinate: {coords!r}")

        gfx = self._add_gfx('Line', x=x1, y=y1,
                            color=color, dasharray=line_style,
                            thickness=thickness, port=port,
                            cond=cond)

        v1 = gfx.makeelement('vertex', x='0', y='0')
        v2 = gfx.makeelement('vertex', x=str(x2-x1), y=str(y2-y1))
        gfx.append_indented(v1)
        gfx.append_indented(v2)

        return gfx


    #-----------------------------------------------------------------------

    def add_rect(self,                         # pylint: disable=too-many-locals
                 *coords, color: str = 'Black',
                 line_style: Union[str, LineStyle, int] = LineStyle.SOLID,
                 thickness: int = 0, port: str = '',
                 fill_style: Union[str, FillStyle, int] = FillStyle.HOLLOW,
                 fill_fg: str = 'Black', fill_bg : str = 'White',
                 cond: str = 'true'):
        """
        Add a rectangle to the definition graphics
        """

        if len(coords) == 4:
            x, y, w, h = coords
        elif len(coords) == 2:
            (x1, y1), (x2, y2) = coords
            x, y, w, h = min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2)
        else:
            raise TypeError(f"Unexpected coordinate: {coords!r}")

        gfx = self._add_gfx('Rectangle', x=x, y=y, w=w, h=h,
                            color=color, dasharray=line_style,
                            thickness=thickness, port=port,
                            fill_style=fill_style,
                            fill_fg=fill_fg, fill_bg=fill_bg,
                            cond=cond)
        return gfx


    #-----------------------------------------------------------------------

    def add_ellipse(self,                      # pylint: disable=too-many-locals
                    *coords, color: str = 'Black',
                    line_style: Union[str, LineStyle, int] = LineStyle.SOLID,
                    thickness: int = 0, port: str = '',
                    fill_style: Union[str, FillStyle, int] = FillStyle.HOLLOW,
                    fill_fg: str = 'Black', fill_bg : str = 'White',
                    cond: str = 'true'):
        """
        Add an ellipse to the definition graphics
        """

        if len(coords) == 4:
            x, y, w, h = coords
        elif len(coords) == 2:
            (x1, y1), (x2, y2) = coords
            x, y, w, h = min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2)
        else:
            raise TypeError(f"Unexpected coordinate: {coords!r}")

        gfx = self._add_gfx('Ellipse', x=x, y=y, w=w, h=h,
                            color=color, dasharray=line_style,
                            thickness=thickness, port=port,
                            fill_style=fill_style,
                            fill_fg=fill_fg, fill_bg=fill_bg,
                            cond=cond)
        return gfx


    #-----------------------------------------------------------------------

    def add_circle(self,
                   *coords, color: str = 'Black',
                   line_style: Union[str, LineStyle, int] = LineStyle.SOLID,
                   thickness: int = 0, port: str = '',
                   fill_style: Union[str, FillStyle, int] = FillStyle.HOLLOW,
                   fill_fg: str = 'Black', fill_bg : str = 'White',
                   cond: str = 'true'):
        """
        Add a circle to the definition graphics
        """

        if len(coords) == 3:
            x, y, r = coords
        elif len(coords) == 2:
            (x, y), r = coords
        else:
            raise TypeError(f"Unexpected coordinate: {coords!r}")

        gfx = self.add_ellipse((x-r, y-r), (x+r, y+r),
                               color=color, line_style=line_style,
                               thickness=thickness, port=port,
                               fill_style=fill_style,
                               fill_fg=fill_fg, fill_bg=fill_bg,
                               cond=cond)

        return gfx


    #-----------------------------------------------------------------------

    def ports(self, name: Optional[str] = None) -> list[Port]:
        """
        Retrieve the list of ports defined in the component graphics
        """

        params = {}
        if name:
            params['name'] = name

        xpath = "Port"
        if params:
            paramlist = "".join(f"param[@name='{key}'][@value='{val}']"
                                for key, val in params.items())
            xpath += f"[paramlist[{paramlist}]]"

        ports = self.xpath(xpath)
        return cast(list[Port], ports)


    #-----------------------------------------------------------------------

    @cached_property
    def port(self) -> PortMapping:
        """
        Retrive the port mapping
        """

        return PortMapping(self)


    #-----------------------------------------------------------------------

    def _add_port(self, x: int, y: int, **kwargs) -> Port:

        port = cast(Port,
                    self.makeelement('Port', classid="Port",
                                     x=str(x), y=str(y),
                                     id=str(self._file.make_id())))
        self.append_indented(port)

        paramlist = cast(ParamListNode, port.makeelement('paramlist'))
        port.append_indented(paramlist)
        paramlist.create_params(kwargs)

        return port


    #-----------------------------------------------------------------------

    def add_input(self,
                  x: int, y: int, name: str, *,
                  dim: int = 1, cond: str = 'true', internal: bool = False,
                  datatype: Union[SignalType, str, int] = SignalType.REAL
                  ) -> Port:
        """
        Add an input port to the graphic definition
        """

        datatype = SignalType(datatype)

        return self._add_port(x, y, name=name, dim=dim, cond=cond,
                              internal=internal, datatype=datatype,
                              mode=NodeType.INPUT,
                              electype=ElectricalType.FIXED)


    #-----------------------------------------------------------------------

    def add_output(self,
                   x: int, y: int, name: str, *,
                   dim: int = 1, cond: str = 'true', internal: bool = False,
                   datatype: Union[SignalType, str, int] = SignalType.REAL,
                   ) -> Port:
        """
        Add an output port to the graphic definition
        """

        datatype = SignalType(datatype)

        return self._add_port(x, y, name=name, dim=dim, cond=cond,
                              internal=internal, datatype=datatype,
                              mode=NodeType.OUTPUT,
                              electype=ElectricalType.FIXED)


    #-----------------------------------------------------------------------

    def add_electrical(self,
                       x: int, y: int, name: str, *,
                       dim: int = 1, cond: str = 'true', internal: bool = False,
                       electype: Union[ElectricalType, str, int] = ElectricalType.FIXED,
                       ) -> Port:
        """
        Add an electical port to the graphic definition
        """

        electype = ElectricalType(electype)

        return self._add_port(x, y, name=name, dim=dim, cond=cond,
                              internal=internal, electype=electype,
                              mode=NodeType.ELECTRICAL,
                              datatype=SignalType.ELECTRICAL)


#===============================================================================
# Gfx Nodes
#===============================================================================

class GfxProtocol(Protocol):
    """
    Gfx base mixin class
    """

    def set(self, key: str, value: str) -> None:
        """Attribute setter"""

    def get(self, key: str, default: str) -> str:
        """Attribute getter"""

    def find(self, xpath: str) -> Optional[ET._Element]:
        """Parameter Finder"""


#===============================================================================

class XYMixin(GfxProtocol):
    """
    Gfx mixin class adding X/Y attributes
    """

    #-----------------------------------------------------------------------

    @property
    def x(self) -> int:
        """
        The x-location of the Gfx item
        """

        return int(self.get('x', '0'))

    @x.setter
    def x(self, x: int):
        self.set('x', str(x))


    #-----------------------------------------------------------------------

    @property
    def y(self) -> int:
        """
        The y-location of the Gfx item
        """

        return int(self.get('y', '0'))

    @y.setter
    def y(self, y: int):
        self.set('y', str(y))


    #-----------------------------------------------------------------------

    @property
    def location(self) -> tuple[int, int]:
        """
        The (x, y) location of the Gfx item
        """

        return self.x, self.y

    @location.setter
    def location(self, location: tuple[int, int]):
        self.x, self.y = location


#===============================================================================

class ParamMixin(GfxProtocol):
    """
    Gfx mixin class for access to parameters
    """

    #-----------------------------------------------------------------------

    def _param(self, name: str) -> ParamNode:

        node = self.find(f'paramlist/param[@name="{name}"]') # pylint: disable=assignment-from-no-return
        assert node is not None

        return cast(ParamNode, node)


    def _get_param(self, name: str) -> str:

        return self._param(name).value


    def _set_param(self, name: str, value: Any) -> None:

        self._param(name).set_value(value)


#===============================================================================

class CondMixin(ParamMixin):
    """
    Gfx mixin class for access to the "cond" parameters
    """

    #-----------------------------------------------------------------------

    @property
    def cond(self) -> str:
        """
        The 'cond' property of a Gfx item
        """

        return self._get_param('cond')

    @cond.setter
    def cond(self, cond: str):

        self._set_param('cond',  cond)


#===============================================================================

@project_lookup.tag('Gfx')
class GfxNode(XmlNode, ProjectMixin, XYMixin, CondMixin):
    """
    A `<Gfx/>` node
    """

    #-----------------------------------------------------------------------

    @property
    def color(self) -> Colour:
        """
        The 'color' property of a visible Gfx item
        """

        return Colour(self._get_param('color'))

    @color.setter
    def color(self, colour: Union[Colour, str, int]):

        self._set_param('color', Colour(colour))


    #-----------------------------------------------------------------------

    def _repr_attrs(self) -> str:

        s = f"{self.x},{self.y}"
        if isinstance(self, WidthHeightMixin):
            s += f",{self.w},{self.h}"
        return s

    def __repr__(self):

        return f"{self.__class__.__name__}[{self._repr_attrs()}]"


#===============================================================================

class LineMixin(ParamMixin):
    """
    Graphic items drawn with strokes
    """

    #-----------------------------------------------------------------------

    @property
    def dasharray(self) -> LineStyle:
        """
        The 'Line Style' of a stroked Gfx item
        """

        return LineStyle(self._get_param('dasharray'))

    @dasharray.setter
    def dasharray(self, dasharray: Union[str, LineStyle, int]):

        self._set_param('dasharray', LineStyle(dasharray))


    #-----------------------------------------------------------------------

    @property
    def thickness(self) -> int:
        """
        The 'Line Thickness' of a stroked Gfx item
        """

        return int(self._param('thickness'))

    @thickness.setter
    def thickness(self, thickness: int):

        self._set_param('thickness', thickness)


class WidthHeightMixin(ParamMixin):
    """
    Graphic items defined by a rectangular bounding box
    """

    #-----------------------------------------------------------------------

    @property
    def w(self) -> int:
        """
        The 'width' of a some Gfx items
        """

        return int(self.get('w', '0'))

    @w.setter
    def w(self, w: int):

        self.set('w', str(w))


    #-----------------------------------------------------------------------

    @property
    def h(self) -> int:
        """
        The 'height' of a some Gfx items
        """

        return int(self.get('h', '0'))


    @h.setter
    def h(self, h: int):

        self.set('h', str(h))


    #-----------------------------------------------------------------------

    @property
    def size(self) -> tuple[int, int]:
        """
        The (width, height) of a some Gfx items
        """

        return self.w, self.h

    @size.setter
    def size(self, width_height: tuple[int, int]):

        self.w, self.h = width_height


#===============================================================================

class FillMixin(ParamMixin):
    """
    Graphic items which can be drawn filled-in
    """

    #-----------------------------------------------------------------------

    @property
    def fill_style(self) -> FillStyle:
        """
        The 'Fill Style' of a painted Gfx item
        """

        return FillStyle(self._get_param('fill_style'))

    @fill_style.setter
    def fill_style(self, fill_style: Union[str, FillStyle, int]):

        self._set_param('fill_style', FillStyle(fill_style))


    #-----------------------------------------------------------------------

    @property
    def fill_fg(self) -> Colour:
        """
        The 'Foreground color' of a painted Gfx item
        """

        return Colour(self._get_param('fill_fg'))

    @fill_fg.setter
    def fill_fg(self, colour:  Union[Colour, str, int]):

        self._set_param('fill_fg', Colour(colour))


    #-----------------------------------------------------------------------

    @property
    def fill_bg(self) -> Colour:
        """
        The 'Background Color' of a painted Gfx item
        """

        return Colour(self._get_param('fill_bg'))

    @fill_bg.setter
    def fill_bg(self, colour:  Union[Colour, str, int]):

        self._set_param('fill_bg', Colour(colour))


#===============================================================================

@project_lookup.classid('Graphics.Text')
class GfxText(GfxNode):
    """Gfx Text"""

    #-----------------------------------------------------------------------

    @property
    def value(self) -> str:
        """
        The 'message' of a Graphics.Text item
        """

        return self._get_param('text')

    @value.setter
    def value(self, text: str):

        self._set_param('text', text)


    #-----------------------------------------------------------------------

    @property
    def full_font(self) -> str:
        """
        The 'font' used to draw a Graphics.Text item
        """

        return self._get_param('full_font')

    @full_font.setter
    def full_font(self, full_font: str):

        self._set_param('full_font', full_font)


    #-----------------------------------------------------------------------

    @property
    def font_size(self) -> int:
        """
        The 'size of font' used to draw a Graphics.Text item
        """

        return int(self._param('font_size'))

    @font_size.setter
    def font_size(self, font_size: int):

        self._set_param('font_size', font_size)


    #-----------------------------------------------------------------------

    @property
    def anchor(self) -> Align:
        """
        The 'text anchor' (Left/Centre/Right) of a Graphics.Text item
        """

        return Align(self._get_param('anchor'))

    @anchor.setter
    def anchor(self, anchor: Union[Align, str, int]):

        self._set_param('anchor', Align(anchor))


    #-----------------------------------------------------------------------

    @property
    def angle(self) -> int:
        """
        The 'angle' (in degrees) to draw the Graphic.Text message at
        """

        return int(self._param('angle'))

    @angle.setter
    def angle(self, angle: int):

        self._set_param('angle', angle)


#===============================================================================

@project_lookup.classid('Graphics.Line')
class GfxLine(GfxNode, LineMixin):
    """Gfx Line"""

    def vertices(self) -> list[Vertex]:
        """
        The list <vertex> elements of a Graphics.Line

        .. versionchanged:: 1.2.0
        """

        return cast(list[Vertex], list(self.iterchildren('vertex')))


    def _repr_attrs(self) -> str:

        return "-".join(f'({x},{y})' for x, y in self.vertices())


#===============================================================================

@project_lookup.classid('Graphics.Rectangle')
class GfxRectangle(GfxNode, WidthHeightMixin, LineMixin, FillMixin):
    """Gfx Rectangle"""


#===============================================================================

@project_lookup.classid('Graphics.Ellipse')
class GfxEllipse(GfxNode, WidthHeightMixin, LineMixin, FillMixin):
    """Gfx Ellipse"""


#===============================================================================
# Port
#===============================================================================

@project_lookup.tag('Port')
class Port(XmlNode, ProjectMixin, XYMixin, CondMixin):
    """Graphics Port"""

    #-----------------------------------------------------------------------

    @property
    def name(self) -> str:
        """
        The 'name' of the connection point
        """

        return self._get_param('name')

    @name.setter
    def name(self, name: str):

        self._set_param('name', name)


    #-----------------------------------------------------------------------

    @property
    def dim(self) -> int:
        """
        The 'dimension' of the connection point
        """

        return int(self._param('dim'))

    @dim.setter
    def dim(self, dim: int):

        self._set_param('dim', dim)


    #-----------------------------------------------------------------------

    @property
    def mode(self) -> NodeType:
        """
        The 'mode' of the connection point (Input, Output, Electrical, ...)
        """

        return NodeType(self._get_param('mode'))

    @mode.setter
    def mode(self, mode: Union[NodeType, str, int]):

        self._set_param('mode', NodeType(mode))


    #-----------------------------------------------------------------------

    @property
    def datatype(self) -> SignalType:
        """
        The 'data type' of input/output Port (Logical, Integer, Real, ...)
        """

        return SignalType(self._get_param('datatype'))

    @datatype.setter
    def datatype(self, datatype: Union[SignalType, str, int]):
        self._set_param('datatype', SignalType(datatype))


    #-----------------------------------------------------------------------

    @property
    def electype(self) -> ElectricalType:
        """
        The 'type' of an Electrical Port (Fixed, Removable, Ground, ...)
        """

        return ElectricalType(self._get_param('electype'))

    @electype.setter
    def electype(self, electype: Union[ElectricalType, str, int]):

        self._set_param('electype', ElectricalType(electype))


    #-----------------------------------------------------------------------

    @property
    def internal(self) -> bool:
        """
        An electrical port's 'internal' nature (not connected externally)
        """

        return bool(self._param('internal'))

    @internal.setter
    def internal(self, internal: bool):

        self._set_param('internal', internal)


    #-----------------------------------------------------------------------

    def __repr__(self):
        #p = self.parameters().as_dict()
        mode = self.mode.name
        kind = self.datatype.name
        dimension = self.dim
        dim = f"({dimension})" if dimension > 1 else ""
        cond = self.cond
        cond = f", {cond}" if cond != "true" else ""
        location = "INTERNAL" if self.internal else f"({self.x},{self.y})"

        return (f"Port[{self.name!r}, {location}, "
                f"{mode}/{kind}{dim}{cond}]")


    #-----------------------------------------------------------------------

    def parameters(self) -> Port.Parameters:
        """
        Access to the Port parameters
        """

        return self.Parameters(self.find('paramlist'))


    #-----------------------------------------------------------------------

    class Parameters(ParametersBase):
        """
        Port parameters
        """

        name: str
        dim: int
        internal: bool
        cond: str
        mode: NodeType
        datatype: SignalType
        electype: ElectricalType


#===============================================================================
# Port Mapping
#===============================================================================

class PortMapping(Mapping[str, Port]):
    """
    The port container

    Use ``defn.port["name"]`` to access a :class:`.Port` by name.

    Since the same port name may exist multiple times with different
    ``enable`` condtions, use ``for port in defn.ports():`` to iterate over
    all defined ports.
    """

    def __init__(self, graphics: Graphics):

        self.container = graphics


    def __getitem__(self, key: str) -> Port:

        xpath = f'Port/paramlist/param[@name="name"][@value="{key!s}"]/../..'
        port = cast(Port, self.container.find(xpath))
        if port is None:
            raise KeyError(key)
        return port


    def __iter__(self) -> Iterator[str]:

        names: dict[str, None] = {}
        for node in self.container.iterfind('Port'):
            port = cast(Port, node)
            names[port.name] = None

        yield from names


    def __len__(self) -> int:

        names: dict[str, None] = {}
        for node in self.container.iterfind('Port'):
            port = cast(Port, node)
            names[port.name] = None

        return len(names)


    def __repr__(self) -> str:

        return f"Ports[{', '.join(self)}]"

    #-----------------------------------------------------------------------

    def add_input(self,                     # pylint: disable=too-many-arguments
                  x: int, y: int, name: str, *,
                  dim: int = 1, cond: str = 'true', internal: bool = False,
                  datatype: Union[SignalType, str, int] = SignalType.REAL
                  ) -> Port:
        """
        Add an input port
        """

        graphics = cast(Graphics, self.container)

        return graphics.add_input(x, y, name, dim=dim, cond=cond,
                                  internal=internal, datatype=datatype)


    #-----------------------------------------------------------------------

    def add_output(self,                    # pylint: disable=too-many-arguments
                   x: int, y: int, name: str, *,
                   dim: int = 1, cond: str = 'true', internal: bool = False,
                   datatype: Union[SignalType, str, int] = SignalType.REAL,
                   ) -> Port:
        """
        Add an output port
        """

        graphics = cast(Graphics, self.container)

        return graphics.add_output(x, y, name, dim=dim, cond=cond,
                                   internal=internal, datatype=datatype)


    #-----------------------------------------------------------------------

    def add_electrical(self,                # pylint: disable=too-many-arguments
                       x: int, y: int, name: str, *,
                       dim: int = 1, cond: str = 'true', internal: bool = False,
                       electype: Union[ElectricalType, str, int] = ElectricalType.FIXED,
                       ) -> Port:
        """
        Add an electical port
        """

        graphics = cast(Graphics, self.container)

        return graphics.add_electrical(x, y, name, dim=dim, cond=cond,
                                       internal=internal, electype=electype)

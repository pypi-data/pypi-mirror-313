"""
XML entities for PSCAD components (this on a canvas)
"""

#===============================================================================
# Imports
#===============================================================================

from __future__ import annotations

import sys

from collections import ChainMap
from functools import cached_property
from typing import cast, Any, Optional, Union, TYPE_CHECKING

from lxml import etree as ET

from mhi.xml.node import IdNode, ParametersBase, ParamListNode

from mhi.xml.pscad.colour import Colour
from mhi.xml.pscad.types import Arrows, BusType, XY, LineStyle, FillStyle
from mhi.xml.pscad.vertex import Vertex
from mhi.xml.pscad._project import project_lookup, ProjectMixin
from mhi.xml.pscad.layer import Layer


if TYPE_CHECKING:
    from mhi.xml.pscad.schematic import Schematic
    from mhi.xml.pscad.definition import UserCmpDefn


#===============================================================================
# Exports
#===============================================================================


__all__ = ['Component', 'UserCmp',
           'Wire', 'WireOrthogonal', 'WireDiagonal', 'Bus',
           'GroupBox']


#===============================================================================
# Components
#===============================================================================

class Component(IdNode, ProjectMixin):
    """
    A Component
    """


    def __repr__(self):

        classid = self.defn or self.get('classid')
        name = self.name
        return f'{classid}[{name}, #{self.id}]'


    @property
    def classid(self) -> str:
        """
        The classid of the component.

        Typically `"UserCmp"` but other possibilities include `"WireOthogonal"`,
        `"Sticky"`, `"GraphFrame"`, `"ControlFrame"`, and so on.
        """

        classid = self.get('classid')
        assert classid is not None
        return classid


    def _ensure_id(self):

        if 'id' not in self or self.get('id') == '0':
            iid = self._file.make_id()
            self.set('id', str(iid))


    @property
    def location(self) -> XY:
        """
        The (X, Y) location of the component.
        """

        return XY(int(self.get('x', '0')), int(self.get('y', '0')))


    @location.setter
    def location(self, xy: XY) -> None:

        self.set('x', str(xy.x))
        self.set('y', str(xy.y))


    @property
    def canvas(self) -> 'Schematic':
        """
        The canvas the component is on.
        """

        return cast('Schematic', self.getparent())


    @property
    def size(self) -> XY:
        """
        The size (width & height) of the component.
        """

        return XY(int(self.get('w', '0')), int(self.get('h', '0')))


    @size.setter
    def size(self, xy: XY) -> None:

        self.set('w', str(xy.x))
        self.set('h', str(xy.y))


    @property
    def defn(self) -> Optional[str]:
        """
        The component's definition.

        .. Note:

            `None` if the component is not a `UserCmp`.
        """

        return self.get('defn')


    @property
    def scope_and_defn(self) -> tuple[str, str]:
        """
        Returns the component definitions's scope and definition names.

        .. Note:

            The "scope" is the portion before the colon (`:`).
        """

        scope = ''
        defn = self.defn or ''
        if defn:
            if ':' in defn:
                scope, defn = defn.split(':', 1)
        return scope, defn


    @property
    def name(self) -> Optional[str]:
        """
        Returns the component's assigned name value.

        The name must be stored in a parameter called `name, `Name` or `NAME`.
        """

        paramlist = self.params
        if paramlist is None:
            return None
        return next((param.get('value')
                     for param in paramlist.iter('param')
                     if param.get('name', '').casefold() == 'name'), None)


    @cached_property
    def params(self) -> Optional[ParamListNode]:
        """
        The parameter list node of the component

        Individual parameters can be set and retrieved using index notation::

            name = cmp['Name']
            cmp['BaseKV'] = '230.0 [kV]'
        """

        xpath = 'paramlist[@link="-1"][@name=""]'
        param_list = self.find(xpath)
        if param_list is None:
            param_lists = cast(list, self.xpath('paramlist'))
            if param_lists:
                param_list = param_lists[0]

        if param_list is not None:
            return cast(ParamListNode, param_list)

        return None


    def __getitem__(self, key):

        if isinstance(key, str):
            return self.params.get_param(key)
        return super().__getitem__(key)


    def __setitem__(self, key, value):

        if isinstance(key, str):
            self.params.set_param(key, value)
        else:
            super().__setitem__(key, value)


    def __contains__(self, key) -> bool:

        if isinstance(key, str):
            if (params := self.params) is not None:
                return key in params

        return super().__contains__(key)                    # type: ignore[misc]


    def enable(self, state=True) -> None:
        """
        Enable this component

        Note:
            This does not affect whether the component is on a disabled layer.
        """

        disabled = 'false' if state else 'true'
        self.set('disable', disabled)


    def disable(self) -> None:
        """
        Disable this component
        """

        self.enable(False)


    @property
    def enabled(self) -> bool:
        """
        Is this component enabled.

        Note:
            This does not check if the component is on a disabled layer.
        """

        disabled = self.get('disable', 'false')
        return disabled.casefold() == 'false'


    @property
    def layer(self) -> Optional[Layer]:
        """
        The `Layer` the component is on, or `None` if not on any layer.
        """

        tree = self.getroottree()
        layer = tree.find(f'Layers/Layer/ref[@link="{self.id}"]/..')
        if layer is not None:
            return cast('Layer', layer)
        return None


    @layer.setter
    def layer(self, layer: Union[Layer, str, None]) -> None:

        old_layer = self.layer
        if isinstance(layer, str):
            new_layer : Optional[Layer] = self.project.layer[layer]
        else:
            new_layer = layer

        if old_layer is not None:
            if old_layer != new_layer:
                ref = old_layer.find(f'ref[@link="{self.id}"]')
                assert ref is not None
                old_layer.remove(ref)

        if new_layer is not None:
            ref = new_layer.makeelement('ref', link=str(self.id))
            new_layer.append_indented(ref, 4)


    def delete(self) -> None:
        """
        Remove this component from the canvas.
        """

        self._remove_from_parent()


#===============================================================================

@project_lookup.tag('User')
#@project_lookup.classid('UserCmp')
class UserCmp(Component):
    """
    A component with a definition defined in a '.pslx' file
    """


    XML = (
    # pylint: disable-next=line-too-long
     """<User classid="UserCmp" id="0" x="0" y="0" w="18" h="18" z="-1" orient="0" defn="{defn}" link="-1" q="4" disable="false">
          <paramlist name="" link="-1" crc="0" />
        </User>""")

    @property
    def defn(self) -> str:
        """
        The definition of the component
        """

        defn = self.get('defn')
        assert defn is not None
        return defn


    @defn.setter
    def defn(self, new_defn: str) -> None:

        assert new_defn.count(':') == 1

        self.set('defn', new_defn)

        # We've changed definitions, form CRC is invalid
        params = self.params
        assert params is not None
        params.set('crc', '0')


    @property
    def subcanvas(self) -> Optional['Schematic']:
        """
        The component's definition's schematic, in one exists
        """

        project = self.project
        namespace, name = self.defn.split(':', 1)
        if project.namespace == namespace:
            return project.canvas(name)
        return None


    def is_module(self) -> bool:
        """
        Does this component's definition contain a schematic?
        """

        return self.subcanvas is not None


    def remap(self, defn: UserCmpDefn):
        """
        Remamp this User Component to a new User Component Definition
        """

        self.defn = defn.full_name
        self._create_missing_params(defn)


    def _create_missing_params(self, defn: UserCmpDefn):

        params = self.params
        assert params is not None

        for name, param in defn.form.parameter.items():
            if name not in params:
                if param.simple_type:
                    params.create_param(name, param.default)
                else:
                    print(f"Warning: did not create {name} parameter in"
                          f" {self.defn}.  Type {param.type} not yet support",
                          file=sys.stderr)


#===============================================================================

@project_lookup.tag('Wire')
#@project_lookup.classid('Branch')
#@project_lookup.classid('WireBranch')
class Wire(Component):
    """
    Base class for all multi-vertex Wires
    """

    @property
    def _origin(self) -> XY:

        return XY(int(self.get('x', '0')), int(self.get('y', '0')))


    def _add_vertex(self, vtx: XY):
        xml = f'<vertex x="{vtx.x}" y="{vtx.y}" />'
        self.append_text('  ')
        self.append(self._parse(xml))
        self.append_text('\n        ')


    def _vertices(self) -> list[Vertex]:

        return cast(list[Vertex], list(self.iterchildren('vertex')))


    def vertices(self) -> list[Vertex]:
        """
        The list <vertex> elements of a Wire

        These are the raw <vertex> elements, relative to the component's
        origin.  Use Wire.vertex[i] to retrieve the actual canvas vertex
        locations.

        .. versionchanged:: 1.2.0
        """

        return self._vertices()


    @property
    def vertex(self) -> VertexContainer:
        """
        Access an individual vertex of the wire

        Vertex locations are read/write, and are absolute positions on the
        canvas.

        Example:
            wire.vertex[1].x = 18

        .. versionadded:: 1.2.0
        """

        return Wire.VertexContainer(self)


    class VertexContainer:
        """
        A list-type container of Wire vertices

        .. versionadded:: 1.2.0
        """

        def __init__(self, wire):

            self._wire = wire


        def _vertices(self):

            return self._wire.vertices()


        def __len__(self) -> int:

            return len(self._vertices())


        def __getitem__(self, key) -> XY:

            vtx = self._vertices()[key]

            return self._wire._origin + vtx.xy


        def __setitem__(self, key, xy: XY):

            vertex = self._vertices()[key]
            vertex.xy = xy - self._wire._origin


#===============================================================================

@project_lookup.classid('WireOrthogonal')
class WireOrthogonal(Wire):
    """
    An orthogonal wire

    .. versionadded:: 1.2.0
    """

    XML = (
    # pylint: disable-next=line-too-long
     """<Wire classid="WireOrthogonal" id="0" name="" x="{x}" y="{y}" w="{w}" h="{h}" orient="0" disable="false" >
        </Wire>""")

    @staticmethod
    def create_instance(canvas: Schematic, /,
                        *vertices: Union[tuple[int, int], XY],
                        ) -> WireOrthogonal:
        """
        Create an Orthogonal wire on the canvas.

        If more than two vertices are given, a multi-vertex wire will be
        created.
        If any segment is neither horizontal or vertical, additional vertices
        will be inserted.

        Parameters:
            *vertices: A series of (X, Y) pairs, in grid units
        """

        return canvas.add_wire(*vertices)


#===============================================================================

@project_lookup.classid('WireDiagonal')
class WireDiagonal(Wire):
    """
    A Sticky Wire

    .. versionadded:: 1.2.0
    """

    XML = (
    # pylint: disable-next=line-too-long
     """<Wire classid="WireDiagonal" id="0" name="" x="{x}" y="{y}" w="{w}" h="{h}" orient="0" disable="false" >
        </Wire>""")


    @staticmethod
    def create_instance(canvas: Schematic, /,
                        *vertices: Union[tuple[int, int], XY],
                        lead_length: int = 1,
                        lead_directions: Optional[list[XY]] = None
                        ) -> WireDiagonal:
        """
        Create new sticky wire on the canvas.
        """

        return canvas.add_sticky_wire(*vertices,
                                      lead_length=lead_length,
                                      lead_directions=lead_directions)


    def vertices(self) -> list[Vertex]:
        """
        The list <vertex> elements of a Sticky Wire

        These are the raw <vertex> elements, relative to the component's
        origin.  Use Wire.vertex[i] to retrieve the actual canvas vertex
        locations.
        """

        vertices = self._vertices()

        return vertices[0:1] + vertices[3::2]


    @property
    def vertex(self) -> WireDiagonal.VertexContainer:
        """
        Access an individual end-point vertex of a sticky wire

        Vertex locations are absolute positions on the canvas.  Setting a new
        vertex location will move the corresponding lead vertex by the same
        amount.
        """

        return WireDiagonal.VertexContainer(self)


    def leads(self) -> list[Vertex]:
        """
        The list <vertex> elements of the lead vertices of a Sticky Wire

        These are the raw <vertex> elements, relative to the component's
        origin.  Use StickyWire.lead[i] to retrieve the actual canvas vertex
        locations.
        """

        vertices = self._vertices()

        return vertices[1:2] + vertices[2::2]


    @property
    def lead(self) -> WireDiagonal.LeadContainer:
        """
        Access the sticky wire's end-point lead's vertex.

        Vertex locations are absolute positions on the canvas.  The lead
        vertex position must always share either the same x-value or the same
        y-value, but not both, to keep the lead horizontal or vertical.
        """

        return WireDiagonal.LeadContainer(self)


    class VertexContainer(Wire.VertexContainer): # pylint: disable=too-few-public-methods
        """
        A list-type container of StickyWire vertices

        .. versionadded:: 1.2.0
        """

        def __setitem__(self, key, xy: XY):

            vtx = self._wire.vertices()[key]
            lead = self._wire.leads()[key]
            delta = vtx.xy - xy
            vtx.xy += delta
            lead.xy += delta


    class LeadContainer(Wire.VertexContainer): # pylint: disable=too-few-public-methods
        """
        A list-type container of StickyWire lead vertices

        .. versionadded:: 1.2.0
        """

        def _vertices(self):

            return self._wire.leads()


        def __setitem__(self, key, xy: XY):

            vtx = self._wire.vertices()[key].xy + self._wire._origin

            horiz = vtx.x == xy.x
            vert = vtx.y == xy.y

            if horiz == vert:
                raise ValueError("Invalid lead position")

            lead = self._wire.leads()[key]
            lead.xy = xy - self._wire._origin


#===============================================================================

@project_lookup.classid('Bus')
class Bus(Wire):
    """
    A Bus

    .. versionadded:: 1.2.0
    """

    Type = BusType


    XML = (
    # pylint: disable-next=line-too-long
     """<Wire classid="Bus" id="0" name="" x="{x}" y="{y}" w="{w}" h="{h}" orient="0" disable="false">
          <paramlist link="-1">
            <param name="Name" value="{Name}" />
            <param name="BaseKV" value="{BaseKV}" />
            <param name="Vrms" value="0" />
            <param name="VA" value="{VA}" />
            <param name="VM" value="{VM}" />
            <param name="type" value="{type}" />
          </paramlist>
        </Wire>""")


    @staticmethod
    def create_instance(canvas: Schematic, /,
                        *vertices: Union[tuple[int, int], XY],
                        Name: str = "",
                        BaseKV: float = 0.0,
                        VM: float = 1.0,
                        VA: float = 0.0,
                        type: BusType = BusType.AUTO # pylint: disable=redefined-builtin
                        ) -> Bus:
        """
        Create a Bus on the canvas.

        If more than two vertices are given, a multi-vertex bus will be
        created.
        If any segment is neither horizontal or vertical, additional vertices
        will be inserted.
        """

        return canvas.add_bus(*vertices, Name=Name, BaseKV=BaseKV,
                              VM=VM, VA=VA, type=type)


    @property
    def parameters(self) -> Bus.Parameters:
        """
        Retrieve the Bus's Parameters
        """

        return self.Parameters(self.find('paramlist'))


    #-----------------------------------------------------------------------

    class Parameters(ParametersBase):
        """
        Bus parameters
        """

        name: str
        BaseKV: float
        VA: float
        VM: float
        type: BusType


#===============================================================================

class TravelingWaveModelWire(Wire):
    """
    Base class for all Traveling Wave Model Wires (TLine/Cable)
    """

    @property
    def user(self) -> UserCmp:
        """
        Return the user component embedded in the Traveling Wave Model Wire
        """

        user = self.find('User')
        assert user is not None

        return cast(UserCmp, user)


    @property
    def params(self) -> ParamListNode:
        """
        Return the parameter list node for the Traveling Wave Model Wire
        """

        return cast(ParamListNode, self.user.params)


    @property
    def subcanvas(self) -> Optional['Schematic']:
        """
        Return the schematic canvas for the Traveling Wave Model Wire
        """

        namespace, name = self.user.defn.split(':', 1)

        project = self.project
        if namespace == project.namespace:
            return project.canvas(name)

        return None


#-------------------------------------------------------------------------------

@project_lookup.classid('TLine')
class TLine(TravelingWaveModelWire):
    """The PSCAD <TLine/> node class"""

    def __repr__(self) -> str:
        return f"TLine[{self.name}]"


#-------------------------------------------------------------------------------

@project_lookup.classid('Cable')
class Cable(TravelingWaveModelWire):
    """The PSCAD <Cable/> node class"""

    def __repr__(self) -> str:
        return f"Cable[{self.name}]"


#===============================================================================
# Annotations
#===============================================================================

@project_lookup.tag('Line')
class Line(Component):
    """The PSCAD <Line/> node class"""


#===============================================================================

@project_lookup.classid('Divider')
class Divider(Component):
    """The PSCAD Divider <Line/> node class"""

    _XML = (
     '''<Line classid="Divider" id="0" name="" x="18" y="18" w="{w}" h="{h}" orient="{orient}">
          <paramlist>
            <param name="state" value="1" />
            <param name="true-color" value="0" />
            <param name="style" value="0" />
            <param name="weight" value="2" />
            <param name="color" value="0" />
          </paramlist>
        </Line>''')

    @classmethod
    def create_instance(cls,
                        canvas: Schematic,
                        x: int = 1, y: int = 1, w: int = 0, h: int = 0,
                        **kwargs
                        ) -> Divider:
        """
        Create a Divider on the canvas.

        .. versionadded: 1.2.0
        """

        if w and h:
            raise ValueError("Cannot specify both width and height for divider")
        if not w or not h:
            w = 6
        orient = 1 if h else 0

        xml = cls._XML.format(w=w*18, h=h*18, orient=orient)
        divider = cast(Divider, canvas._parse(xml)) # pylint: disable=protected-access

        if kwargs:
            for key, val in kwargs.items():
                divider[key] = val

        canvas.add(divider, x*18, y*18)

        return divider


    @property
    def parameters(self) -> Divider.Parameters:
        """
        Retrieve the Divider's Parameters
        """

        return self.Parameters(self.find('paramlist'))


    #-----------------------------------------------------------------------

    class Parameters(ParametersBase):
        """
        Divider parameters
        """

        state: int
        style: LineStyle
        weight: int
        color: Colour


#===============================================================================

@project_lookup.classid('Groupbox')
class GroupBox(Component):
    """A PSCAD Group Box <Line/> node class"""

    _XML = (
     '''<Line id="0" classid="GroupBox" x="18" y="18" w="{w}" h="{h}">
          <paramlist>
            <param name="name" value="Groupbox" />
            <param name="show_name" value="true" />
            <param name="font" value="Tahoma, 13world" />
            <param name="line_style" value="0" />
            <param name="line_weight" value="0" />
            <param name="line_colour" value="#FF000000" />
            <param name="fill_style" value="0" />
            <param name="fill_fg" value="#FFFFE4B5" />
            <param name="fill_bg" value="#FFFFFFFF" />
          </paramlist>
        </Line>''')

    @classmethod
    def create_instance(cls,
                        canvas: Schematic,
                        x: int = 1, y: int = 1, w: int = 11, h: int = 6, *,
                        name: str = "Groupbox",
                        **kwargs
                        ) -> GroupBox:
        """
        Create a Group Box on the canvas.

        .. versionadded: 1.2.0
        """

        xml = cls._XML.format(w=w*18, h=h*18)
        group_box = cast(GroupBox, canvas._parse(xml)) # pylint: disable=protected-access

        group_box['name'] = name
        if kwargs:
            for key, val in kwargs.items():
                group_box[key] = val

        canvas.add(group_box, x*18, y*18)

        return group_box


    @property
    def parameters(self) -> GroupBox.Parameters:
        """
        Retrieve the Group Box's Parameters
        """

        return self.Parameters(self.find('paramlist'))


    #-----------------------------------------------------------------------

    class Parameters(ParametersBase):
        """
        Group Box parameters
        """

        name: str
        show_name: bool
        font: str
        line_style: LineStyle
        line_weight: int
        line_colour: Colour
        fill_style: FillStyle
        fill_fg: Colour
        fill_bg: Colour


#===============================================================================

@project_lookup.tag('Sticky')
#@project_lookup.classid('Sticky')
class Sticky(Component):
    """The PSCAD <Sticky/> node class"""

    XML = (
     '''<Sticky classid="Sticky" id="0" x="0" y="0" w="{w}" h="{h}" colors="0, 15792890">
          <paramlist>
            <param name="full_font" value="Tahoma, 12world" />
            <param name="align" value="0" />
            <param name="style" value="1" />
            <param name="arrows" value="0" />
            <param name="fg_color_adv" value="#FF000000" />
            <param name="bg_color_adv" value="#FFFAFAF0" />
            <param name="hl_color_adv" value="#FFFFFF00" />
            <param name="bdr_color_adv" value="#FF95918C" />
          </paramlist><![CDATA[]]></Sticky>'''
     )

    @staticmethod
    def create_instance(canvas: Schematic,
                        x: int = 1, y: int = 1, w: int = 6, h: int = 2,
                        text: str = "Sticky Note",
                        **kwargs) -> Sticky:
        """
        Create a Sticky Note on the canvas.

        .. versionadded: 1.2.0
        """

        xml = Sticky.XML.format(w=w*18, h=h*18)
        sticky = cast(Sticky, canvas._parse(xml)) # pylint: disable=protected-access

        if kwargs:
            for key, val in kwargs.items():
                sticky[key] = val
        sticky.text = text

        canvas.add(sticky, x*18, y*18)

        return sticky


    @property                                           # type: ignore[override]
    def text(self) -> str:
        """
        Sticky Note contents"
        """

        paramlist = self.params
        assert paramlist is not None
        assert paramlist.tail is not None

        return paramlist.tail


    @text.setter
    def text(self, text: str) -> None:

        paramlist = self.params
        assert paramlist is not None

        paramlist.tail = ET.CDATA(text)


    @property
    def parameters(self) -> Sticky.Parameters:
        """
        Retrieve the Bus's Parameters
        """

        return self.Parameters(self.find('paramlist'))


    #-----------------------------------------------------------------------

    class Parameters(ParametersBase):
        """
        Sticky parameters
        """

        full_font: str
        align: int
        style: int
        arrows: Arrows
        fg_color_adv: Colour
        bg_color_adv: Colour
        hl_color_adv: Colour
        bdr_color_adv: Colour


#===============================================================================

@project_lookup.tag('Link')
#@project_lookup.classid('UrlCmp')
class UrlCmp(Component):
    """The PSCAD UrlCmp <Link/> node class"""

    _XML = (
     '''<Link classid="UrlCmp" id="0" x="72" y="432" z="-1" orient="0" link="-1" q="4">
          <paramlist>
            <param name="display" value="" />
            <param name="hyperlink" value="" />
          </paramlist>
        </Link>''')

    @classmethod
    def create_instance(cls,
                        canvas: Schematic,
                        x: int = 1, y: int = 1,
                        display: str = "https://mhi.ca/",
                        hyperlink: str = "https://mhi.ca/"
                        ) -> UrlCmp:
        """
        Create a UrlCmp on the canvas.

        .. versionadded: 1.2.0
        """

        xml = cls._XML.format()
        url_cmp = cast(UrlCmp, canvas._parse(xml)) # pylint: disable=protected-access

        url_cmp['display'] = display
        url_cmp['hyperlink'] = hyperlink

        canvas.add(url_cmp, x*18, y*18)

        return url_cmp


    @property
    def parameters(self) -> UrlCmp.Parameters:
        """
        Retrieve the UrlCmp's Parameters
        """

        return self.Parameters(self.find('paramlist'))


    #-----------------------------------------------------------------------

    class Parameters(ParametersBase):
        """
        UrlCmp parameters
        """

        display: str
        hyperlink: str

#===============================================================================

@project_lookup.tag('Instrument')
#@project_lookup.classid('PhasorMeter')
#@project_lookup.classid('PolyMeter')
class Instrument(Component):
    """The PSCAD <Instrument/> node class"""


#===============================================================================

@project_lookup.tag('Frame')
#@project_lookup.classid('ControlFrame')
class Frame(Component):
    """The PSCAD <Frame/> node class"""

    XML = (
     '''<Frame classid="{classid}" x="0" y="0" w="{w}" h="{h}" name="{name}" link="-1">
          <paramlist link="-1">
            <param name="Icon" value="-1,-1" />
            <param name="state" value="1" />
          </paramlist>
        </Frame>''')


    @staticmethod
    def _create(canvas: Schematic, classid: str, x: int, y: int, w: int, h: int,
                name: str, default_params: dict[str, Any], **kwargs) -> Frame:

        unknown = {key for key in kwargs if key not in default_params}
        if unknown:
            raise KeyError(f"Unknown parameters: {', '.join(unknown)}")
        params: dict[str, Any] = ChainMap(kwargs, default_params) # type: ignore[assignment]

        xml = Frame.XML.format(classid=classid, w=w*18, h=h*18, name=name)
        frame = cast(Frame, canvas._parse(xml)) # pylint: disable=protected-access

        paramlist = frame.params
        assert paramlist is not None
        paramlist.create_params(params)

        canvas.add(frame, x*18, y*18)

        return frame


#-------------------------------------------------------------------------------

@project_lookup.classid('GraphFrame')
class GraphFrame(Frame):
    """A Graph Frame"""

    DEFAULT_PARAMS = {
        "title": "$(GROUP) : Graphs",
        "markers": False,
        "pan_enable": False,
        "pan_amount": 75,
        "xtitle": "sec",
        "xgridauto": True,
        "xgrid": 0.1,
        "xfont": "Tahoma, 12world",
        "xangle": 0,
        "lockmarkers": False,
        "deltareadout": False,
        "xmarker": 0,
        "omarker": 0,
        "XLabel": "sec",
        "Pan": False,
        "glyphs": False,
        "ticks": False,
        "grid": False,
        "yinter": False,
        "xinter": False,
        "semilog": False,
        "snapaperture": False,
        "dynaperture": True,
        "minorgrids": False,
        }

    @classmethod
    def create_instance(cls, canvas: Schematic,
                        x: int = 1, y: int = 1, w: int = 32, h: int = 16, /,
                        **kwargs) -> GraphFrame:
        """
        Create a Graph Frame on the canvas.

        .. versionadded: 1.2.0
        """

        frame = cls._create(canvas, 'GraphFrame', x, y, w, h, 'frame',
                            cls.DEFAULT_PARAMS, **kwargs)
        graph_frame = cast(GraphFrame, frame)

        alt_pl = frame.create_param_list_node(name='', link=graph_frame.id)
        alt_pl.create_param('xmin', 0.0)
        alt_pl.create_param('xmax', 1.0)

        return graph_frame


#-------------------------------------------------------------------------------

@project_lookup.classid('PlotFrame')
class PlotFrame(Frame):
    """An XY Plot Frame"""

    DEFAULT_PARAMS = {
        "title": "$(GROUP) : Graphs",
        "glyphs": False,
        "ticks": False,
        "grid": False,
        "yinter": False,
        "xinter": False,
        "xhair": False,
        "snaptogrid": False,
        "aspect": False,
        "tracestyle": 0,
        "grid_color": "#FF95908C",
        "curve_colours": "Navy;Green;Maroon;Teal;Purple;Brown",
        "curve_colours2": "Blue;Lime;Red;Aqua;Fuchsia;Yellow",
        "invertcolors": False,
        "markers": 0,
        "xmarker": 0,
        "omarker": 0,
        "mode": 0,
        "autocolor": False,
        }

    @classmethod
    def create_instance(cls, canvas: Schematic,
                        x: int = 1, y: int = 1, w: int = 18, h: int = 20, /,
                        **kwargs) -> PlotFrame:
        """
        Create an XY Plot Frame on the canvas.

        .. versionadded: 1.2.0
        """

        frame = cls._create(canvas, 'PlotFrame', x, y, w, h, 'PlotFrame',
                            cls.DEFAULT_PARAMS, **kwargs)
        plot_frame = cast(PlotFrame, frame)

        alt_pl = plot_frame.create_param_list_node(name='', link=plot_frame.id)
        alt_pl.create_param('xmin', 0.0)
        alt_pl.create_param('xmax', 1.0)

        return plot_frame


#===============================================================================

class ControlFrame(Frame):
    """A Control Frame"""

    DEFAULT_PARAMS = {
        "title": "$(GROUP) : Controls",
        }

    @classmethod
    def create_instance(cls, canvas: Schematic,
                        x: int = 1, y: int = 1, w: int = 4, h: int = 7, /,
                        **kwargs) -> ControlFrame:
        """
        Create a Control Frame on the canvas.

        .. versionadded: 1.2.0
        """

        frame = cls._create(canvas, 'ControlFrame', x, y, w, h, '',
                            cls.DEFAULT_PARAMS, **kwargs)
        control_frame = cast(ControlFrame, frame)

        return control_frame


#===============================================================================

@project_lookup.tag('FileCmp')
class FileCmp(Component):
    """The PSCAD <FileCmp/> node class"""

    _XML = (
     '''<FileCmp classid="FileCmp" id="0" x="18" y="18" w="72" h="54" disable="false">
          <paramlist>
            <param name="name" value="" />
            <param name="filepath" value="" />
          </paramlist>
        </FileCmp>''')

    @classmethod
    def create_instance(cls,
                        canvas: Schematic,
                        x: int = 1, y: int = 1,
                        name: str = "untitled",
                        filepath: str = "$(ProjectDir)\\untitled.f"
                        ) -> FileCmp:
        """
        Create a Sticky Note on the canvas.

        .. versionadded: 1.2.0
        """

        xml = cls._XML.format()
        filecmp = cast(FileCmp, canvas._parse(xml)) # pylint: disable=protected-access

        filecmp['name'] = name
        filecmp['filepath'] = filepath

        canvas.add(filecmp, x*18, y*18)

        return filecmp

"""
XML entities for PSCAD schematics
"""

#===============================================================================
# Imports
#===============================================================================

from __future__ import annotations

from typing import cast, Iterable, Iterator, Optional, Union, TYPE_CHECKING

from mhi.xml.node import XmlNode, ParametersBase, ParamListNode
from mhi.xml.pscad._project import project_lookup, ProjectMixin

from mhi.xml.pscad.types import XY, UP, DOWN, LEFT, RIGHT, BusType
from mhi.xml.pscad.component import (Component, UserCmp,
                                     Bus, WireOrthogonal, WireDiagonal)

if TYPE_CHECKING:
    from mhi.xml.pscad.definition import Definition


#===============================================================================
# Exports
#===============================================================================

__all__ = ['Schematic', ]


#===============================================================================
# Schematic Canvases
#===============================================================================

@project_lookup.tag('schematic')
class Schematic(XmlNode, ProjectMixin):
    """
    A canvas which contains a set of components.
    """

    @staticmethod
    def _xpath(xpath: Optional[str],
               classid: Optional[str],
               defn: Optional[str],
               with_params: Optional[set[str]],
               params: Optional[dict[str, str]]
               ) -> str:

        if xpath:
            if classid or defn or with_params or params:
                raise ValueError(
                    f"xpath cannot be used with classid/defn/params\n"
                    f"    xpath={xpath}\n"
                    f"    classid={classid}\n"
                    f"    defn={defn}\n"
                    f"    with_params={with_params}\n"
                    f"    params={params}")
            return xpath

        parts = []
        node = "*"
        if classid is not None:
            node += f"[@classid={classid!r}]" if classid else "[@classid]"
        if defn:
            node += f"[@defn={defn!r}]"
        parts.append(node)

        if params or with_params:
            parts.append('paramlist')
            if params:
                parts.extend(f"param[@name={name!r}][@value={value!r}]/.."
                             for name, value in params.items())
            if with_params:
                if params:
                    with_params = with_params - params.keys()
                parts.extend(f"param[@name={name!r}]/.."
                             for name in with_params)
            parts.append("..")

        xpath = "/".join(parts)

        return xpath


    def __repr__(self):

        classid = self.get('classid', 'Unknown!')
        return f'{classid}[{self.name!r}]'


    def __iter__(self):

        yield from self.xpath("*[@classid]")


    def find_by_id(self, iid: int) -> Optional[Component]:
        """
        Find a component by is PSCAD `id` number
        """

        return cast(Optional[Component], self.find(f"*[@id='{iid}']"))


    @property
    def name(self) -> str:
        """
        Name of the schematic's definition
        """

        return self.definition.name


    @property
    def definition(self) -> 'Definition':
        """
        Definition the schematic is part of
        """

        return cast('Definition', self.getparent())


    def components(self,
                   name: Optional[str] = None, /, *,
                   defn: Optional[str] = None,
                   include_defns: Optional[set[str]] = None,
                   exclude_defns: Optional[set[str]] = None,
                   xpath: Optional[str] = None,
                   classid: Optional[str] = None,
                   with_params: Optional[set[str]] = None,
                   **params) -> Iterator[Component]:
        """
        Component search

        Find the components within the canvas identified by the provided
        arguments.  All arguments are optional.  The name parameter, if
        given, must be the first and only positional parameter.  All other
        parameters must be keyword parameters.

        :param str name: Name of the component (positional parameter only)
        :param str classid: Component class identifier
        :param str defn: Definition name
        :param set[str] include_defns: Definition names to include in search
        :param set[str] exclude_defns: Definition names to exclude from search
        :param set[str] with_params: Only components with have the given parameters
        :param key=value: Components with the given parameter key=value pairs

        At most one of `defn`, `include_defns` or `exclude_defns` may be
        provided.
        """

        xpath = self._xpath(xpath, classid, defn, with_params, params)

        if name:
            name = name.casefold()

        cmps = cast(list[Component], self.xpath(xpath))
        for cmp in cmps:
            if cmp.tag in {'paramlist', 'grouping'}:
                continue
            if name is not None:
                cmp_name = cmp.name
                if cmp_name is None or cmp_name.casefold() != name:
                    continue
            if include_defns and cmp.defn not in include_defns:
                continue
            if exclude_defns and cmp.defn in exclude_defns:
                continue
            yield cmp


    def component(self,
                  name: Optional[str] = None, /, *,
                  defn: Optional[str] = None,
                  include_defns: Optional[set[str]] = None,
                  exclude_defns: Optional[set[str]] = None,
                  xpath: Optional[str] = None,
                  raise_if_not_found: bool = False,
                  classid: Optional[str] = None,
                  with_params: Optional[set[str]] = None,
                  **params) -> Optional[Component]:
        """
        Component search

        Find the component within the canas identified by the provided
        arguments.  All arguments are optional.  The name parameter, if
        given, must be the first and only positional parameter.  All
        other parameters must be keyword parameters.

        :param str name: Name of the component (positional parameter only)
        :param str classid: Component class identifier
        :param str defn: Definition name
        :param set[str] include_defns: Definition names to include in search
        :param set[str] exclude_defns: Definition names to exclude from search
        :param bool raise_if_not_found: Raise an exception if component isn't found (default: False)
        :param set[str] with_params: Only components with have the given parameters
        :param key=value: Components with the given parameter key=value pairs

        At most one of `defn`, `include_defns` or `exclude_defns` may be
        provided.
        """

        xpath = self._xpath(xpath, classid, defn, with_params, params)
        comps = list(self.components(name, xpath=xpath,
                                     include_defns=include_defns,
                                     exclude_defns=exclude_defns))

        if len(comps) == 0:
            if raise_if_not_found:
                raise NameError(f"Component {xpath!r} not found")
            return None
        if len(comps) > 1:
            raise NameError(f"Multiple components {xpath!r} found ({len(comps)})")

        return comps[0]


    def page_modules(self) -> Iterator[UserCmp]:
        """
        Retrieve the page module components on the canvas
        """

        project = self.project
        project_namespace = project.namespace
        for user in self.iterfind('User[@classid="UserCmp"]'):
            user = cast(UserCmp, user)
            namespace, name = user.defn.split(':', 1)
            if namespace == project_namespace:
                canvas = project.canvas(name)
                if canvas is not None:
                    yield user

    def remove_components(self, component, *components) -> None:
        """
        Remove listed components from the schematic
        """

        self.remove(component)

        for cmp in components:
            self.remove(cmp)


    def remove(self, component) -> None:
        """
        Remove the given components from the schematic
        """

        iid = component.id
        super().remove(component)
        if iid:
            refs = cast(list[XmlNode],
                        self.xpath(f'/Layers/Layer/ref[@id="{iid}"]'))
            for ref in refs:
                ref._remove_from_parent()     # pylint: disable=protected-access


    def add(self, component, x, y, orient=None) -> None:
        """
        Add a component to the schematic at the given XY location.
        If an orientation is specified, set that as well.
        """

        self.append_indented(component)

        component.location = XY(x, y)
        if orient is not None:
            component.set('orient', str(orient))

        component._ensure_id()                # pylint: disable=protected-access


    def create(self, defn: str, **kwargs) -> UserCmp:
        """
        Create a new User Component from a definition.
        """

        xml = UserCmp.XML.format(defn=defn)
        component = cast(UserCmp, self._parse(xml))

        if kwargs:
            paramlist = cast(ParamListNode, component.find('paramlist'))
            paramlist.create_params(kwargs)

        return cast(UserCmp, component)


    @staticmethod
    def _xy(vertices: Iterable[Union[tuple[int, int], XY]]) -> list[XY]:
        """
        Convert vertices to list[XY]
        """

        return [vtx if isinstance(vtx, XY) else XY(*vtx) for vtx in vertices]


    @staticmethod
    def _orthogonal(vertices) -> list[XY]:
        """
        Turn a list of [x,y] pairs into a list of [x,y] pairs where
          - successive vertices are different
          - successive vertices are either horizontal or vertical
        """

        if len(vertices) < 2:
            raise ValueError("At least two vertices must be supplied")

        vertexes = []

        it = iter(vertices)
        vtx = next(it)
        prev = vtx
        vertexes.append(vtx)

        for vtx in it:
            if vtx != prev:
                if vtx.x != prev.x and vtx.y != prev.y:
                    vertexes.append(XY(prev.x, vtx.y))
                vertexes.append(vtx)
                prev = vtx

        return vertexes


    @staticmethod
    def _zero_offset(vertices: list[XY]) -> tuple[int, int, list[XY]]:
        """
        Remove the initial offset from all vertices
        """

        vtx0 = vertices[0]

        return vtx0.x, vtx0.y, [vtx - vtx0 for vtx in vertices]


    @staticmethod
    def _width_height(vertices) -> tuple[int, int]:
        """
        Remove the initial offset from all vertices
        """

        min_x = min(vtx.x for vtx in vertices)
        max_x = max(vtx.x for vtx in vertices)
        min_y = min(vtx.y for vtx in vertices)
        max_y = max(vtx.y for vtx in vertices)

        w = max_x - min_x + 10
        h = max_y - min_y + 10

        return w, h


    def add_wire(self, *vertices: Union[tuple[int, int], XY]) -> WireOrthogonal:
        """add_wire( (x1,y1), (x2,y2), [... (xn,yn) ...])
        Create an Orthogonal wire on the canvas.

        If more than two vertices are given, a multi-vertex wire will be
        created.
        If any segment is neither horizontal or vertical, additional vertices
        will be inserted.

        Parameters:
            *vertices: A series of (X, Y) pairs, in grid units

        .. versionadded:: 1.2.0
        """

        vertexes = self._xy(vertices)
        vertexes = self._orthogonal(vertexes)
        x, y, vertexes = self._zero_offset(vertexes)
        w, h = self._width_height(vertexes)

        xml = WireOrthogonal.XML.format(x=x, y=y, w=w, h=h)
        wire = cast(WireOrthogonal, self._parse(xml))
        for vtx in vertexes:
            wire._add_vertex(vtx)             # pylint: disable=protected-access

        self.append_indented(wire)

        wire._ensure_id()                     # pylint: disable=protected-access

        return wire


    def add_bus(self,
                *vertices: Union[tuple[int, int], XY], Name: str = "",
                BaseKV: float = 0.0, VM: float = 1.0, VA: float = 0.0,
                type: BusType = BusType.AUTO # pylint: disable=redefined-builtin
                ) -> Bus:
        """add_bus( (x1,y1), (x2,y2), [... (xn,yn) ...])
        Create a Bus on the canvas.

        If more than two vertices are given, a multi-vertex bus will be
        created.
        If any segment is neither horizontal or vertical, additional vertices
        will be inserted.

        .. versionadded:: 1.2.0
        """

        vertexes = self._xy(vertices)
        vertexes = self._orthogonal(vertexes)
        x, y, vertexes = self._zero_offset(vertexes)
        w, h = self._width_height(vertexes)

        xml = Bus.XML.format(Name=Name, BaseKV=BaseKV, VM=VM, VA=VA,
                             type=type, x=x, y=y, w=w, h=h)
        bus = cast(Bus, self._parse(xml))
        for vtx in vertexes:
            bus._add_vertex(vtx)              # pylint: disable=protected-access

        self.append_indented(bus)

        bus._ensure_id()                      # pylint: disable=protected-access

        return bus


    def add_sticky_wire(self,                  # pylint: disable=too-many-locals
                        *vertices: Union[tuple[int, int], XY],
                        lead_length: int = 1,
                        lead_directions: Optional[list[XY]] = None
                        ) -> WireDiagonal:
        """add_sticky_wire( (x1,y1), (x2,y2), [... (xn,yn) ...],
                             lead_length: int, lead_direction: list[XY])
        Create new sticky wire on the canvas.

        .. versionadded:: 1.2.0
        """

        vertexes = self._xy(vertices)
        num_vertices = len(vertexes)
        if num_vertices < 2:
            raise ValueError("Must have at least two vertices")
        if not lead_directions:
            lead_directions = []
            cx = sum(vtx.x for vtx in vertexes) / num_vertices
            cy = sum(vtx.y for vtx in vertexes) / num_vertices

            for vtx in vertexes:
                dx = vtx.x - cx
                dy = vtx.y - cy
                if abs(dx) > abs(dy):
                    lead_directions.append(LEFT if dx > 0 else RIGHT)
                else:
                    lead_directions.append(UP if dy > 0 else DOWN)
        elif len(lead_directions) != num_vertices:
            raise ValueError("Number of lead directions must match vertices")

        leads = [xy + lead_dir * lead_length
                 for xy, lead_dir in zip(vertexes, lead_directions)]
        vertexes = [xy for pair in zip(leads, vertexes) for xy in pair]
        vertexes[:2] = vertexes[1::-1]

        x, y, vertexes = self._zero_offset(vertexes)
        w, h = self._width_height(vertexes)

        xml = WireDiagonal.XML.format(x=x, y=y, w=w, h=h)
        wire = cast(WireDiagonal, self._parse(xml))
        for vtx in vertexes:
            wire._add_vertex(vtx)             # pylint: disable=protected-access

        self.append_indented(wire)

        wire._ensure_id()                     # pylint: disable=protected-access

        return wire


    @property
    def parameters(self) -> Schematic.Parameters:
        """
        Retrieve the Schematic's Parameters
        """

        return self.Parameters(self.find('paramlist'))


    #-----------------------------------------------------------------------

    class Parameters(ParametersBase):
        """
        Schematic parameters
        """

        # All canvases
        show_grid: int
        size: int
        orient: int
        show_border: int

        # Additional user canvas parameters
        show_signal: int
        show_virtual: int
        show_sequence: int
        auto_sequence: int
        monitor_bus_voltage: int
        show_terminals: int
        virtual_filter: str
        animation_freq: int

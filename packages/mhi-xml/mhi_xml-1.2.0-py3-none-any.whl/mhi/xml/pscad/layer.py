"""
XML entities for PSCAD schematic layers
"""

#===============================================================================
# Imports
#===============================================================================

from __future__ import annotations

from typing import cast, Iterator, TYPE_CHECKING

from mhi.xml.node import XmlNode, NamedIdNode, KeyMapping, ParametersBase
from mhi.xml.pscad._project import project_lookup, ProjectMixin

if TYPE_CHECKING:
    from mhi.xml.pscad.component import Component


#===============================================================================
# Exports
#===============================================================================


__all__ = ['LayerMapping',
           'Layer',
           'Layers',
           ]


#===============================================================================
# Blue-Green-Red to Colour
#===============================================================================

def bgr(x):
    """
    Convert BGR to RGB (or vis-versa)
    """

    return int.from_bytes(x.to_bytes(3, 'little'), 'big', signed=False)


#===============================================================================
# Layers
#===============================================================================

@project_lookup.tag('Layer')
class Layer(NamedIdNode, ProjectMixin):
    """
    A project layer
    """

    @property
    def parameters(self) -> Layer.Parameters:
        """
        Retrieve the Layer Parameters object
        """

        return self.Parameters(self.find('paramlist'))


    @property
    def state(self) -> str:
        """
        The layer's state.

        Possible values are 'Enabled', 'Disabled', 'Visible',
        or a custom user state.
        """


        return self.get('state', 'Enabled')


    @state.setter
    def state(self, state: str) -> None:

        self.set('state', state)


    @property
    def disabled(self) -> bool:
        """
        True if the layer's state is 'Disabled' (read-only)
        """

        return self.state.casefold() == 'disabled'


    @property
    def enabled(self) -> bool:
        """
        True if the layer's state is 'Enabled' (read-only)
        """

        return self.state.casefold() == 'enabled'


    @property
    def ids(self) -> set[int]:
        """
        Return the set of ids which belong to the layer.
        """

        return {int(ref.get('link', '0'))
                for ref in self.iterfind('ref')}


    def components(self) -> Iterator[Component]:
        """
        Return all components which belong to the layer.

        .. versionadded:: 1.2.0
        """

        project = self.project
        ids = self.ids
        xpath = 'definitions/Definition/schematic/*[@id]'
        for node in cast(Iterator[Component], project.root.xpath(xpath)):
            cmp = cast('Component', node)
            if cmp.id in ids:
                yield cmp


    def delete_components(self) -> None:
        """
        Remove all components on the layer

        .. versionadded:: 1.2.0
        """

        components = self.components()
        for cmp in components:
            cmp.delete()


    def delete(self):
        """
        Remove this layer
        """

        self._remove_from_parent()


    def __eq__(self, other):
        if isinstance(other, Layer):
            return self.id == other.id
        return False


    def __ne__(self, other):
        if isinstance(other, Layer):
            return self.id != other.id
        return True


    def __repr__(self):
        return f"Layer[{self.name}, state={self.state!r}]"


    class Parameters(ParametersBase):
        """
        Layer Parameters
        """

        disabled_color: str
        disabled_opacity: int
        highlight_color: str
        highlight_opacity: int


#===============================================================================

_LAYER_XML = (
 """<Layer classid="Layer" name="{name}" state="{state}" id="{id}">
      <paramlist>
        <param name="disabled_color" value="#FF{disabled_color:06X}" />
        <param name="disabled_opacity" value="{disabled_opacity}" />
        <param name="highlight_color" value="#FF{highlight_color:06X}" />
        <param name="highlight_opacity" value="{highlight_opacity}" />
      </paramlist>
    </Layer>""")


@project_lookup.tag('Layers')
class Layers(XmlNode, ProjectMixin):
    """
    Project <Layers/> container
    """


class LayerMapping(KeyMapping[Layer]):
    """
    The project's :class:`.Layer` dictionary

    Examples::

        # Create a layer
        layer = project.layer.create('Layer1')

        # Set layer properties
        layer.state = 'Invisible'
        layer.parameters.disabled_color = 0xAA8866
        layer.parameters.disabled_opacity = 128
        layer.parameters.highlight_color = 0x76FF7A
        layer.parameters.highlight_opacity = 100

        # Delete a layer
        del project.layer['Layer1']
    """

    _container: Layers

    def create(self,
               name: str, *,
               state: str = 'Enabled',
               disabled_color: int = 13616578,
               disabled_opacity: int = 128,
               highlight_color: int = 7798650,
               highlight_opacity: int = 100) -> Layer:
        """
        Create a new layer
        """

        if name in self:
            raise KeyError(f"Layer {name!r} already exists")

        name = name.strip()
        state = state.strip()
        disabled_color = int(disabled_color)
        disabled_opacity = int(disabled_opacity)
        highlight_color = int(highlight_color)
        highlight_opacity = int(highlight_opacity)

        if not name.isidentifier():
            raise ValueError(f"Illegal name: {name}")
        if not state.isidentifier():
            raise ValueError(f"Illegal state: {state}")
        for color in (disabled_color, highlight_color):
            if color not in range(0, 0x1_00_00_00):
                raise ValueError(f"Illegal color: {color}")
        for opacity in (disabled_opacity, highlight_opacity):
            if opacity not in range(0, 256):
                raise ValueError(f"Illegal opacity: {opacity}")


        prj = self._container.project
        iid = prj.make_id()

        layer_xml = _LAYER_XML.format(name=name, state=state, id=iid,
                                      disabled_color=bgr(disabled_color),
                                      disabled_opacity=disabled_opacity,
                                      highlight_color=bgr(highlight_color),
                                      highlight_opacity=highlight_opacity)

        layer = cast(Layer, prj._parse(layer_xml))  # pylint: disable=protected-access
        self._container.append_indented(layer)

        return layer

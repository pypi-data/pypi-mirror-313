"""
XML entities for PSCAD definition mappings
"""

#===============================================================================
# Imports
#===============================================================================

from __future__ import annotations

from typing import cast

from mhi.xml.node import XmlNode, NamedNodeContainerMapping
from mhi.xml.pscad._project import project_lookup, ProjectMixin
from mhi.xml.pscad.definition import Definition, UserCmpDefn

from mhi.xml.pscad.twm import RowDefn


#===============================================================================
# Exports
#===============================================================================


__all__ = ['DefinitionMapping', 'Definitions',]


#===============================================================================
# Definitions
#===============================================================================

class DefinitionMapping(NamedNodeContainerMapping[Definition]):
    """
    The project's :class:`.Definition` dictionary.

    Example::

        for defn_name in project.definition:
            print(defn_name)

        main_defn = project.definition['Main']

        del project.definition['not_needed']
    """

    def __init__(self, definitions: Definitions):

        super().__init__(definitions, 'Definition', 'Definitions')


    def _pre_add(self, key: str, defn: Definition): # pylint: disable=arguments-renamed

        project = cast(Definitions, self._container).project
        if project.id_exists(defn.id):
            defn.set('id', str(project.make_id()))

        schematic = defn.schematic
        if schematic is not None:
            for cmp in schematic.components():
                if project.id_exists(cmp.id):
                    cmp.set('id', str(project.make_id()))


    def _create(self, name: str, xml: str) -> Definition:

        defn = cast(Definition, self._container._parse(xml)) # pylint: disable=protected-access

        self[name] = defn
        return defn


    def create(self, name: str) -> UserCmpDefn:
        """
        Create a new UserCmp Definition
        """

        xml = UserCmpDefn._XML.format(name=name) # pylint: disable=protected-access

        return cast(UserCmpDefn, self._create(name, xml))


    def _create_twm(self, name: str, type_: str) -> RowDefn:

        xml = RowDefn._XML.format(name=name, type=type_) # pylint: disable=protected-access

        return cast(RowDefn, self._create(name, xml))


    def create_tline(self, name: str) -> RowDefn:
        """
        Create a new TLine
        """

        return self._create_twm(name, 'TLine')


    def create_cable(self, name: str) -> RowDefn:
        """
        Create a new TLine
        """

        return self._create_twm(name, 'Cable')


#-------------------------------------------------------------------------------

@project_lookup.tag('definitions')
class Definitions(XmlNode, ProjectMixin):
    """
    A `<definitions/>` container node
    """

"""
MHI XML for PSCAD Project (*.pscx, *.pslx) files
"""

#===============================================================================
# Imports
#===============================================================================

from __future__ import annotations

import logging
import os
import re
import time

from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import cast, Iterator, Optional, Union

from lxml import etree as ET

from mhi.xml.node import XmlNode, ParametersBase
from mhi.xml.file import File
from mhi.xml.pscad._project import project_lookup, ProjectMixin
from mhi.xml.pscad.component import Component, UserCmp
from mhi.xml.pscad.definition import UserCmpDefn
from mhi.xml.pscad.definitions import Definitions, DefinitionMapping
from mhi.xml.pscad.layer import Layers, LayerMapping
from mhi.xml.pscad.resource import ResourceMapping
from mhi.xml.pscad.schematic import Schematic
from mhi.xml.pscad.substitution import SubstitutionSetMapping, GlobalSubstitutions


#===============================================================================


LOG = logging.getLogger(__name__)


#===============================================================================
# Exports
#===============================================================================


__all__ = ['ProjectFile',
           ]


#===============================================================================
# List Node
#===============================================================================

@project_lookup.tag('List')
class ListNode(XmlNode, ProjectMixin):
    """
    <List classid="xyz">
       <xyz .../>
       <xyz .../>
    </List>
    """


#===============================================================================
# Project File
#===============================================================================

PROJECT_PARSER = project_lookup.parser(strip_cdata=False)


#===============================================================================

class ProjectFile(File):
    """
    A PSCAD Project (Library or Case)
    """

    _path: Path
    _doc: ET._ElementTree

    _canvases_in_use: Optional[list[Schematic]] = None

    _BLANK_PROJECT = """\
<project name="{name}" version="5.0.2" schema="" Target="{target}">
  <paramlist name="Settings">
    <param name="creator" value="{user},{timestamp}" />
    <param name="time_duration" value="0.5" />
    <param name="time_step" value="50" />
    <param name="sample_step" value="250" />
    <param name="chatter_threshold" value=".001" />
    <param name="branch_threshold" value=".0005" />
    <param name="StartType" value="0" />
    <param name="startup_filename" value="$(Namespace).snp" />
    <param name="PlotType" value="0" />
    <param name="output_filename" value="$(Namespace).out" />
    <param name="SnapType" value="0" />
    <param name="SnapTime" value="0.3" />
    <param name="snapshot_filename" value="$(Namespace).snp" />
    <param name="MrunType" value="0" />
    <param name="Mruns" value="1" />
    <param name="Scenario" value="" />
    <param name="Advanced" value="14335" />
    <param name="sparsity_threshold" value="200" />
    <param name="Options" value="16" />
    <param name="Build" value="18" />
    <param name="Warn" value="0" />
    <param name="Check" value="0" />
    <param name="Debug" value="0" />
    <param name="description" value="" />
    <param name="revisor" value="{user},{timestamp}" />
  </paramlist>
  <Layers />
  <List classid="Settings" />
  <bookmarks />
  <GlobalSubstitutions name="Default">
    <List classid="Sub" />
    <List classid="ValueSet" />
    <paramlist>
      <param name="Current" value="" />
    </paramlist>
  </GlobalSubstitutions>
  <definitions>
    <Definition classid="StationDefn" name="DS" id="0" group="" url="" version="" build="" crc="0" view="false">
      <paramlist name="">
        <param name="Description" value="" />
      </paramlist>
      <schematic classid="StationCanvas">
        <paramlist>
          <param name="show_grid" value="0" />
          <param name="size" value="0" />
          <param name="orient" value="1" />
          <param name="show_border" value="0" />
          <param name="monitor_bus_voltage" value="0" />
          <param name="show_signal" value="0" />
          <param name="show_virtual" value="0" />
          <param name="show_sequence" value="0" />
          <param name="auto_sequence" value="1" />
          <param name="bus_expand_x" value="8" />
          <param name="bus_expand_y" value="8" />
          <param name="bus_length" value="4" />
        </paramlist>
        <grouping />
        <Wire classid="Branch" id="0" name="Main" x="180" y="180" w="66" h="82" orient="0" disable="false" defn="Main" recv="-1" send="-1" back="-1">
          <vertex x="0" y="0" />
          <vertex x="0" y="18" />
          <vertex x="54" y="54" />
          <vertex x="54" y="72" />
          <User classid="UserCmp" id="0" name="{name}:Main" x="0" y="0" w="0" h="0" z="-1" orient="0" defn="{name}:Main" link="-1" q="4" disable="false">
            <paramlist name="" link="-1" crc="0" />
          </User>
        </Wire>
      </schematic>
    </Definition>
    <Definition classid="UserCmpDefn" name="Main" id="0" group="" url="" version="" build="" crc="0" view="false" date="0">
      <paramlist name="">
        <param name="Description" value="" />
      </paramlist>
      <form name="" w="320" h="400" splitter="60" />
      <graphics viewBox="-200 -200 200 200" size="2">
        <Gfx classid="Graphics.Rectangle" id="0" x="-36" y="-36" w="72" h="72">
          <paramlist>
            <param name="color" value="Black" />
            <param name="dasharray" value="0" />
            <param name="thickness" value="0" />
            <param name="port" value="" />
            <param name="fill_style" value="0" />
            <param name="fill_fg" value="Black" />
            <param name="fill_bg" value="Black" />
            <param name="cond" value="true" />
          </paramlist>
        </Gfx>
        <Gfx classid="Graphics.Text" id="0" x="0" y="0">
          <paramlist>
            <param name="text" value="%:Name" />
            <param name="anchor" value="0" />
            <param name="full_font" value="Tahoma, 13world" />
            <param name="angle" value="0" />
            <param name="color" value="Black" />
            <param name="cond" value="true" />
          </paramlist>
        </Gfx>
      </graphics>
      <schematic classid="UserCanvas">
        <paramlist>
          <param name="show_grid" value="0" />
          <param name="size" value="0" />
          <param name="orient" value="1" />
          <param name="show_border" value="0" />
          <param name="monitor_bus_voltage" value="0" />
          <param name="show_signal" value="0" />
          <param name="show_virtual" value="0" />
          <param name="show_sequence" value="0" />
          <param name="auto_sequence" value="1" />
          <param name="bus_expand_x" value="8" />
          <param name="bus_expand_y" value="8" />
          <param name="bus_length" value="4" />
        </paramlist>
        <grouping />
      </schematic>
    </Definition>
  </definitions>
  <List classid="Resource" />
  <hierarchy/>
</project>"""


    @classmethod
    def _create(cls, path: Path, target: str) -> ProjectFile:
        if not path.parent.is_dir():
            raise ValueError("Folder does not exists")
        if path.exists():
            raise ValueError("Target already exists")

        name = path.stem
        user = os.getlogin()
        timestamp = int(time.time())

        with open(path, 'w', encoding='utf-8') as f:
            f.write(cls._BLANK_PROJECT.format(name=name, user=user,
                                              target=target,
                                              timestamp=timestamp))
        return cls(path)


    @classmethod
    def create(cls, path: Union[Path, str]) -> ProjectFile:
        """
        Create a new PSCAD Library (*.pslx) or Project Case (*.pscx)
        """

        path = Path(path)
        if path.suffix == '.pscx':
            target = 'EMTDC'
        elif path.suffix == '.pslx':
            target = 'Library'
        else:
            raise ValueError("Invalid suffix")

        return cls._create(path, target)


    def __init__(self, path: Union[Path, str]):

        super().__init__(PROJECT_PARSER)

        self._read(Path(path))


    def __repr__(self) -> str:

        return f"Project[{self.namespace}]"


    @property
    def path(self) -> Path:
        """
        The path of the project's XML document (read-only)
        """

        return self._path


    def save_as(self, path: Union[Path, str]) -> None:
        """
        Write the project's XML document to a new location.

        Updates the :attr:`ProjectFile.path` property.  If written as a `.pscx`
        file, the :attr:`.namespace` property is updated to keep the filename
        and namespace in sync.
        """

        path = Path(path)

        ext = path.suffix.lower()
        if ext not in {'.pscx', '.pslx'}:
            raise ValueError("Invalid project suffix")

        if ext == '.pscx':
            self._set_namespace(path.stem)

        super().save_as(path)


    @property
    def namespace(self) -> str:
        """
        Namespace of the project

        Read-only if the project is a case; read-write if the project
        is a library.
        """

        namespace = self._root.get('name')
        assert namespace is not None

        return namespace


    @namespace.setter
    def namespace(self, namespace: str):
        if not namespace.isidentifier() or len(namespace) > 30:
            raise ValueError("Invalid namespace name: {namespace!r}")

        if self._path.suffix.lower() != '.pslx':
            raise ValueError("Not a library")

        self._set_namespace(namespace)


    def _set_namespace(self, namespace: str):

        if not re.match("^[A-Za-z]", namespace):
            namespace = "a" + namespace
        namespace = re.sub("[^A-Za-z0-9_]", "_", namespace[:30])

        if self.namespace != namespace:
            old_prefix = f"{self.namespace}:"
            new_prefix = f"{namespace}:"

            xpath = f'//schematic/*[starts-with(@defn, {old_prefix!r})]'
            cmps = cast(list[Component], self._root.xpath(xpath))
            for cmp in cmps:
                defn = cast(str, cmp.defn).removeprefix(old_prefix)
                cmp.set('defn', new_prefix + defn)

            xpath = f'//schematic/Wire/*[starts-with(@defn, {old_prefix!r})]'
            cmps = cast(list[Component], self._root.xpath(xpath))
            for cmp in cmps:
                defn = cast(str, cmp.defn).removeprefix(old_prefix)
                cmp.set('defn', new_prefix + defn)

            xpath = f'//call[starts-with(@name, {old_prefix!r})]'
            calls = cast(list[ET.ElementBase], self._root.xpath(xpath))
            for call in calls:
                name = call.get('name', '').removeprefix(old_prefix)
                call.set('name', new_prefix + name)

            self._root.set('name', namespace)


    @property
    def root(self) -> XmlNode:

        return cast(XmlNode, self._root)


    @property
    def version(self) -> str:
        """
        The PSCAD project file version
        """

        return self._root.get('version', '5.0.0')


    @version.setter
    def version(self, new_version: str):

        if not re.fullmatch(r"5\.[0-2]\.[1-9]?\d", new_version):
            raise ValueError("Invalid version: {new_version!r}")

        self._root.set('version', new_version)


    @property
    def parameters(self) -> ProjectFile.Parameters:
        """
        The project parameters structure
        """

        xpath = 'paramlist[@name="Settings"]'
        return self.Parameters(self._root.find(xpath))


    class Parameters(ParametersBase):
        """
        Project Parameters
        """

        # General
        description: str
        creator: str
        revisor: str

        # Runtime - Time Settings
        time_duration: float
        time_step: float
        sample_step: float

        # Runtime Startup
        StartType: int
        startup_filename: str
        PlotType: int
        output_filename: str
        SnapType: int
        snapshot_filename: str
        SnapTime: float
        MrunType: int
        Mruns: int

        # Simulation
        branch_threshold: float
        chatter_threshold: float
        sparsity_threshold: int


        # Fortran
        Preprocessor: str
        Source: str

        # Bit flags
        Advanced: int
        Build: int
        Check: int
        Debug: int
        Options: int
        Warn: int

        # Other...?
        #multirun_filename: str
        #latency_count: int
        #architecture: str
        #Scenario: str

        @property
        def created_by(self) -> str:
            """Return the creator of the project"""

            return self.creator.split(",", 1)[0]

        @property
        def created_on(self) -> datetime:
            """Return the date/time the project was created"""

            timestamp = int(self.creator.split(",", 1)[1])
            return datetime.fromtimestamp(timestamp)

        @property
        def revised_by(self) -> str:
            """Return the last revisor of the project"""

            return self.revisor.split(",", 1)[0]

        @property
        def revised_on(self) -> datetime:
            """Return the date/time the project was last revised"""

            timestamp = int(self.revisor.split(",", 1)[1])
            return datetime.fromtimestamp(timestamp)


    def _find_or_make(self, xpath: str, xml: str) -> XmlNode:

        node = self._root.find(xpath)
        if node is None:
            node = self._parse(xml)
            self._root.append_indented(node)

        return cast(XmlNode, node)


    @property
    def layer(self) -> LayerMapping:
        """
        The project's Layer mapping.

        Examples::

            layer_1 = project.layer.create('Layer1')
            layer_1.state = 'Invisible'

            layer_2 = project.layer.create('Layer2')
            layer_2.state = 'Disabled'
            layer_2.parameters.disabled_color = 0xAA8866
        """

        layers = cast(Layers, self._find_or_make('Layers', '<Layers/>'))

        return LayerMapping(layers, 'Layer', 'name', 'Layers')


    @property
    def substitution_set(self) -> SubstitutionSetMapping:
        """
        The global substitution set mapping.

        This is a dictionary of global substitution sets, where
        each set is a dictionary of substitution variables and
        the value which will replace them.

        Example::

            # Create new substitution sets
            euro_ss = project.substitution_set.create_set('Euro')
            project.substitution_set.create_sets('Asia', 'Africa')

            # Set initial (default) global substitutions
            default_ss = project.substitution_set['Default']
            default_ss['BaseKV'] = '230.0 [kV]'
            default_ss['Freq'] = '60.0 [Hz]'

            # Override 'Freq' in 'Euro' substitution set
            euro['Freq'] = '50.0 [Hz]'

            # Set the project's current global substitution set
            project.substitution_set.current = 'Euro'

            # Delete a global substitution set
            del project.substitution_set['Africa']
        """

        gs = self._find_or_make('GlobalSubstitutions', GlobalSubstitutions.XML)

        return SubstitutionSetMapping(cast(GlobalSubstitutions, gs))


    @property
    def definition(self) -> DefinitionMapping:
        """
        The project's :class:`.Definition` mapping.

        Example::

            for defn_name in project.definition:
                print(defn_name)

            main_defn = project.definition['Main']

            del project.definition['not_needed']
        """

        definitions = self._find_or_make('definitions', '<definitions/>')

        return DefinitionMapping(cast(Definitions, definitions))


    def remap(self, old: ProjectFile, new: ProjectFile,
              *definition: str) -> set[str]:
        """
        Replace definition references from one namespace with definition
        references having the same definition name in another namespace.

        If definition names are given, each must exist in both namespaces.
        If no definition names are given, all common definition names will
        be used.

        Returns definition names remapped from ``old`` to ``new``.

        Raises a ``ValueError`` if no common definition names are found,
        or if any of the given definition names are not common to both
        ``old`` and ``new``.

        .. versionadded:: 1.2.0
        """

        old_defs = set(old.definition)
        new_defs = set(new.definition)
        common = old_defs & new_defs

        if not common:
            raise ValueError("No definition names in common")

        if definition:
            replace = set(definition)
            if not replace <= common:
                missing = ', '.join(map(repr, replace - common))
                raise ValueError(f"Cannot remap {missing}")
        else:
            replace = common

        old_ns = old.namespace
        #new_ns = new.namespace

        replaced = set()
        for name in replace:
            new_defn = cast(UserCmpDefn, new.definition[name])

            changes = self._remap(f'{old_ns}:{name}', new_defn)
            if changes:
                replaced.add(name)


        return replaced

    def _remap(self, old_defn: str, new_defn: UserCmpDefn) -> bool:

        xpath = ('definitions/Definition/schematic/User[@classid="UserCmp"]'
                 f'[@defn="{old_defn}"]')

        found = False

        for cmp in cast(list[UserCmp], self._root.xpath(xpath)):
            cmp.remap(new_defn)
            found = True

        return found


    @property
    def resource(self) -> ResourceMapping:
        """
        The project's :class:`.Resource` mapping.

        Example::

            for resource_name in project.resource:
                print(resource_name)
        """

        resources = self._find_or_make('List[@classid="Resource"]',
                                       '<List @classid="Resource"/>')

        return ResourceMapping(resources)


    _SCHEMATICS = ET.XPath('definitions/Definition/schematic[@classid=$classid]')

    def _schematics(self, classid: str) -> list[Schematic]:

        schematics = self._SCHEMATICS(self._root, classid=classid)
        return cast(list[Schematic], schematics)


    def user_canvases(self) -> list[Schematic]:
        """
        List of user canvases
        """

        return self._schematics('UserCanvas')


    def canvas(self, name: str) -> Schematic:
        """
        Canvas lookup.
        """

        xpath = f'definitions/Definition[@name={name!r}]/schematic'
        return cast(Schematic, self._root.find(xpath))


    _USERCMP = ET.XPath('User[@classid="UserCmp"]')

    def canvases_in_use(self) -> list[Schematic]:
        """
        List of canvases in use.

        .. note::

            If a module itself has been marked as disabled, the underlying
            canvas is not in use.  If a modules is merely disabled due to
            being placed on a layer that happens to be disabled, the underlying
            canvas is still considered to be in use, since the conditions
            which determine whether or not a layer is disabled are not
            evaluated here.
        """

        if self._canvases_in_use is not None:
            return self._canvases_in_use

        canvases = {canvas.name: canvas for canvas in self.user_canvases()}
        active = []
        found = {'Main'}

        prefix = f'{self.namespace}:'

        while found:
            name = found.pop()
            canvas = canvases.pop(name)
            active.append(canvas)

            user_components = cast(list[UserCmp], self._USERCMP(canvas))
            for user in user_components:
                defn = user.defn
                if user.enabled and defn.startswith(prefix):
                    name = defn.split(':', 1)[1]
                    if name in canvases:
                        found.add(name)

        self._canvases_in_use = active
        return self._canvases_in_use


    def components(self,
                   name: Optional[str] = None, /, *,
                   defn: Optional[str] = None,
                   include_defns: Optional[set[str]] = None,
                   exclude_defns: Optional[set[str]] = None,
                   xpath: Optional[str] = None,
                   classid: Optional[str] = None,
                   canvases_in_use_only: bool = False,
                   with_params: Optional[set[str]] = None,
                   **params) -> Iterator['Component']:
        """
        Component search

        Find the components within the project identified by the
        provided arguments.  All arguments are optional.  The name parameter,
        if given, must be the first and only positional parameter.
        All other parameters must be keyword parameters.

        :param str name: Name of the component (positional parameter only)
        :param str classid: Component class identifier
        :param str defn: Definition name
        :param set[str] include_defns: Definition names to include in search
        :param set[str] exclude_defns: Definition names to exclude from search
        :param bool canvases_in_use_only: Ignore non-instanciated canvases (default: False)
        :param set[str] with_params: Only components with have the given parameters
        :param key=value: Components with the given parameter key=value pairs

        At most one of `defn`, `include_defns` or `exclude_defns` may be
        provided.
        """

        xpath = Schematic._xpath(xpath, classid, defn, with_params, params) # pylint: disable=protected-access

        if canvases_in_use_only:
            canvases = self.canvases_in_use()
        else:
            canvases = self.user_canvases()

        for canvas in canvases:
            yield from canvas.components(name, xpath=xpath,
                                         include_defns=include_defns,
                                         exclude_defns=exclude_defns)

    def component(self,
                  name: Optional[str] = None, /, *,
                  defn: Optional[str] = None,
                  include_defns: Optional[set[str]] = None,
                  exclude_defns: Optional[set[str]] = None,
                  classid: Optional[str] = None,
                  xpath: Optional[str] = None,
                  raise_if_not_found: bool = False,
                  raise_if_multiple_found: bool = False,
                  canvases_in_use_only: bool = False,
                  with_params: Optional[set[str]] = None,
                  **params) -> Optional['Component']:
        """
        Component search

        Find the component within the project identified by the provided
        arguments.  All arguments are optional.  The name parameter,
        if given, must be the first and only positional parameter.
        All other parameters must be keyword parameters.

        :param str name: Name of the component (positional parameter only)
        :param str classid: Component class identifier
        :param str defn: Definition name
        :param set[str] include_defns: Definition names to include in search
        :param set[str] exclude_defns: Definition names to exclude from search
        :param bool canvases_in_use_only: Ignore non-instanciated canvases (default: False)
        :param bool raise_if_not_found: Raise an exception if component isn't found (default: False)
        :param bool raise_if_multiple_found: Raise exception if multiple are found. (default: False)
        :param set[str] with_params: Only components with have the given parameters
        :param key=value: Components with the given parameter key=value pairs

        At most one of `defn`, `include_defns` or `exclude_defns` may be
        provided.
        """

        it = self.components(name,
                             defn=defn,
                             include_defns=include_defns,
                             exclude_defns=exclude_defns,
                             classid=classid,
                             xpath=xpath,
                             canvases_in_use_only=canvases_in_use_only,
                             with_params=with_params,
                             **params)

        cmp = next(it, None)
        if cmp is None:
            if raise_if_not_found:
                raise ValueError("Component not found")
        elif raise_if_multiple_found:
            if next(it, None) is not None:
                raise ValueError("Multiple components found")

        return cmp


    def named_components(self, *,
                         classid: Optional[str] = None,
                         defn: Optional[str] = None
                         ) -> dict[str, list[Component]]:
        """
        Find all named components (of a particular class and/or definition),
        and return a dictionary of name-to-components.

        Note:

            Multiple components can share the same name, so the returned
            dictionary will contain a list for each name, even if only
            one component by that name exists.
        """

        components = defaultdict(list)
        for cmp in self.components(classid=classid, defn=defn):
            name = cmp.name
            if name:
                components[name].append(cmp)

        return dict(components)

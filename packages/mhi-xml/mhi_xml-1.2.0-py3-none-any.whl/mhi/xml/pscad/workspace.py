"""
MHI XML for PSCAD Workspace (*.pswx) files
"""

#===============================================================================
# Imports
#===============================================================================

from __future__ import annotations

import logging
import re

from collections.abc import MutableMapping, ItemsView
from enum import Enum
from os import PathLike
from pathlib import Path
from typing import cast, Iterator, Optional, Union

from lxml import etree as ET

from mhi.xml.node import (XmlNode, NamedNode, NamedNodeContainerMapping,
                          ParametersBase,
                          TagLookup, param_tag_lookup)
from mhi.xml.file import FileProtocol, File
from mhi.xml.pscad.project import ProjectFile

#===============================================================================
# Exports
#===============================================================================

__all__ = ['WorkspaceFile']


#===============================================================================

LOG = logging.getLogger(__name__)


#===============================================================================

workspace_tag_lookup = TagLookup(param_tag_lookup)


#===============================================================================

class WorkspaceMixin(FileProtocol):    # pylint: disable=too-few-public-methods
    """
    Access WorkspaceFile from an Xml node in the Workspace
    """

    @property
    def workspace(self) -> WorkspaceFile:
        """
        Retrieve WorkspaceFile
        """

        return cast(WorkspaceFile, self._file)


#===============================================================================

@workspace_tag_lookup('project')
class ProjectNode(NamedNode, WorkspaceMixin):
    """
    A project within a workspace.

    .. note::

        This `ProjectNode` only represents an entry within the
        :class:`WorkspaceFile`.  It must be :meth:`opened <open>` to
        obtain the actual :class:`~mhi.xml.pscad.project.ProjectFile`.
    """


    class Type(Enum):
        """
        Project Types
        """

        LIBRARY = 'library'
        PROJECT = 'project'


    TYPE_BY_EXT = {
        '.pslx': Type.LIBRARY,
        '.pscx': Type.PROJECT,
        }


    def __repr__(self) -> str:
        return f"{self.type.title()}<{self.name!r}, {self.filepath!r}>"


    @staticmethod
    def validate_name(name: str) -> None:
        """
        Ensure the name is a legal PSCAD project identifier
        """

        if not name.isidentifier():
            raise ValueError("Illegal Project name")


    @staticmethod
    def validate_type(kind: str) -> None:
        """
        Ensure the type is a legal PSCAD project type
        """

        ProjectNode.Type(kind)


    @property
    def type(self) -> str:
        """
        Type of the project (read-only)

        Either `'library'` or `'project'`
        """

        return self.get('type', ProjectNode.Type.PROJECT.value)


    @property
    def is_library(self) -> bool:
        """
        `True` if the project represents a PSCAD Library.
        (read-only)
        """

        return self.type == ProjectNode.Type.LIBRARY.value


    @property
    def is_case(self) -> bool:
        """
        `True` if the project represents a PSCAD Project Case.
        (read-only)
        """

        return self.type == ProjectNode.Type.PROJECT.value


    @property
    def filepath(self) -> str:
        """
        The project's filepath attribute string. (read-only)
        """

        return self.get('filepath', '')


    @property
    def path(self) -> Path:
        """
        The project's filepath, resolved relative to the workspace file.
        (read-only)
        """

        return self.workspace.folder / self.filepath


    def open(self) -> ProjectFile:
        """
        Open the project's XML file
        """

        path = self.path
        LOG.info("Opening %s", path)

        return ProjectFile(path)


    def delete(self) -> None:
        """
        Remove this project from the workspace.
        """

        self._remove_from_parent()


#===============================================================================

@workspace_tag_lookup('projects')
class ProjectsNode(XmlNode, WorkspaceMixin):
    """
    Workspace XML <projects/> element
    """


#===============================================================================

class ProjectMapping(NamedNodeContainerMapping[ProjectNode]):
    r"""
    The workspace's :class:`ProjectNode` dictionary.

    The `ProjectNode` dictionary contains the libraries and cases in the
    workspace (excluding the Master Library).  The dictionary may be
    iterated over to obtain each `ProjectNode` within, or it may be
    indexed by namespace to obtain a specific one::

        workspace = ...
        for prj_name, prj_node in workspace.project.values():
            print(prj_name, prj_node.path)

        tutorial_ws = ...
        vdiv_node = tutorial_ws.project['vdiv']

    A project may be added to the workspace by assigning a path to a **new**
    namespace, or removed by deleting the entry::

        del workspace.project['old_library']
        workspace.project['new_library'] = Path(r"C:\Path\to\new_library.pslx")
    """

    def __init__(self, workspace_file: WorkspaceFile):

        super().__init__(workspace_file.projects, 'project')


    def __setitem__(self, namespace: str,
                    project_or_path: Union[ProjectNode, PathLike, str]) -> None:

        if isinstance(project_or_path, ProjectNode):
            project = project_or_path

        else:
            path = Path(project_or_path)
            prj_type = ProjectNode.TYPE_BY_EXT[path.suffix.lower()]
            if prj_type == ProjectNode.Type.PROJECT:
                if namespace.casefold() != path.stem.casefold():
                    raise ValueError(f"Filename {path.stem!r} does not match "
                                     f"the namespace name {namespace!r}")

            node = self._container.makeelement('project',
                                               name=namespace,
                                               type=prj_type.value,
                                               filepath=str(path))
            project = cast(ProjectNode, node)

        super().__setitem__(namespace, project)


    def __repr__(self) -> str:
        return f"Projects[{', '.join(self.names())}]"


#===============================================================================

_SIMULATION_XML = (
 """<simulation name="{name}" dependson="None" id="{id}" classid="SimulationSet">
      <paramlist name="Default">
        <param name="enabled" value="true" />
        <param name="before_run" value="" />
        <param name="before_block" value="true" />
        <param name="after_run" value="" />
        <param name="after_block" value="true" />
      </paramlist>
    </simulation>""")

@workspace_tag_lookup('simulation')
class SimulationSetNode(NamedNode):
    """
    A simulation set element.
    """

    def __repr__(self) -> str:
        return f"Simulation<{self.name!r}>"


    def delete(self) -> None:
        """
        Remove this simulation set from the workspace
        """

        self._remove_from_parent()


    @property
    def task(self) -> TaskMapping:
        """
        The simulation set's task dictionary.
        """

        return TaskMapping(self)


    def namespaces(self) -> list[str]:
        """
        The project names that are part of this simulation set.
        """

        return list(self.task.keys())


    @property
    def depends_on(self) -> str:
        """
        Simultaion set dependency.
        """

        return self.get('dependson', 'None')


    def parameters(self, name='Default') -> SimulationSetNode.Parameters:
        """
        The simultaion set's parameters structure.
        """

        xpath = f'paramlist[@name={name!r}]'
        return self.Parameters(self.find(xpath))


    #-----------------------------------------------------------------------

    class Parameters(ParametersBase):
        """
        The simulation set's parameters  (read/write)
        """

        enabled: bool
        before_run: str
        before_block: bool
        after_run: str
        after_block: bool


#===============================================================================

@workspace_tag_lookup('simulations')
class SimulationsNode(XmlNode, WorkspaceMixin):
    """
    Workspace XML <simulations/> element
    """


#===============================================================================

class SimulationSetMapping(NamedNodeContainerMapping[SimulationSetNode]):
    r"""
    The workspace's :class:`SimulationSetNode` dictionary.

    The dictionary contains the simulation sets in the workspace.
    The dictionary may be iterated over to obtain each
    `SimulationSetNode` within, or it may be indexed by
    name to obtain a specific one::

        workspace = ...
        for simset in workspace.simulation_set.values():
            print(simset.name)

        default_ss = workspace.simulation_set['default']

    New simulation sets may be created using the :meth:`.create` method::

        simset1 = workspace.simulation_set.create('simset1')

    A simulation set may be removed from the workspace by deleting the entry::

        del workspace.simulation_set['simset1']
    """

    def __init__(self, workspace_file: WorkspaceFile):

        super().__init__(workspace_file.simulations, 'simulation')


    def create(self, name: str) -> SimulationSetNode:
        """
        Create a new simulation set
        """

        if name in self:
            raise KeyError(f"Simulation set {name} already exists")

        workspace = cast(WorkspaceMixin, self._container).workspace
        xml = _SIMULATION_XML.format(name=name, id=workspace.make_id())
        simulation_set_node = cast(SimulationSetNode, workspace._parse(xml))    # pylint: disable=protected-access

        self._container.append_indented(simulation_set_node)

        return simulation_set_node


    def __repr__(self) -> str:
        return f"SimulationSets[{', '.join(self.names())}]"


#===============================================================================

@workspace_tag_lookup('task')
class SimulationTaskNode(XmlNode):
    """
    A simulation set's task element.
    """

    def __repr__(self) -> str:
        return f"SimulationTask<{self.namespace!r}>"


    def delete(self) -> None:
        """
        Remove this simulation task from the simulation set.
        """

        self._remove_from_parent()


    @property
    def namespace(self) -> str:
        """
        The namespace of this simulation set task.
        """

        return self.get('namespace', '')


    def parameters(self, name='Options') -> SimulationTaskNode.Parameters:
        """
        The simulation set task's parameters structure.
        """

        xpath = f'paramlist[@name={name!r}]'
        return self.Parameters(self.find(xpath))


    #-----------------------------------------------------------------------

    class Parameters(ParametersBase):
        """
        Parameters of a simulation set's task (read/write).
        """

        simulationset: str
        namespace: str
        name: str
        ammunition: int
        volley: int
        affinity_type: int
        affinity: int
        rank_snap: bool
        substitutions: str
        clean: bool


#===============================================================================

class TaskMapping(MutableMapping[str, SimulationTaskNode]):
    """
    A simulation set's task dictionary.
    """


    def __init__(self, simset: SimulationSetNode):

        self._simset = simset


    def _find(self, namespace: str) -> Optional[SimulationTaskNode]:

        assert isinstance(namespace, str)

        xpath = f"task[@namespace={namespace!r}]"
        task_node = cast(SimulationTaskNode, self._simset.find(xpath))
        return task_node


    def _get(self, namespace: str) -> SimulationTaskNode:

        task_node = self._find(namespace)
        if task_node is None:
            raise KeyError(namespace)

        return task_node


    def __getitem__(self, namespace: str) -> SimulationTaskNode:

        return self._get(namespace)


    def __setitem__(self, namespace: str, task_node: SimulationTaskNode):

        if self._find(namespace) is not None:
            raise KeyError(f"{namespace!r} already exists")

        task_node.set('namespace', namespace)
        self._simset.append_indented(task_node)


    def __delitem__(self, namespace: str) -> None:

        task_node = self._get(namespace)
        task_node._remove_from_parent()


    def __iter__(self) -> Iterator[str]:

        for task_node in self._simset.iterchildren('task'):
            yield task_node.get('namespace', '')


    def items(self) -> ItemsView[str, SimulationTaskNode]:

        class _ItemsView(ItemsView[str, SimulationTaskNode]):

            _mapping: TaskMapping

            def __iter__(self) -> Iterator[tuple[str, SimulationTaskNode]]:
                simset = self._mapping._simset

                for node in simset.iterchildren('task'):
                    task_node = cast(SimulationTaskNode, node)
                    yield task_node.get('namespace', ''), task_node

        return _ItemsView(self)


    def __len__(self) -> int:

        return len(self._simset.findall('task'))


    def __contains__(self, namespace) -> bool:

        return self._find(namespace) is not None


    def namespaces(self) -> list[str]:
        """
        List the namespaces of the tasks in the simulation set.
        """
        return list(self.keys())


    def __repr__(self) -> str:

        return f"Tasks[{','.join(self.namespaces())}]"


#===============================================================================

WORKSPACE_PARSER = ET.XMLParser(strip_cdata=False)
WORKSPACE_PARSER.set_element_class_lookup(workspace_tag_lookup)


#===============================================================================

class WorkspaceFile(File):
    r"""
    A PSCAD Workspace XML File

    An existing workspace is read by specifying an existing workspace file
    in the constructor::

        from mhi.xml.pscad import WorkspaceFile

        ws = WorkspaceFile(r"C:\Workspace\Path\TheWorkspace.pswx")


    Since project files are located relative to the workspace, to create
    a new workspace the directory of the new workspace is required.
    Specifying a directory, instead of a file, creates an empty workspace::

        from mhi.xml.pscad import WorkspaceFile

        ws = WorkspaceFile(r"C:\Workspace\Path")

        ...

        ws.save_as("TheWorkspace.pswx")
    """

    _EMPTY = """\
<workspace name="default" version="5.0.2" crc="0">
  <paramlist name="options">
  </paramlist>
  <projects />
  <simulations />
  <pmr />
  <messagegrid expanded="">
    <column name="Icon" />
    <column name="Id" />
    <column name="Component" />
    <column name="Namespace" />
    <column name="Description" />
  </messagegrid>
</workspace>"""


    def __init__(self, path: Union[Path, str, None] = None):

        super().__init__(WORKSPACE_PARSER)

        ws_path = Path(path) if path is not None else Path(".")
        if ws_path.is_dir():
            self._folder = ws_path
            self._load(self._EMPTY)
        elif ws_path.is_file():
            if ws_path.suffix.lower() != ".pswx":
                raise ValueError("PSCAD Workspace suffix ('.pswx') expected.")
            self._read(ws_path)
            self._folder = ws_path.parent
        else:
            raise FileNotFoundError(f"Invalid workspace path {path!r}")


    def save_as(self, path: Union[Path, str]) -> None:
        """
        Write the workspace XML document to a new location.

        .. note::

            This updates the "read-only" name, path, and folder properties.
        """

        path = Path(path)

        if path.suffix.lower() != '.pswx':
            raise ValueError("Invalid PSCAD workspace suffix")

        # Must start with letter, 30 chars max, only letters/numbers/_
        name = path.stem
        if not re.match("^[A-Za-z]", name):
            name = "a" + name
        name = re.sub("[^A-Za-z0-9_]", "_", name[:30])

        self._root.set('name', name)

        super().save_as(path)
        self._folder = path.parent


    @property
    def name(self) -> str:
        """
        Name of the workspace (read-only)
        """

        return self._root.get('name', '')

    @property
    def folder(self) -> Path:
        """
        The workspace directory (read-only)
        """

        return self._folder


    @property
    def version(self) -> str:
        """
        PSCAD version used to create the workspace.
        """

        return self._root.get('version', '')


    @version.setter
    def version(self, new_version: str):

        if not re.fullmatch(r"5\.[0-2]\.[1-9]?\d", new_version):
            raise ValueError("Invalid version: {new_version!r}")

        self._root.set('version', new_version)


    def __repr__(self) -> str:

        name = self._path or self._folder / "<unnamed>.pswx"
        return f"Workspace[{name}]"


    @property
    def projects(self) -> ProjectsNode:
        r"""
        The workspace's `<projects/>` XML node.
        """

        node = self._root.find('projects')
        assert isinstance(node, ProjectsNode)
        return node


    @property
    def project(self) -> ProjectMapping:
        r"""
        The workspace's "Project" dictionary.

        It is used to find the workspace's projects::

            from mhi.xml.pscad import WorkspaceFile

            examples_folder = r"C:\Users\Public\Documents\PSCAD\5.0.2\Examples"
            ws = WorkspaceFile(rf"{examples_folder}\tutorial\Tutorial.pswx")

            vdiv = ws.project["vdiv"].open()

        .. Note::

            A `ProjectNode` must be 'opened' to access the corresponding
            `Project`.
        """

        return ProjectMapping(self)


    def add_project(self,
                    project_or_path: Union[ProjectFile, PathLike, str]) -> None:
        """
        Add a project to the workspace
        """

        if isinstance(project_or_path, ProjectFile):
            path = project_or_path.path
            name = project_or_path.namespace
        else:
            path = Path(project_or_path)
            name = path.stem

        self.project[name] = path


    def all_exist(self) -> bool:
        """
        Verify that all projects in the workspace exist.
        """

        for prj in self.projects.iterchildren('project'):
            prj = cast(ProjectNode, prj)
            path = self._folder / prj.filepath
            all_exist = True
            if not path.is_file():
                LOG.error("Project %r not found: %s", prj.name, path)
                all_exist = True

        return all_exist


    @property
    def simulations(self) -> SimulationsNode:
        r"""
        The workspace's `<simulations/>` XML node.
        """

        node = self._root.find('simulations')
        assert isinstance(node, SimulationsNode)
        return node


    @property
    def simulation_set(self) -> SimulationSetMapping:
        """
        The workspace's simulation set dictionary.

        It is used to access the workspace's simulation sets::

            from mhi.xml.pscad import WorkspaceFile

            workspace = ...

            default_simset = workspace.simulation_set["default"]
            base_simset = workspace.simulation_set.create("base")
        """

        return SimulationSetMapping(self)

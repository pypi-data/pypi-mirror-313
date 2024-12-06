"""
XML entities for PSCAD Global Substitution variables
"""

#===============================================================================
# Imports
#===============================================================================

from __future__ import annotations

from collections.abc import MutableMapping

from typing import cast, Any, Iterator, Optional

from mhi.xml.node import XmlNode, ParametersBase
from mhi.xml.pscad._project import project_lookup, ProjectMixin


#===============================================================================
# Exports
#===============================================================================

__all__ = ['GlobalSubstitutions',
           'SubstitutionSetMapping',
           'DefaultSubstitutionSet',
           'SubstitutionSet',
           ]


#===============================================================================
# Global Substitutions
#===============================================================================

_GS_VALUE_SET_LIST_XML = '<List classid="ValueSet" />'
_GS_SUB_LIST_XML = '<List classid="Sub" />'


@project_lookup.tag('GlobalSubstitutions')
class GlobalSubstitutions(XmlNode, ProjectMixin):
    """
    Project <GlobalSubstitutions/> container
    """

    XML = (
    f"""<GlobalSubstitutions name="Default">
        {_GS_SUB_LIST_XML}
        {_GS_VALUE_SET_LIST_XML}
        <paramlist>
          <param name="Current" value="" />
        </paramlist>
      </GlobalSubstitutions>""")


@project_lookup.classid('Sub')
class SubstitutionsList(XmlNode, ProjectMixin):
    """
    Global Substitution Default Substitutions List

    <List classid="Sub" />
    """


@project_lookup.tag('Sub')
class Sub(XmlNode, ProjectMixin):
    """
    Global Substitution

    <Sub/>
    """


@project_lookup.classid('ValueSet')
class ValueSetsList(XmlNode, ProjectMixin):
    """
    Global Substitution Value Sets List

    <List classid="ValueSet" />
    """


@project_lookup.tag('ValueSet')
class ValueSet(XmlNode, ProjectMixin):
    """
    Global Substitution Value Set

    <ValueSet/>
    """


#-------------------------------------------------------------------------------
# Substitution Set (Base)
#-------------------------------------------------------------------------------

class SubstitutionSetBase(MutableMapping[str, str]):    # pylint: disable=abstract-method
    """
    A dictionary or mapping of substitution key=value pairs.
    """

    def __init__(self, substitution_sets: SubstitutionSetMapping,
                 container: XmlNode):

        self._substitution_sets = substitution_sets
        self._container = container


    def __ior__(self, other):

        if not isinstance(other, dict):
            return NotImplemented

        self.update(other)

        return self


    def __repr__(self):

        kv = ', '.join(f"{k!r}: {v!r}" for k, v in self.items())
        return f"{{{kv}}}"


#-------------------------------------------------------------------------------
# Global Substitutions / Substitution Set Mapping
#-------------------------------------------------------------------------------

class SubstitutionSetMapping(MutableMapping[str, SubstitutionSetBase]):
    """
    The project's global substitution set dictionary.

    Usage::

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

    def __init__(self, container: GlobalSubstitutions):

        self._container = container

        list_of_subs = cast(SubstitutionsList,
                            container.find('List[@classid="Sub"]'))
        self._default_value_set = DefaultSubstitutionSet(self, list_of_subs)

        self._value_sets = cast(ValueSetsList,
                                container.find('List[@classid="ValueSet"]'))


    def _default_set_name(self) -> str:

        return self._container.get('name', 'Default')


    def _is_default_set_name(self, name) -> bool:

        return name == ''  or  name == self._default_set_name()


    def _find(self, key: str) -> Optional[SubstitutionSetBase]:

        if self._is_default_set_name(key):
            return self._default_value_set

        value_set = cast(ValueSet,
                         self._value_sets.find(f'ValueSet[@name={key!r}]'))
        if value_set is not None:
            return SubstitutionSet(self, value_set)

        return None


    def _get(self, key: str) -> SubstitutionSetBase:

        substitution_set = self._find(key)
        if substitution_set is None:
            raise KeyError(key)

        return substitution_set


    def __len__(self) -> int:

        value_sets = self._value_sets.findall('ValueSet')
        return len(value_sets) + 1


    def __iter__(self) -> Iterator[str]:

        yield self._default_set_name()

        for value_set in self._value_sets.iterfind('ValueSet'):
            yield value_set.get('name', '')


    def __getitem__(self, key: str) -> SubstitutionSetBase:

        return self._get(key)


    def __setitem__(self, key: str, values) -> None:

        value_set = self._find(key)
        if value_set is not None and isinstance(values, SubstitutionSetBase):
            if values is value_set or values._container is value_set._container:
                return

        if not self._is_default_set_name(key):
            keys = set(self._default_value_set)

            missing = [key for key in values if key not in keys]
            if missing:
                raise ValueError(f"No defaults for {', '.join(missing)}")

        if value_set is None:
            value_set = self.create_set(key)

        value_set.update(values)

        for a_key in value_set:
            if a_key not in values:
                del value_set[a_key]


    def __delitem__(self, key: str) -> None:

        if self._is_default_set_name(key):
            raise ValueError("Cannot delete default set")

        value_set = self._get(key)
        value_set._container._remove_from_parent()


    def create_set(self, key: str) -> SubstitutionSet:
        """
        Create a new global substitution set
        """

        if self._find(key) is not None:
            raise ValueError("Substitution set {key!r} already exists.")

        project = self._container.project
        xml = _GS_GENERAL_SUBSET_XML.format(id=project.make_id(), name=key)
        value_set = cast(ValueSet, project._parse(xml)) # pylint: disable=protected-access
        self._value_sets.append_indented(value_set)

        return SubstitutionSet(self, value_set)


    def create_sets(self, key: str, *keys: str) -> None:
        """
        Create one or more new global substitution sets
        """

        all_keys = (key,) + keys
        for a_key in all_keys:
            self.create_set(a_key)


    def __repr__(self):

        return f"GlobalSubstitutions[{', '.join(self.keys())}]"


    @property
    def current(self) -> str:
        """
        The project's currently active substitution set name
        """

        return self.parameters.Current


    @current.setter
    def current(self, value: str):

        if value == '':
            value = self._default_set_name()

        # Ensure substitution set name exists
        self._get(value)

        self.parameters.Current = value         # pylint: disable=invalid-name


    @property
    def parameters(self) -> Parameters:
        """
        Global Substitution parameters
        """

        return self.Parameters(self._container.find('paramlist'))


    class Parameters(ParametersBase):
        """
        Global Substitutions parameters
        """

        Current: str


#-------------------------------------------------------------------------------
# Default Substitution Set
#-------------------------------------------------------------------------------

_GS_DEFAULT_SUBSET_XML = (
   """<Sub id="{id}" classid="GlobalSubstitution">
        <paramlist>
          <param name="name" value="{name}" />
          <param name="value" value="{value}" />
          <param name="group" value="" />
          <param name="cat" value="" />
        </paramlist>
      </Sub>""")

class DefaultSubstitutionSet(SubstitutionSetBase):
    """
    Default Substitution Set

        <List classid="Sub">
          <Sub id="#" ...>
             <paramlist>
                <param name="name" value="NAME" />
                <param name="value" value="VALUE" />
             </paramlist>
          </Sub>
          <Sub .../>
       </List>
    """

    _container: SubstitutionsList


    def __len__(self) -> int:

        return len(self._container.findall('Sub'))


    def __iter__(self) -> Iterator[str]:

        xpath = 'Sub/paramlist/param[@name="name"]'
        for param in self._container.iterfind(xpath):
            yield param.get('value', '')


    def _find(self, key: str) -> Optional[Sub]:

        if not key.isidentifier():
            raise KeyError(f"Invalid key {key!r}")

        xpath = f'Sub/paramlist/param[@name="name"][@value={key!r}]/../..'
        return cast(Sub, self._container.find(xpath))


    def _get(self, key: str) -> Sub:

        sub = self._find(key)
        if sub is None:
            raise KeyError(key)

        return sub


    def __getitem__(self, key: str) -> str:

        sub = self._get(key)
        param = sub.find('paramlist/param[@name="value"]')
        assert param is not None
        return param.get('value', '')


    def __setitem__(self, key: str, value: Any):

        value = str(value)
        sub = self._find(key)
        if sub is None:
            project = self._container.project
            xml = _GS_DEFAULT_SUBSET_XML.format(id=project.make_id(),
                                                name=key, value=value)
            sub = cast(Sub, project._parse(xml))
            self._container.append(sub)
        else:
            param = sub.find('paramlist/param[@name="value"]')
            assert param is not None
            param.set('value', value)


    def __delitem__(self, key: str):

        sub = self._get(key)
        self._container.remove(sub)

        substitution_sets = self._substitution_sets
        for substitution_set in substitution_sets.values():
            if key in substitution_set:
                del substitution_set[key]


#-------------------------------------------------------------------------------
# General Substitution Set
#-------------------------------------------------------------------------------

_GS_GENERAL_SUBSET_XML = (
   """<ValueSet id="{id}" classid="GlobalSubstitutionValueSet" name="{name}">
        <paramlist />
      </ValueSet>""")

class SubstitutionSet(SubstitutionSetBase):
    """
    Global Substitution Set

    A "dictionary" of NAME=VALUE pairs, stored in the Project XML as::

      <ValueSet id="#" ... name="SET_NAME">
         <paramlist>
            <param name="NAME" value="VALUE" />
            ...
         </paramlist>
      </ValueSet>
    """

    @property
    def name(self) -> str:
        """
        Name of the Substitution Set
        """

        return self._container.get('name', '')


    def __len__(self) -> int:

        return len(self._container.findall('paramlist/param'))


    def __iter__(self) -> Iterator[str]:

        for param in self._container.iterfind('paramlist/param'):
            yield param.get('name', '')


    def _find(self, key: str) -> Optional[XmlNode]:

        if not key.isidentifier():
            raise KeyError(f"Invalid key {key!r}")

        node = self._container.find(f'paramlist/param[@name={key!r}]')
        return cast(XmlNode, node)


    def _get(self, key: str) -> XmlNode:

        param = self._find(key)
        if param is None:
            raise KeyError(key)

        return param


    def __getitem__(self, key: str) -> str:

        param = self._get(key)
        return param.get('value', '')


    def __setitem__(self, key: str, value: Any):

        value = str(value)
        param = self._find(key)
        if param is None:
            if key not in self._substitution_sets['']:
                raise KeyError(f"No default exists for {key!r}")

            paramlist = cast(XmlNode, self._container.find('paramlist'))
            param = cast(XmlNode, paramlist.makeelement('param', name=key))
            paramlist.append_indented(param)

        return param.set('value', value)


    def __delitem__(self, key: str):

        param = self._get(key)
        param._remove_from_parent()

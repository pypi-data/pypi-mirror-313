"""
MHI's XML Nodes

Includes:
   - XmlNode       (a few extra methods, ...)
   - NamedNode     <node name='A-Name'/>
   - IdNode        <node id='10'/>
   - NamedIdNode   <node name='A-Name' id='10'/>
   - and so on.
"""

#===============================================================================
# Imports
#===============================================================================

from __future__ import annotations

from collections import ChainMap
from collections.abc import MutableMapping, ItemsView
from typing import get_type_hints, cast, TYPE_CHECKING
from typing import Any, ClassVar, Iterator, Optional, TypeVar, Union
from warnings import warn
from lxml import etree as ET

if TYPE_CHECKING:
    import mhi.xml.file


#===============================================================================
# Exports
#===============================================================================

__all__ = ['XmlNode',
           'NamedNode', 'NamedNodeContainerMapping',
           'KeyMapping',
           'IdNode', 'NamedIdNode',
           'ParamNode', 'ParamListNode', 'ParametersBase',
           'TagLookup', 'param_tag_lookup',
           ]


#===============================================================================

class TagLookup(ET.CustomElementClassLookup):
    """
    Tag-based XML Class Looking

    The class supports a chain of dictionary lookups, going from
    XML tag name to Python class for that tag.
    File specific lookup objects can delegate to other lookup objects
    for XML tags common to a variety of files.
    """

    _tag_map: ChainMap[str, XmlNode]


    def __init__(self, parent: Optional[TagLookup] = None):

        if parent:
            self._tag_map = parent._tag_map.new_child()
        else:
            self._tag_map = ChainMap()


    def __call__(self, tag):
        """
        Decorator, used to register a tag-class pair to this lookup object

        Usage:
            @tag_lookup_object("tagname")
            class SomeClass(XmlNode):
                ...
        """

        def wrapper(cls):
            if tag in self._tag_map.maps[0]:
                raise KeyError(f"Duplicate tag {tag!r}")

            self._tag_map[tag] = cls
            return cls

        return wrapper


    def lookup(self, node_type, document, namespace, name): # pylint: disable=unused-argument
        """
        Return a type to be used for the given XML element

        Parameters:
            node_type: one of 'element', 'comment', 'PI', 'entity'
            doc: document that the node is in
            namespace: namespace URI of the node (None for comments/PIs/entities)
            name: name of the element/entity (None for comments, target for PIs)
        """

        if node_type == 'element':
            return self._tag_map.get(name, XmlNode)

        # Fallback for non-element nodes
        return None


param_tag_lookup = TagLookup()


#===============================================================================

class XmlNode(ET.ElementBase):
    """
    Custom nase for XML nodes
    """


    @property
    def _parser(self):
        """
        Return the parser used to parse the XML tree
        """

        return self.getroottree().parser


    def _parse(self, xml_str: str) -> ET._Element:
        """
        Parse an XML string into an ElementTree node
        """

        return ET.fromstring(xml_str, self._parser)


    @property
    def _file(self) -> mhi.xml.file.File:
        """
        Return the file object which holds the XML tree
        """

        root = cast(RootNode, self.getroottree().getroot())

        return root._file_ref               # pylint: disable=protected-access


    def _remove_from_parent(self):
        tail = self.tail
        predecessor = self.getprevious()
        successor = self.getnext()
        parent = self.getparent()
        assert parent is not None
        parent.remove(self)
        if len(parent) == 0:
            parent.text = None
        elif successor is None:
            predecessor.tail = tail


    def set_modified(self):
        """
        Mark the file containing this node as modified.
        """

        self._file.set_modified()


    def append_text(self, text: str) -> None:
        """
        Append the given text string to the content inside this node.

        If the node contains other elements, the text is added
        to the last child's `tail`, instead of as this node's `text`.
        """

        if len(self) > 0:
            last_child = self[-1]
            if last_child.tail:
                last_child.tail += text
            else:
                last_child.tail = text
        else:
            if self.text:
                self.text += text
            else:
                self.text = text


    def append_indented(self, node: ET._Element,
                        spaces: int = -1, space_inc: int = 2) -> None:
        """
        Append a child node to the children of the current node, with
        white-space before and after the element to maintain proper
        indentation.

        Note: The child's content is not modified; it is assumed to already
        be properly indented.
        """

        if spaces < 0:

            tail = str(self.tail or "")     # pylint was confused about tail
            spaces = len(tail.lstrip('\n')) if tail else 0
            if self.getnext() is None:
                spaces += space_inc

        indent = "\n" + " " * spaces
        indent_inc = " " * space_inc

        if len(self) == 0:
            if self.text is None:
                self.text = indent
            self.text += indent_inc
        else:
            last_child = self[-1]
            if last_child.tail is None:
                last_child.tail = indent
            last_child.tail += indent_inc

        node.tail = indent
        self.append(node)


    def create_param_list_node(self, **kwargs) -> ParamListNode:
        """
        Add a <paramlist/> child node
        """

        kwargs = {key: str(val) for key, val in kwargs.items()}
        node = self.makeelement('paramlist', **kwargs)
        paramlist = cast(ParamListNode, node)

        self.append_indented(paramlist)

        return paramlist


#===============================================================================

class RootNode(XmlNode):
    """
    The Root Node of a file

    This will hold a reference to the File object
    """

    _file_ref: mhi.xml.file.File


#===============================================================================

class NamedNode(XmlNode):
    """
    An XML node with a read-only `name` attribute

    <tag name='something'>
    """


    @property
    def name(self) -> str:
        """
        The value of the `name` attribute
        """

        name = self.get('name')
        assert name is not None

        return name


#===============================================================================

Key = Union[str, int]
KeyedNode = TypeVar('KeyedNode', bound=XmlNode)
ANamedNode = TypeVar('ANamedNode', bound=NamedNode)


#===============================================================================

class KeyMapping(MutableMapping[str, KeyedNode]):
    """
    A container that contains elements identified by a key-value.

    The elements do not need to be a direct child of the container.
    In the following structure, an instance of `KeyMapping` could be used
    to map to `subcontainer[@key='...']`, while another instance could
    map to `subcontainer/tag[@name='...']`::

      <container>
        <subcontainer key='key_a'>
          <tag name='name1' />
          <tag name='name2' />
        </subcontainer>
        <subcontainer key='key_b'>
          <tag name='name3' />
          <tag name='name4' />
        </subcontainer>
      </container>

    Keyed Nodes can be found or deleted, but not added unless the path
    is a direct child node.
    """

    def __init__(self, container: XmlNode, path: str, attr: str,
                 class_name: Optional[str] = None):

        self._container = container
        self._path = path
        self._attr = attr
        self._name = class_name or self.__class__.__name__


    def _validate_key(self, key: str):

        if not isinstance(key, str):
            raise ValueError(f'Invalid name: "{key!s}"')


    def _find(self, key: str) -> Optional[KeyedNode]:

        self._validate_key(key)

        xpath = f'{self._path}[@{self._attr}="{key!s}"]'
        keyed_node = cast(KeyedNode, self._container.find(xpath))
        return keyed_node


    def _get(self, key: str) -> KeyedNode:

        keyed_node = self._find(key)
        if keyed_node is None:
            raise KeyError(key)

        return keyed_node


    def __contains__(self, key) -> bool:

        return self._find(key) is not None


    def __getitem__(self, key: str) -> KeyedNode:

        return self._get(key)


    def __setitem__(self, key: str, keyed_node: KeyedNode) -> None:

        if '/' in self._path:
            raise NotImplementedError("Cannot add grandchildren!")

        if self._find(key) is not None:
            raise KeyError(f'"{key!s}" already exists')

        self._pre_add(key, keyed_node)

        keyed_node.set(self._attr, key)
        self._container.append_indented(keyed_node)


    def _pre_add(self, key: str, keyed_node: KeyedNode) -> None:

        pass


    def __delitem__(self, key: str) -> None:

        keyed_node = self._get(key)
        keyed_node._remove_from_parent()


    def __iter__(self) -> Iterator[str]:

        for keyed_node in self._container.iterfind(self._path):
            yield keyed_node.get(self._attr, '')


    def items(self) -> ItemsView[str, KeyedNode]:

        class _ItemsView(ItemsView[str, KeyedNode]):

            _mapping: KeyMapping

            def __iter__(self) -> Iterator[tuple[str, KeyedNode]]:
                mapping = self._mapping

                for node in mapping._container.iterfind(mapping._path):
                    keyed_node = cast(KeyedNode, node)
                    yield keyed_node.get(mapping._attr, ''), keyed_node

        return _ItemsView(self)


    def __len__(self) -> int:

        return len(self._container.findall(self._path))


    def __repr__(self):

        return f"{self._name}[{', '.join(self.keys())}]"



#===============================================================================

class NamedNodeContainerMapping(KeyMapping[ANamedNode]):
    """
    An XML node that contains a subtype of `NamedNode` elements.

    The NamedNode tag must be stored in the `_CHILD_TAG` of
    the container mapping.

    Each `NamedNode` can be referenced by name or index.

    <container>
      <tag name='name1' />
      <tag name='name2' />
    </container>
    """


    def __init__(self, container: XmlNode, tag: str,
                 class_name: Optional[str] = None):

        super().__init__(container, tag, 'name', class_name)


    def names(self):
        """
        List all the name keys in the container
        """

        return list(self.keys())



#===============================================================================

class IdNode(XmlNode):
    """
    An XML node with a read-only `id` attribute

    <tag id='123456789'>
    """

    @property
    def id(self) -> int:
        """
        The value of the `id` attribute
        """

        return int(self.get('id', '0'))


#===============================================================================

class NamedIdNode(NamedNode, IdNode):
    """
    An XML node with read-only `name` and `id` attributes

    <tag name='something' id='123456789'>
    """


#===============================================================================

@param_tag_lookup('param')
class ParamNode(NamedNode):
    """
    A param node, contained in a `paramlist` node container.

    A param have both a name and a value.  Usually, the value is stored
    as a `value` attribute, but may be stored as child nodes for complex
    values (such as tables).

    <paramlist>
      <param name="p1" value="10"/>
      <param name="p2" value="true"/>
      ...
    </paramlist>
    """


    @property
    def value(self) -> str:
        """
        The value of the param node, returned as a string
        """

        value = self.get('value')
        if value is None:
            raise NotImplementedError("Non-attribute values not yet supported")

        return value


    @value.setter
    def value(self, value: str):

        if isinstance(value, str):
            self.set('value', str(value))
        else:
            warn(f"Expected string, got {type(value)}", stacklevel=2)
            self.set_value(value)


    def set_value(self, value: Union[bool, int, float, str, None]):
        """
        Set the parameter's value

        Conversion is done from all value types to a PSCAD-esque string value
        """

        if value is None:
            value = ''
        elif isinstance(value, bool):
            value = str(value).lower()
        self.set('value', str(value))


    def __bool__(self) -> bool:

        value = self.value.casefold()
        if value == 'false':
            return False
        if value == 'true':
            return True
        raise ValueError(f"Expected 'true' or 'false', not {value!r}")


    def __int__(self) -> int:

        return int(self.value)


    def __float__(self) -> float:

        return float(self.value)


    def __str__(self) -> str:

        return self.value


#===============================================================================

@param_tag_lookup('paramlist')
class ParamListNode(NamedNode):
    """
    A container of `<param/>` nodes.
    """


    def _find_param(self, name):

        return self.find(f"param[@name={name!r}]")


    def _param(self, name: str):

        param = self._find_param(name)
        if param is None:
            raise KeyError(f"No such param: {name!r}")
        return param


    def get_param(self, name: str) -> str:
        """
        Return the named parameter's value, as a string
        """

        return self._param(name).value


    def set_param(self, name: str, value: Any) -> None:
        """
        Set the named parameter's value
        """

        self._param(name).set_value(value)


    def __getitem__(self, key):

        if isinstance(key, str):
            return self._param(key)
        return super().__getitem__(key)


    def __setitem__(self, key, value):

        if isinstance(key, str):
            self._param(key).value = value
        else:
            super().__setitem__(key, value)


    def __contains__(self, key: str) -> bool:
        return self._find_param(key) is not None


    def has_keys(self, *keys: str) -> bool:
        """
        Test if the `<paramlist/>` contains all of the given keys
        """

        return all(self._find_param(key) is not None for key in keys)


    def missing_keys(self, *keys: str) -> str:
        """
        Returns a comma-separated string of which keys of the given keys
        are not present in the `<paramlist/>`.

        Returns an empty string if all keys are found.
        """

        return ", ".join(key for key in keys if self._find_param(key) is None)


    def as_dict(self) -> dict[str, str]:
        """
        Returns all of the `<paramlist/>` parameters as a dictionary.

        No attempt is made to convert values to other types.
        """

        return {param.get('name', ''): param.get('value', '') for param in self}


    def create_param(self, name: str, val: Any) -> ParamNode:
        """
        Create and add a new `<param name={name} value={val}>` node
        """

        if isinstance(val, bool):
            val = 'true' if val else 'false'

        param = self.makeelement('param', name=name, value=str(val))
        param = cast(ParamNode, param)

        self.append_indented(param)

        return param


    def create_params(self, dct: Optional[dict[str, Any]] = None,
                      **kwargs) -> None:
        """
        Create and add new `<param name="..." value="...">` nodes
        """

        if dct:
            if kwargs:
                kwargs = dct | kwargs
            else:
                kwargs = dct

        for key, val in kwargs.items():
            self.create_param(key, val)


    def __repr__(self):
        params = ", ".join(f"{param.name}={param.value!r}"
                           for param in self)
        return f"ParamList[{params}]"


#===============================================================================

class ParamDescriptor:
    """
    Data descriptor for known parameters
    """

    __slots__ = ('name', 'kind')


    def __init__(self, name: str, kind: type):

        self.name = name
        self.kind = kind


    def __get__(self, obj, objtype=None):

        if obj is None:
            return self

        param = obj._param_list._param(self.name)
        kind = self.kind
        if kind in {bool, int, float, str}:
            return kind(param)

        return kind(param.value)


    def __set__(self, obj, value):

        kind = self.kind
        if callable(getattr(kind, 'encode_to_str', None)):
            value = kind.encode_to_str(value)

        param = obj._param_list._param(self.name)
        param.set_value(value)


#===============================================================================

class ParametersBase:
    """
    A typed-enhanced proxy of a `<paramlist/>`.

    The type for a param's value is determine using the type-hint
    for that member name.

    Example:
        class MyParameters(ParametersBase):
            enabled: bool
            time_step: float
            num_runs: int
    """


    __slots__ = ('_param_list',)

    _unknown_type: ClassVar[type] = str
    _defaults: ClassVar[dict[str, Any]] = {}

    def __init__(self, param_list: Optional[ET._Element]):

        assert isinstance(param_list, ParamListNode)

        if not self._defaults:
            self._set_parameter_types()

        object.__setattr__(self, '_param_list', param_list)


    def __init_subclass__(cls, /, unknown_type: type = str, **kwargs):
        super().__init_subclass__(**kwargs)

        cls._unknown_type = unknown_type
        cls._defaults = {}

        try:
            cls._set_parameter_types()
        except NameError:
            pass


    @classmethod
    def _set_parameter_types(cls):

        types = get_type_hints(cls)
        for name, kind in types.items():
            if not name.startswith('_'):
                cls._set_type(name, kind)


    @classmethod
    def _set_type(cls, name: str, a_type: type):
        """
        Assign a type to an untyped parameter
        """

        param = ParamDescriptor(name, a_type)
        if hasattr(cls, name):
            cls._defaults[name] = getattr(cls, name)
        setattr(cls, name, param)


    def __getattr__(self, name):

        if not name.startswith('_'):
            param = self._param_list._find_param(name)
            if param is not None:
                param_type = type(self)._unknown_type
                return param_type(param.value)

        raise AttributeError(f"No such parameter: {name!r}")


    def __setattr__(self, name, value):

        attr = getattr(type(self), name, None)
        if attr is not None:
            attr.__set__(self, value)
            return

        param = self._param_list._find_param(name)
        if param is None:
            raise AttributeError(f"No such parameter: {name!r}")

        param_type = type(self)._unknown_type
        if not isinstance(value, param_type):
            raise TypeError(f"Expected {param_type} for {name!r}")

        param.set_value(value)


    def as_dict(self) -> dict[str, Any]:
        """
        Return all of the parameters as a dictionary
        """

        if self._param_list is not None:
            return {param.name: getattr(self, param.name)
                    for param in self._param_list}
        return {}


    def set_defaults(self):
        """
        Create all parameters, assigning using their default values
        """

        self._param_list.create_params(**self._defaults)


    def __repr__(self):

        params = ", ".join(f"{key}={val!r}"
                           for key, val in self.as_dict().items())
        return f"{self.__class__.__name__}[{params}]"

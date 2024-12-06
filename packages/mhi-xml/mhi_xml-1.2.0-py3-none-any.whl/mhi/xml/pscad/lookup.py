"""
XML Tag to Python Class lookup parser factory
"""

from lxml import etree as ET
from mhi.xml.node import TagLookup, XmlNode

class Lookup:
    """
    Register `<tag classid='xxx' />` XML elements with a Python class
    for XML element-to-object mapping.
    """

    _tag: TagLookup
    _map: dict[str, XmlNode]

    def __init__(self, base_tag_lookup):
        self._tag = TagLookup(base_tag_lookup)
        self._classid = {}
        self._defn = {}

    @property
    def tag(self):
        """
        Decorator for `@xxx.tag('Tag')` decorations
        """

        return self._tag


    def classid(self, class_id: str):
        """
        Decorator for `@xxx.classid('classid_name')` decorations
        """

        def wrapper(cls):
            if class_id in self._classid:
                raise KeyError(f"Duplicate classid {class_id!r}")
            self._classid[class_id] = cls
            return cls

        return wrapper


    def defn(self, defn: str):
        """
        Decorator for `@xxx.defn('project:defn_name')` decorations
        """

        def wrapper(cls):
            if defn in self._defn:
                raise KeyError(f"Duplicate classid {defn!r}")
            self._defn[defn] = cls
            return cls

        return wrapper


    def parser(self, **kwargs) -> ET.XMLParser:
        """
        Generate a parser which maps

        Example::

            # For <ATag ... /> nodes:
            @parser.tag('ATag')
            class ATagClass:
                ...

            # For <DontCare classid='SomeClass' ... /> nodes:
            @parser.classid('SomeClassId')
            class SomeClassIdClass:
                ...
        """

        parser = ET.XMLParser(**kwargs)

        lookup = ET.AttributeBasedElementClassLookup(
            'classid', self._classid, self._tag)
        lookup = ET.AttributeBasedElementClassLookup(
            'defn', self._defn, lookup)
        parser.set_element_class_lookup(lookup)

        return parser

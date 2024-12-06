"""
XML entities for PSCAD project XML elements
"""

#===============================================================================
# Imports
#===============================================================================

from __future__ import annotations

from typing import cast, TYPE_CHECKING

from mhi.xml.node import param_tag_lookup
from mhi.xml.file import FileProtocol
from mhi.xml.pscad.lookup import Lookup

if TYPE_CHECKING:
    from mhi.xml.pscad.project import ProjectFile


#===============================================================================
# Exports
#===============================================================================

__all__ = ['project_lookup', 'ProjectMixin']


#===============================================================================
# Project XML Lookup
#===============================================================================

project_lookup = Lookup(param_tag_lookup)


#===============================================================================
# Project File Lookup
#===============================================================================

class ProjectMixin(FileProtocol):       # pylint: disable=too-few-public-methods
    """
    XML elements in PSCAD Projects should have access to the ProjectFile
    """

    @property
    def project(self) -> ProjectFile:
        """
        Retrieve the ProjectFile
        """

        return cast('ProjectFile', self._file)

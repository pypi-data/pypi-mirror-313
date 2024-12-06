"""
Library for reading/updating various kinds of MHI-specific XML files
"""

_VERSION = (1, 2, 0)

_TYPE = 'f0'

VERSION = '{0}.{1}.{2}'.format(*_VERSION, _TYPE) # pylint: disable=consider-using-f-string
VERSION_HEX = int.from_bytes((*_VERSION, int(_TYPE, 16)), byteorder='big')

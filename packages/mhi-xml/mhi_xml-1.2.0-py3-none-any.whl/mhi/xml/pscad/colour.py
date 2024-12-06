"""
======
Colour
======
"""


#===============================================================================
# Imports
#===============================================================================

from __future__ import annotations
from typing import ClassVar, Optional, Union


#===============================================================================
# Exports
#===============================================================================

__all__ = ['Colour',
           ]


#===============================================================================
# Colour Meta Class
#===============================================================================

class ColourMeta(type):
    """
    Meta class for Colour

    Enables `Color[name]` look-ups
    """

    def __getitem__(cls, name: str) -> Colour:
        """
        Add `Colour[name]` lookups to the `Colour` class (like Enum).
        """

        colour_name = name.casefold()
        if colour_name in Colour._BY_NAME:
            return Colour._BY_NAME[colour_name]
        raise KeyError(name)


    def __call__(cls, *args):
        """
        Add `Colour(name)` lookups, for "singleton" named colours.
        Return Colour(colour) unchanged.
        """

        if len(args) == 1:
            colour = args[0]
            if isinstance(colour, cls):
                return colour
            if isinstance(colour, str):
                if named_colour := cls._BY_NAME.get(colour.casefold()):
                    return named_colour

        return super().__call__(*args)


#===============================================================================
# Colour
#===============================================================================

class Colour(metaclass=ColourMeta):
    """
    Colour class

    Colour(r, g, b, a)  - create a colour using full ARGB info
    Colour(r, g, b)     - create a colour using RGB info (default max alpha)
    Colour("#aarrggbb")
    Colour("#rrggbb")
    Colour("#argb")
    Colour("#rgb")
    Colour(0xrr_gg_bb)  - create a colour using RGB info
    """

    __slots__ = ('_argb', '_name')
    _BY_NAME: ClassVar[dict[str, Colour]] = {}

    _argb: int
    _name: Optional[str]


    #-----------------------------------------------------------------------

    @classmethod
    def register(cls, name: str, *args, named=True) -> None:
        """
        Register standard-named colours
        """

        # Create brand-new colour object
        name = name.casefold()
        colour = Colour(*args)
        if named:
            colour._name = name             # pylint: disable=protected-access

        # Replace with existing one, if duplicate colour found
        for clr in cls._BY_NAME.values():
            if clr == colour:
                colour = clr

        cls._BY_NAME[name] = colour

        # Create alias if name ends with "1", and unnumbered name doesn't exist
        if name[-1] == '1' and not name[-2].isdecimal():
            name = name[:-1]
            if name not in cls._BY_NAME:
                if named:
                    colour._name = name     # pylint: disable=protected-access
                cls._BY_NAME[name] = colour


    #-----------------------------------------------------------------------

    def __init__(self, clr: Union[Colour, int, str], *args: int):

        self._name = None
        if args:
            if not isinstance(clr, int):
                raise ValueError("Integer expected with multiple arguments")
            if len(args) == 3:
                r, (g, b, a) = clr, args
            elif len(args) == 2:
                r, (g, b), a = clr, args, 255
            else:
                raise ValueError("Invalid number of arguments")
            self._argb = int.from_bytes((a, r, g, b), 'big')

        elif isinstance(clr, int):
            r, g, b = clr.to_bytes(3, 'big')
            self._argb = int.from_bytes((255, r, g, b), 'big')

        elif isinstance(clr, str) and clr.startswith('#'):
            s = clr[1:]
            if len(s) in {3, 4}:
                s = "".join(c+c for c in s)
            if len(s) == 6:
                s  = "ff" + s
            elif len(s) != 8:
                raise ValueError(f"Invalid Colour format: {clr!r}")
            self._argb = int(s, 16)

        else:
            raise ValueError(f"Invalid argument: {clr!r}")


    #-----------------------------------------------------------------------

    @property
    def argb(self) -> bytes:
        """The 'a, r, g, and b' channel values as 4 bytes (read-only)"""
        return self._argb.to_bytes(4, 'big')


    @property
    def a(self) -> int:
        """The 'alpha' channel value (read-only)"""
        return self.argb[0]


    @property
    def r(self) -> int:
        """The 'red' channel value (read-only)"""
        return self.argb[1]


    @property
    def g(self) -> int:
        """The 'green' channel value (read-only)"""
        return self.argb[2]


    @property
    def b(self) -> int:
        """The 'blue' channel value (read-only)"""
        return self.argb[3]


    #-----------------------------------------------------------------------

    def __eq__(self, other) -> bool:

        if isinstance(other, Colour):
            return self._argb == other._argb
        return False


    #-----------------------------------------------------------------------

    def __str__(self):

        return f'#{self._argb:08x}'


    def __repr__(self):

        if self._name:
            return f'Colour({self._name!r})'

        a, r, g, b = self.argb
        return f'Colour({r}, {g}, {b}, {a})'


#===============================================================================

# Colours from Window's online document
Colour.register("aliceblue", 0xF0F8FF)
Colour.register("antiquewhite", 0xFAEBD7)
Colour.register("aqua", 0x00FFFF)
Colour.register("aquamarine", 0x7FFFD4)
Colour.register("azure", 0xF0FFFF)
Colour.register("beige", 0xF5F5DC)
Colour.register("bisque", 0xFFE4C4)
Colour.register("black", 0x000000)
Colour.register("blanchedalmond", 0xFFEBCD)
Colour.register("blue", 0x0000FF)
Colour.register("blueviolet", 0x8A2BE2)
Colour.register("brown", 0xA52A2A)
Colour.register("burlywood", 0xDEB887)
Colour.register("cadetblue", 0x5F9EA0)
Colour.register("chartreuse", 0x7FFF00)
Colour.register("chocolate", 0xD2691E)
Colour.register("coral", 0xFF7F50)
Colour.register("cornflower", 0x6495ED)
Colour.register("cornsilk", 0xFFF8DC)
Colour.register("crimson", 0xDC143C)
Colour.register("cyan", 0x00FFFF)
Colour.register("darkblue", 0x00008B)
Colour.register("darkcyan", 0x008B8B)
Colour.register("darkgoldenrod", 0xB8860B)
Colour.register("darkgray", 0xA9A9A9)
Colour.register("darkgreen", 0x006400)
Colour.register("darkkhaki", 0xBDB76B)
Colour.register("darkmagenta", 0x8B008B)
Colour.register("darkolivegreen", 0x556B2F)
Colour.register("darkorange", 0xFF8C00)
Colour.register("darkorchid", 0x9932CC)
Colour.register("darkred", 0x8B0000)
Colour.register("darksalmon", 0xE9967A)
Colour.register("darkseagreen", 0x8FBC8B)
Colour.register("darkslateblue", 0x483D8B)
Colour.register("darkslategray", 0x2F4F4F)
Colour.register("darkturquoise", 0x00CED1)
Colour.register("darkviolet", 0x9400D3)
Colour.register("deeppink", 0xFF1493)
Colour.register("deepskyblue", 0x00BFFF)
Colour.register("dimgray", 0x696969)
Colour.register("dodgerblue", 0x1E90FF)
Colour.register("firebrick", 0xB22222)
Colour.register("floralwhite", 0xFFFAF0)
Colour.register("forestgreen", 0x228B22)
Colour.register("fuchsia", 0xFF00FF)
Colour.register("gainsboro", 0xDCDCDC)
Colour.register("ghostwhite", 0xF8F8FF)
Colour.register("gold", 0xFFD700)
Colour.register("goldenrod", 0xDAA520)
Colour.register("gray", 0x808080)
Colour.register("green", 0x008000)
Colour.register("greenyellow", 0xADFF2F)
Colour.register("honeydew", 0xF0FFF0)
Colour.register("hotpink", 0xFF69B4)
Colour.register("indianred", 0xCD5C5C)
Colour.register("indigo", 0x4B0082)
Colour.register("ivory", 0xFFFFF0)
Colour.register("khaki", 0xF0E68C)
Colour.register("lavender", 0xE6E6FA)
Colour.register("lavenderblush", 0xFFF0F5)
Colour.register("lawngreen", 0x7CFC00)
Colour.register("lemonchiffon", 0xFFFACD)
Colour.register("lightblue", 0xADD8E6)
Colour.register("lightcoral", 0xF08080)
Colour.register("lightcyan", 0xE0FFFF)
Colour.register("lightgoldenrodyellow", 0xFAFAD2)
Colour.register("lightgreen", 0x90EE90)
Colour.register("lightgray", 0xD3D3D3)
Colour.register("lightpink", 0xFFB6C1)
Colour.register("lightsalmon", 0xFFA07A)
Colour.register("lightseagreen", 0x20B2AA)
Colour.register("lightskyblue", 0x87CEFA)
Colour.register("lightslategray", 0x778899)
Colour.register("lightsteelblue", 0xB0C4DE)
Colour.register("lightyellow", 0xFFFFE0)
Colour.register("lime", 0x00FF00)
Colour.register("limegreen", 0x32CD32)
Colour.register("linen", 0xFAF0E6)
Colour.register("magenta", 0xFF00FF)
Colour.register("maroon", 0x800000)
Colour.register("mediumaquamarine", 0x66CDAA)
Colour.register("mediumblue", 0x0000CD)
Colour.register("mediumorchid", 0xBA55D3)
Colour.register("mediumpurple", 0x9370DB)
Colour.register("mediumseagreen", 0x3CB371)
Colour.register("mediumslateblue", 0x7B68EE)
Colour.register("mediumspringgreen", 0x00FA9A)
Colour.register("mediumturquoise", 0x48D1CC)
Colour.register("mediumvioletred", 0xC71585)
Colour.register("midnightblue", 0x191970)
Colour.register("mintcream", 0xF5FFFA)
Colour.register("mistyrose", 0xFFE4E1)
Colour.register("moccasin", 0xFFE4B5)
Colour.register("navajowhite", 0xFFDEAD)
Colour.register("navy", 0x000080)
Colour.register("oldlace", 0xFDF5E6)
Colour.register("olive", 0x808000)
Colour.register("olivedrab", 0x6B8E23)
Colour.register("orange", 0xFFA500)
Colour.register("orangered", 0xFF4500)
Colour.register("orchid", 0xDA70D6)
Colour.register("palegoldenrod", 0xEEE8AA)
Colour.register("palegreen", 0x98FB98)
Colour.register("paleturquoise", 0xAFEEEE)
Colour.register("palevioletred", 0xDB7093)
Colour.register("papayawhip", 0xFFEFD5)
Colour.register("peachpuff", 0xFFDAB9)
Colour.register("peru", 0xCD853F)
Colour.register("pink", 0xFFC0CB)
Colour.register("plum", 0xDDA0DD)
Colour.register("powderblue", 0xB0E0E6)
Colour.register("purple", 0x800080)
Colour.register("red", 0xFF0000)
Colour.register("rosybrown", 0xBC8F8F)
Colour.register("royalblue", 0x4169E1)
Colour.register("saddlebrown", 0x8B4513)
Colour.register("salmon", 0xFA8072)
Colour.register("sandybrown", 0xF4A460)
Colour.register("seagreen", 0x2E8B57)
Colour.register("seashell", 0xFFF5EE)
Colour.register("sienna", 0xA0522D)
Colour.register("silver", 0xC0C0C0)
Colour.register("skyblue", 0x87CEEB)
Colour.register("slateblue", 0x6A5ACD)
Colour.register("slategray", 0x708090)
Colour.register("snow", 0xFFFAFA)
Colour.register("springgreen", 0x00FF7F)
Colour.register("steelblue", 0x4682B4)
Colour.register("tan", 0xD2B48C)
Colour.register("teal", 0x008080)
Colour.register("thistle", 0xD8BFD8)
Colour.register("tomato", 0xFF6347)
Colour.register("turquoise", 0x40E0D0)
Colour.register("violet", 0xEE82EE)
Colour.register("wheat", 0xF5DEB3)
Colour.register("white", 0xFFFFFF)
Colour.register("whitesmoke", 0xF5F5F5)
Colour.register("yellow", 0xFFFF00)
Colour.register("yellowgreen", 0x9ACD32)


# Additional CSS colours from Webucator.com
Colour.register("ANTIQUEWHITE1", 255, 239, 219)
Colour.register("ANTIQUEWHITE2", 238, 223, 204)
Colour.register("ANTIQUEWHITE3", 205, 192, 176)
Colour.register("ANTIQUEWHITE4", 139, 131, 120)
Colour.register("AQUAMARINE1", 127, 255, 212)
Colour.register("AQUAMARINE2", 118, 238, 198)
Colour.register("AQUAMARINE3", 102, 205, 170)
Colour.register("AQUAMARINE4", 69, 139, 116)
Colour.register("AZURE1", 240, 255, 255)
Colour.register("AZURE2", 224, 238, 238)
Colour.register("AZURE3", 193, 205, 205)
Colour.register("AZURE4", 131, 139, 139)
Colour.register("BANANA", 227, 207, 87)
Colour.register("BISQUE1", 255, 228, 196)
Colour.register("BISQUE2", 238, 213, 183)
Colour.register("BISQUE3", 205, 183, 158)
Colour.register("BISQUE4", 139, 125, 107)
Colour.register("BLUE1", 0, 0, 255)
Colour.register("BLUE2", 0, 0, 238)
Colour.register("BLUE3", 0, 0, 205)
Colour.register("BLUE4", 0, 0, 139)
Colour.register("BRICK", 156, 102, 31)
Colour.register("BROWN1", 255, 64, 64)
Colour.register("BROWN2", 238, 59, 59)
Colour.register("BROWN3", 205, 51, 51)
Colour.register("BROWN4", 139, 35, 35)
Colour.register("BURLYWOOD1", 255, 211, 155)
Colour.register("BURLYWOOD2", 238, 197, 145)
Colour.register("BURLYWOOD3", 205, 170, 125)
Colour.register("BURLYWOOD4", 139, 115, 85)
Colour.register("BURNTSIENNA", 138, 54, 15)
Colour.register("BURNTUMBER", 138, 51, 36)
Colour.register("CADETBLUE1", 152, 245, 255)
Colour.register("CADETBLUE2", 142, 229, 238)
Colour.register("CADETBLUE3", 122, 197, 205)
Colour.register("CADETBLUE4", 83, 134, 139)
Colour.register("CADMIUMORANGE", 255, 97, 3)
Colour.register("CADMIUMYELLOW", 255, 153, 18)
Colour.register("CARROT", 237, 145, 33)
Colour.register("CHARTREUSE1", 127, 255, 0)
Colour.register("CHARTREUSE2", 118, 238, 0)
Colour.register("CHARTREUSE3", 102, 205, 0)
Colour.register("CHARTREUSE4", 69, 139, 0)
Colour.register("CHOCOLATE1", 255, 127, 36)
Colour.register("CHOCOLATE2", 238, 118, 33)
Colour.register("CHOCOLATE3", 205, 102, 29)
Colour.register("CHOCOLATE4", 139, 69, 19)
Colour.register("COBALT", 61, 89, 171)
Colour.register("COBALTGREEN", 61, 145, 64)
Colour.register("COLDGREY", 128, 138, 135)
Colour.register("CORAL1", 255, 114, 86)
Colour.register("CORAL2", 238, 106, 80)
Colour.register("CORAL3", 205, 91, 69)
Colour.register("CORAL4", 139, 62, 47)
Colour.register("CORNFLOWERBLUE", 100, 149, 237)
Colour.register("CORNSILK1", 255, 248, 220)
Colour.register("CORNSILK2", 238, 232, 205)
Colour.register("CORNSILK3", 205, 200, 177)
Colour.register("CORNSILK4", 139, 136, 120)
Colour.register("CYAN1", 0, 255, 255)
Colour.register("CYAN2", 0, 238, 238)
Colour.register("CYAN3", 0, 205, 205)
Colour.register("CYAN4", 0, 139, 139)
Colour.register("DARKGOLDENROD1", 255, 185, 15)
Colour.register("DARKGOLDENROD2", 238, 173, 14)
Colour.register("DARKGOLDENROD3", 205, 149, 12)
Colour.register("DARKGOLDENROD4", 139, 101, 8)
Colour.register("DARKOLIVEGREEN1", 202, 255, 112)
Colour.register("DARKOLIVEGREEN2", 188, 238, 104)
Colour.register("DARKOLIVEGREEN3", 162, 205, 90)
Colour.register("DARKOLIVEGREEN4", 110, 139, 61)
Colour.register("DARKORANGE1", 255, 127, 0)
Colour.register("DARKORANGE2", 238, 118, 0)
Colour.register("DARKORANGE3", 205, 102, 0)
Colour.register("DARKORANGE4", 139, 69, 0)
Colour.register("DARKORCHID1", 191, 62, 255)
Colour.register("DARKORCHID2", 178, 58, 238)
Colour.register("DARKORCHID3", 154, 50, 205)
Colour.register("DARKORCHID4", 104, 34, 139)
Colour.register("DARKSEAGREEN1", 193, 255, 193)
Colour.register("DARKSEAGREEN2", 180, 238, 180)
Colour.register("DARKSEAGREEN3", 155, 205, 155)
Colour.register("DARKSEAGREEN4", 105, 139, 105)
Colour.register("DARKSLATEGRAY1", 151, 255, 255)
Colour.register("DARKSLATEGRAY2", 141, 238, 238)
Colour.register("DARKSLATEGRAY3", 121, 205, 205)
Colour.register("DARKSLATEGRAY4", 82, 139, 139)
Colour.register("DEEPPINK1", 255, 20, 147)
Colour.register("DEEPPINK2", 238, 18, 137)
Colour.register("DEEPPINK3", 205, 16, 118)
Colour.register("DEEPPINK4", 139, 10, 80)
Colour.register("DEEPSKYBLUE1", 0, 191, 255)
Colour.register("DEEPSKYBLUE2", 0, 178, 238)
Colour.register("DEEPSKYBLUE3", 0, 154, 205)
Colour.register("DEEPSKYBLUE4", 0, 104, 139)
Colour.register("DODGERBLUE1", 30, 144, 255)
Colour.register("DODGERBLUE2", 28, 134, 238)
Colour.register("DODGERBLUE3", 24, 116, 205)
Colour.register("DODGERBLUE4", 16, 78, 139)
Colour.register("EGGSHELL", 252, 230, 201)
Colour.register("EMERALDGREEN", 0, 201, 87)
Colour.register("FIREBRICK1", 255, 48, 48)
Colour.register("FIREBRICK2", 238, 44, 44)
Colour.register("FIREBRICK3", 205, 38, 38)
Colour.register("FIREBRICK4", 139, 26, 26)
Colour.register("FLESH", 255, 125, 64)
Colour.register("GOLD1", 255, 215, 0)
Colour.register("GOLD2", 238, 201, 0)
Colour.register("GOLD3", 205, 173, 0)
Colour.register("GOLD4", 139, 117, 0)
Colour.register("GOLDENROD1", 255, 193, 37)
Colour.register("GOLDENROD2", 238, 180, 34)
Colour.register("GOLDENROD3", 205, 155, 29)
Colour.register("GOLDENROD4", 139, 105, 20)
Colour.register("GRAY1", 3, 3, 3)
Colour.register("GRAY2", 5, 5, 5)
Colour.register("GRAY3", 8, 8, 8)
Colour.register("GRAY4", 10, 10, 10)
Colour.register("GRAY5", 13, 13, 13)
Colour.register("GRAY6", 15, 15, 15)
Colour.register("GRAY7", 18, 18, 18)
Colour.register("GRAY8", 20, 20, 20)
Colour.register("GRAY9", 23, 23, 23)
Colour.register("GRAY10", 26, 26, 26)
Colour.register("GRAY11", 28, 28, 28)
Colour.register("GRAY12", 31, 31, 31)
Colour.register("GRAY13", 33, 33, 33)
Colour.register("GRAY14", 36, 36, 36)
Colour.register("GRAY15", 38, 38, 38)
Colour.register("GRAY16", 41, 41, 41)
Colour.register("GRAY17", 43, 43, 43)
Colour.register("GRAY18", 46, 46, 46)
Colour.register("GRAY19", 48, 48, 48)
Colour.register("GRAY20", 51, 51, 51)
Colour.register("GRAY21", 54, 54, 54)
Colour.register("GRAY22", 56, 56, 56)
Colour.register("GRAY23", 59, 59, 59)
Colour.register("GRAY24", 61, 61, 61)
Colour.register("GRAY25", 64, 64, 64)
Colour.register("GRAY26", 66, 66, 66)
Colour.register("GRAY27", 69, 69, 69)
Colour.register("GRAY28", 71, 71, 71)
Colour.register("GRAY29", 74, 74, 74)
Colour.register("GRAY30", 77, 77, 77)
Colour.register("GRAY31", 79, 79, 79)
Colour.register("GRAY32", 82, 82, 82)
Colour.register("GRAY33", 84, 84, 84)
Colour.register("GRAY34", 87, 87, 87)
Colour.register("GRAY35", 89, 89, 89)
Colour.register("GRAY36", 92, 92, 92)
Colour.register("GRAY37", 94, 94, 94)
Colour.register("GRAY38", 97, 97, 97)
Colour.register("GRAY39", 99, 99, 99)
Colour.register("GRAY40", 102, 102, 102)
Colour.register("GRAY42", 107, 107, 107)
Colour.register("GRAY43", 110, 110, 110)
Colour.register("GRAY44", 112, 112, 112)
Colour.register("GRAY45", 115, 115, 115)
Colour.register("GRAY46", 117, 117, 117)
Colour.register("GRAY47", 120, 120, 120)
Colour.register("GRAY48", 122, 122, 122)
Colour.register("GRAY49", 125, 125, 125)
Colour.register("GRAY50", 127, 127, 127)
Colour.register("GRAY51", 130, 130, 130)
Colour.register("GRAY52", 133, 133, 133)
Colour.register("GRAY53", 135, 135, 135)
Colour.register("GRAY54", 138, 138, 138)
Colour.register("GRAY55", 140, 140, 140)
Colour.register("GRAY56", 143, 143, 143)
Colour.register("GRAY57", 145, 145, 145)
Colour.register("GRAY58", 148, 148, 148)
Colour.register("GRAY59", 150, 150, 150)
Colour.register("GRAY60", 153, 153, 153)
Colour.register("GRAY61", 156, 156, 156)
Colour.register("GRAY62", 158, 158, 158)
Colour.register("GRAY63", 161, 161, 161)
Colour.register("GRAY64", 163, 163, 163)
Colour.register("GRAY65", 166, 166, 166)
Colour.register("GRAY66", 168, 168, 168)
Colour.register("GRAY67", 171, 171, 171)
Colour.register("GRAY68", 173, 173, 173)
Colour.register("GRAY69", 176, 176, 176)
Colour.register("GRAY70", 179, 179, 179)
Colour.register("GRAY71", 181, 181, 181)
Colour.register("GRAY72", 184, 184, 184)
Colour.register("GRAY73", 186, 186, 186)
Colour.register("GRAY74", 189, 189, 189)
Colour.register("GRAY75", 191, 191, 191)
Colour.register("GRAY76", 194, 194, 194)
Colour.register("GRAY77", 196, 196, 196)
Colour.register("GRAY78", 199, 199, 199)
Colour.register("GRAY79", 201, 201, 201)
Colour.register("GRAY80", 204, 204, 204)
Colour.register("GRAY81", 207, 207, 207)
Colour.register("GRAY82", 209, 209, 209)
Colour.register("GRAY83", 212, 212, 212)
Colour.register("GRAY84", 214, 214, 214)
Colour.register("GRAY85", 217, 217, 217)
Colour.register("GRAY86", 219, 219, 219)
Colour.register("GRAY87", 222, 222, 222)
Colour.register("GRAY88", 224, 224, 224)
Colour.register("GRAY89", 227, 227, 227)
Colour.register("GRAY90", 229, 229, 229)
Colour.register("GRAY91", 232, 232, 232)
Colour.register("GRAY92", 235, 235, 235)
Colour.register("GRAY93", 237, 237, 237)
Colour.register("GRAY94", 240, 240, 240)
Colour.register("GRAY95", 242, 242, 242)
Colour.register("GRAY97", 247, 247, 247)
Colour.register("GRAY98", 250, 250, 250)
Colour.register("GRAY99", 252, 252, 252)
Colour.register("GREEN1", 0, 255, 0)
Colour.register("GREEN2", 0, 238, 0)
Colour.register("GREEN3", 0, 205, 0)
Colour.register("GREEN4", 0, 139, 0)
Colour.register("HONEYDEW1", 240, 255, 240)
Colour.register("HONEYDEW2", 224, 238, 224)
Colour.register("HONEYDEW3", 193, 205, 193)
Colour.register("HONEYDEW4", 131, 139, 131)
Colour.register("HOTPINK1", 255, 110, 180)
Colour.register("HOTPINK2", 238, 106, 167)
Colour.register("HOTPINK3", 205, 96, 144)
Colour.register("HOTPINK4", 139, 58, 98)
Colour.register("INDIANRED1", 255, 106, 106)
Colour.register("INDIANRED2", 238, 99, 99)
Colour.register("INDIANRED3", 205, 85, 85)
Colour.register("INDIANRED4", 139, 58, 58)
Colour.register("IVORY1", 255, 255, 240)
Colour.register("IVORY2", 238, 238, 224)
Colour.register("IVORY3", 205, 205, 193)
Colour.register("IVORY4", 139, 139, 131)
Colour.register("IVORYBLACK", 41, 36, 33)
Colour.register("KHAKI1", 255, 246, 143)
Colour.register("KHAKI2", 238, 230, 133)
Colour.register("KHAKI3", 205, 198, 115)
Colour.register("KHAKI4", 139, 134, 78)
Colour.register("LAVENDERBLUSH1", 255, 240, 245)
Colour.register("LAVENDERBLUSH2", 238, 224, 229)
Colour.register("LAVENDERBLUSH3", 205, 193, 197)
Colour.register("LAVENDERBLUSH4", 139, 131, 134)
Colour.register("LEMONCHIFFON1", 255, 250, 205)
Colour.register("LEMONCHIFFON2", 238, 233, 191)
Colour.register("LEMONCHIFFON3", 205, 201, 165)
Colour.register("LEMONCHIFFON4", 139, 137, 112)
Colour.register("LIGHTBLUE1", 191, 239, 255)
Colour.register("LIGHTBLUE2", 178, 223, 238)
Colour.register("LIGHTBLUE3", 154, 192, 205)
Colour.register("LIGHTBLUE4", 104, 131, 139)
Colour.register("LIGHTCYAN1", 224, 255, 255)
Colour.register("LIGHTCYAN2", 209, 238, 238)
Colour.register("LIGHTCYAN3", 180, 205, 205)
Colour.register("LIGHTCYAN4", 122, 139, 139)
Colour.register("LIGHTGOLDENROD1", 255, 236, 139)
Colour.register("LIGHTGOLDENROD2", 238, 220, 130)
Colour.register("LIGHTGOLDENROD3", 205, 190, 112)
Colour.register("LIGHTGOLDENROD4", 139, 129, 76)
Colour.register("LIGHTGREY", 211, 211, 211)
Colour.register("LIGHTPINK1", 255, 174, 185)
Colour.register("LIGHTPINK2", 238, 162, 173)
Colour.register("LIGHTPINK3", 205, 140, 149)
Colour.register("LIGHTPINK4", 139, 95, 101)
Colour.register("LIGHTSALMON1", 255, 160, 122)
Colour.register("LIGHTSALMON2", 238, 149, 114)
Colour.register("LIGHTSALMON3", 205, 129, 98)
Colour.register("LIGHTSALMON4", 139, 87, 66)
Colour.register("LIGHTSKYBLUE1", 176, 226, 255)
Colour.register("LIGHTSKYBLUE2", 164, 211, 238)
Colour.register("LIGHTSKYBLUE3", 141, 182, 205)
Colour.register("LIGHTSKYBLUE4", 96, 123, 139)
Colour.register("LIGHTSLATEBLUE", 132, 112, 255)
Colour.register("LIGHTSTEELBLUE1", 202, 225, 255)
Colour.register("LIGHTSTEELBLUE2", 188, 210, 238)
Colour.register("LIGHTSTEELBLUE3", 162, 181, 205)
Colour.register("LIGHTSTEELBLUE4", 110, 123, 139)
Colour.register("LIGHTYELLOW1", 255, 255, 224)
Colour.register("LIGHTYELLOW2", 238, 238, 209)
Colour.register("LIGHTYELLOW3", 205, 205, 180)
Colour.register("LIGHTYELLOW4", 139, 139, 122)
Colour.register("MAGENTA2", 238, 0, 238)
Colour.register("MAGENTA3", 205, 0, 205)
Colour.register("MAGENTA4", 139, 0, 139)
Colour.register("MANGANESEBLUE", 3, 168, 158)
Colour.register("MAROON1", 255, 52, 179)
Colour.register("MAROON2", 238, 48, 167)
Colour.register("MAROON3", 205, 41, 144)
Colour.register("MAROON4", 139, 28, 98)
Colour.register("MEDIUMORCHID1", 224, 102, 255)
Colour.register("MEDIUMORCHID2", 209, 95, 238)
Colour.register("MEDIUMORCHID3", 180, 82, 205)
Colour.register("MEDIUMORCHID4", 122, 55, 139)
Colour.register("MEDIUMPURPLE1", 171, 130, 255)
Colour.register("MEDIUMPURPLE2", 159, 121, 238)
Colour.register("MEDIUMPURPLE3", 137, 104, 205)
Colour.register("MEDIUMPURPLE4", 93, 71, 139)
Colour.register("MELON", 227, 168, 105)
Colour.register("MINT", 189, 252, 201)
Colour.register("MISTYROSE1", 255, 228, 225)
Colour.register("MISTYROSE2", 238, 213, 210)
Colour.register("MISTYROSE3", 205, 183, 181)
Colour.register("MISTYROSE4", 139, 125, 123)
Colour.register("NAVAJOWHITE1", 255, 222, 173)
Colour.register("NAVAJOWHITE2", 238, 207, 161)
Colour.register("NAVAJOWHITE3", 205, 179, 139)
Colour.register("NAVAJOWHITE4", 139, 121, 94)
Colour.register("OLIVEDRAB1", 192, 255, 62)
Colour.register("OLIVEDRAB2", 179, 238, 58)
Colour.register("OLIVEDRAB3", 154, 205, 50)
Colour.register("OLIVEDRAB4", 105, 139, 34)
Colour.register("ORANGE1", 255, 165, 0)
Colour.register("ORANGE2", 238, 154, 0)
Colour.register("ORANGE3", 205, 133, 0)
Colour.register("ORANGE4", 139, 90, 0)
Colour.register("ORANGERED1", 255, 69, 0)
Colour.register("ORANGERED2", 238, 64, 0)
Colour.register("ORANGERED3", 205, 55, 0)
Colour.register("ORANGERED4", 139, 37, 0)
Colour.register("ORCHID1", 255, 131, 250)
Colour.register("ORCHID2", 238, 122, 233)
Colour.register("ORCHID3", 205, 105, 201)
Colour.register("ORCHID4", 139, 71, 137)
Colour.register("PALEGREEN1", 154, 255, 154)
Colour.register("PALEGREEN2", 144, 238, 144)
Colour.register("PALEGREEN3", 124, 205, 124)
Colour.register("PALEGREEN4", 84, 139, 84)
Colour.register("PALETURQUOISE1", 187, 255, 255)
Colour.register("PALETURQUOISE2", 174, 238, 238)
Colour.register("PALETURQUOISE3", 150, 205, 205)
Colour.register("PALETURQUOISE4", 102, 139, 139)
Colour.register("PALEVIOLETRED1", 255, 130, 171)
Colour.register("PALEVIOLETRED2", 238, 121, 159)
Colour.register("PALEVIOLETRED3", 205, 104, 137)
Colour.register("PALEVIOLETRED4", 139, 71, 93)
Colour.register("PEACHPUFF1", 255, 218, 185)
Colour.register("PEACHPUFF2", 238, 203, 173)
Colour.register("PEACHPUFF3", 205, 175, 149)
Colour.register("PEACHPUFF4", 139, 119, 101)
Colour.register("PEACOCK", 51, 161, 201)
Colour.register("PINK1", 255, 181, 197)
Colour.register("PINK2", 238, 169, 184)
Colour.register("PINK3", 205, 145, 158)
Colour.register("PINK4", 139, 99, 108)
Colour.register("PLUM1", 255, 187, 255)
Colour.register("PLUM2", 238, 174, 238)
Colour.register("PLUM3", 205, 150, 205)
Colour.register("PLUM4", 139, 102, 139)
Colour.register("PURPLE1", 155, 48, 255)
Colour.register("PURPLE2", 145, 44, 238)
Colour.register("PURPLE3", 125, 38, 205)
Colour.register("PURPLE4", 85, 26, 139)
Colour.register("RASPBERRY", 135, 38, 87)
Colour.register("RAWSIENNA", 199, 97, 20)
Colour.register("RED1", 255, 0, 0)
Colour.register("RED2", 238, 0, 0)
Colour.register("RED3", 205, 0, 0)
Colour.register("RED4", 139, 0, 0)
Colour.register("ROSYBROWN1", 255, 193, 193)
Colour.register("ROSYBROWN2", 238, 180, 180)
Colour.register("ROSYBROWN3", 205, 155, 155)
Colour.register("ROSYBROWN4", 139, 105, 105)
Colour.register("ROYALBLUE1", 72, 118, 255)
Colour.register("ROYALBLUE2", 67, 110, 238)
Colour.register("ROYALBLUE3", 58, 95, 205)
Colour.register("ROYALBLUE4", 39, 64, 139)
Colour.register("SALMON1", 255, 140, 105)
Colour.register("SALMON2", 238, 130, 98)
Colour.register("SALMON3", 205, 112, 84)
Colour.register("SALMON4", 139, 76, 57)
Colour.register("SAPGREEN", 48, 128, 20)
Colour.register("SEAGREEN1", 84, 255, 159)
Colour.register("SEAGREEN2", 78, 238, 148)
Colour.register("SEAGREEN3", 67, 205, 128)
Colour.register("SEAGREEN4", 46, 139, 87)
Colour.register("SEASHELL1", 255, 245, 238)
Colour.register("SEASHELL2", 238, 229, 222)
Colour.register("SEASHELL3", 205, 197, 191)
Colour.register("SEASHELL4", 139, 134, 130)
Colour.register("SEPIA", 94, 38, 18)
Colour.register("SGIBEET", 142, 56, 142)
Colour.register("SGIBRIGHTGRAY", 197, 193, 170)
Colour.register("SGICHARTREUSE", 113, 198, 113)
Colour.register("SGIDARKGRAY", 85, 85, 85)
Colour.register("SGIGRAY12", 30, 30, 30)
Colour.register("SGIGRAY16", 40, 40, 40)
Colour.register("SGIGRAY32", 81, 81, 81)
Colour.register("SGIGRAY36", 91, 91, 91)
Colour.register("SGIGRAY52", 132, 132, 132)
Colour.register("SGIGRAY56", 142, 142, 142)
Colour.register("SGIGRAY72", 183, 183, 183)
Colour.register("SGIGRAY76", 193, 193, 193)
Colour.register("SGIGRAY92", 234, 234, 234)
Colour.register("SGIGRAY96", 244, 244, 244)
Colour.register("SGILIGHTBLUE", 125, 158, 192)
Colour.register("SGILIGHTGRAY", 170, 170, 170)
Colour.register("SGIOLIVEDRAB", 142, 142, 56)
Colour.register("SGISALMON", 198, 113, 113)
Colour.register("SGISLATEBLUE", 113, 113, 198)
Colour.register("SGITEAL", 56, 142, 142)
Colour.register("SIENNA1", 255, 130, 71)
Colour.register("SIENNA2", 238, 121, 66)
Colour.register("SIENNA3", 205, 104, 57)
Colour.register("SIENNA4", 139, 71, 38)
Colour.register("SKYBLUE1", 135, 206, 255)
Colour.register("SKYBLUE2", 126, 192, 238)
Colour.register("SKYBLUE3", 108, 166, 205)
Colour.register("SKYBLUE4", 74, 112, 139)
Colour.register("SLATEBLUE1", 131, 111, 255)
Colour.register("SLATEBLUE2", 122, 103, 238)
Colour.register("SLATEBLUE3", 105, 89, 205)
Colour.register("SLATEBLUE4", 71, 60, 139)
Colour.register("SLATEGRAY1", 198, 226, 255)
Colour.register("SLATEGRAY2", 185, 211, 238)
Colour.register("SLATEGRAY3", 159, 182, 205)
Colour.register("SLATEGRAY4", 108, 123, 139)
Colour.register("SNOW1", 255, 250, 250)
Colour.register("SNOW2", 238, 233, 233)
Colour.register("SNOW3", 205, 201, 201)
Colour.register("SNOW4", 139, 137, 137)
Colour.register("SPRINGGREEN1", 0, 238, 118)
Colour.register("SPRINGGREEN2", 0, 205, 102)
Colour.register("SPRINGGREEN3", 0, 139, 69)
Colour.register("STEELBLUE1", 99, 184, 255)
Colour.register("STEELBLUE2", 92, 172, 238)
Colour.register("STEELBLUE3", 79, 148, 205)
Colour.register("STEELBLUE4", 54, 100, 139)
Colour.register("TAN1", 255, 165, 79)
Colour.register("TAN2", 238, 154, 73)
Colour.register("TAN3", 205, 133, 63)
Colour.register("TAN4", 139, 90, 43)
Colour.register("THISTLE1", 255, 225, 255)
Colour.register("THISTLE2", 238, 210, 238)
Colour.register("THISTLE3", 205, 181, 205)
Colour.register("THISTLE4", 139, 123, 139)
Colour.register("TOMATO1", 255, 99, 71)
Colour.register("TOMATO2", 238, 92, 66)
Colour.register("TOMATO3", 205, 79, 57)
Colour.register("TOMATO4", 139, 54, 38)
Colour.register("TURQUOISE1", 0, 245, 255)
Colour.register("TURQUOISE2", 0, 229, 238)
Colour.register("TURQUOISE3", 0, 197, 205)
Colour.register("TURQUOISE4", 0, 134, 139)
Colour.register("TURQUOISEBLUE", 0, 199, 140)
Colour.register("VIOLETRED", 208, 32, 144)
Colour.register("VIOLETRED1", 255, 62, 150)
Colour.register("VIOLETRED2", 238, 58, 140)
Colour.register("VIOLETRED3", 205, 50, 120)
Colour.register("VIOLETRED4", 139, 34, 82)
Colour.register("WARMGREY", 128, 128, 105)
Colour.register("WHEAT1", 255, 231, 186)
Colour.register("WHEAT2", 238, 216, 174)
Colour.register("WHEAT3", 205, 186, 150)
Colour.register("WHEAT4", 139, 126, 102)
Colour.register("YELLOW1", 255, 255, 0)
Colour.register("YELLOW2", 238, 238, 0)
Colour.register("YELLOW3", 205, 205, 0)
Colour.register("YELLOW4", 139, 139, 0)

# PSCAD signal-type colours; names map to colours, but not are the colour names.
Colour.register("logical", "#ffc364c5", named=False)
Colour.register("integer", "#ff1f75fe", named=False)
Colour.register("real", "#ff17806d", named=False)
Colour.register("complex", "#ffff7538", named=False)

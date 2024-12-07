"""Use ANSI formatting to color output text by hexadecimal values, RGB values or by color specific name or decorate
it.\n The color names and values is inspired by https://www.w3schools.com/colors/colors_names.asp and
https://github.com/jonathantneal

Functions:
expand - Expands the colors list, extra colors will be available if this function will be executed.
enrich - Return colored and decorated font for rgb values or for hex.
dye - Only determine the foreground color of the font but can accept a dictionary of strings with their different colors values.
printr - Prints the decorated colorized text that have sent as argument.
printd - Prints text that have sent as an argument in multiple colors.

Examples in main
"""

from __future__ import print_function

import json
from os import getenv, system
import requests

__ALL__ = ["_check_value", 'enrich', 'printr', 'dye', 'printd', 'show']

system("color")
if getenv("CLICOLOR", "1") == "0":
    try:
        raise EnvironmentError
    except EnvironmentError:
        print('ANSI colors disabled')
else:
    _OPEN = "\x1b["
    _CLOSE = "\x1b[0m"

_COLORS = {
    'aliceblue': ['#F0F8FF', '(240,248,255)'],
    'antiquewhite': ['#FAEBD7', '(250,235,215)'],
    'aqua': ['#00FFFF', '(0,255,255)'],
    'aquamarine': ['#7FFFD4', '(127,255,212)'],
    'azure': ['#F0FFFF', '(240,255,255)'],
    'beige': ['#F5F5DC', '(245,245,220)'],
    'bisque': ['#FFE4C4', '(255,228,196)'],
    'black': ['#000000', '(0,0,0)'],
    'blanchedalmond': ['#FFEBCD', '(255,235,205)'],
    'blue': ['#0000FF', '(0,0,255)'],
    'blueviolet': ['#8A2BE2', '(138,43,226)'],
    'brown': ['#A52A2A', '(165,42,42)'],
    'burlywood': ['#DEB887', '(222,184,135)'],
    'cadetblue': ['#5F9EA0', '(95,158,160)'],
    'chartreuse': ['#7FFF00', '(127,255,0)'],
    'chocolate': ['#D2691E', '(210,105,30)'],
    'coral': ['#FF7F50', '(255,127,80)'],
    'cornflowerblue': ['#6495ED', '(100,149,237)'],
    'cornsilk': ['#FFF8DC', '(255,248,220)'],
    'crimson': ['#DC143C', '(220,20,60)'],
    'cyan': ['#00FFFF', '(0,255,255)'],
    'darkblue': ['#00008B', '(0,0,139)'],
    'darkcyan': ['#008B8B', '(0,139,139)'],
    'darkgoldenrod': ['#B8860B', '(184,134,11)'],
    'darkgray': ['#A9A9A9', '(169,169,169)'],
    'darkgrey': ['#A9A9A9', '(169,169,169)'],
    'darkgreen': ['#006400', '(0,100,0)'],
    'darkkhaki': ['#BDB76B', '(189,183,107)'],
    'darkmagenta': ['#8B008B', '(139,0,139)'],
    'darkolivegreen': ['#556B2F', '(85,107,47)'],
    'darkorange': ['#FF8C00', '(255,140,0)'],
    'darkorchid': ['#9932CC', '(153,50,204)'],
    'darkred': ['#8B0000', '(139,0,0)'],
    'darksalmon': ['#E9967A', '(233,150,122)'],
    'darkseagreen': ['#8FBC8F', '(143,188,143)'],
    'darkslateblue': ['#483D8B', '(72,61,139)'],
    'darkslategray': ['#2F4F4F', '(47,79,79)'],
    'darkslategrey': ['#2F4F4F', '(47,79,79)'],
    'darkturquoise': ['#00CED1', '(0,206,209)'],
    'darkviolet': ['#9400D3', '(148,0,211)'],
    'deeppink': ['#FF1493', '(255,20,147)'],
    'deepskyblue': ['#00BFFF', '(0,191,255)'],
    'dimgray': ['#696969', '(105,105,105)'],
    'dimgrey': ['#696969', '(105,105,105)'],
    'dodgerblue': ['#1E90FF', '(30,144,255)'],
    'firebrick': ['#B22222', '(178,34,34)'],
    'floralwhite': ['#FFFAF0', '(255,250,240)'],
    'forestgreen': ['#228B22', '(34,139,34)'],
    'fuchsia': ['#FF00FF', '(255,0,255)'],
    'gainsboro': ['#DCDCDC', '(220,220,220)'],
    'ghostwhite': ['#F8F8FF', '(248,248,255)'],
    'gold': ['#FFD700', '(255,215,0)'],
    'goldenrod': ['#DAA520', '(218,165,32)'],
    'gray': ['#808080', '(128,128,128)'],
    'grey': ['#808080', '(128,128,128)'],
    'green': ['#008000', '(0,128,0)'],
    'greenyellow': ['#ADFF2F', '(173,255,47)'],
    'honeydew': ['#F0FFF0', '(240,255,240)'],
    'hotpink': ['#FF69B4', '(255,105,180)'],
    'iceberg': ['#56A5EC', '(86, 165, 236)'],
    'indianred': ['#CD5C5C', '(205,92,92)'],
    'indigo': ['#4B0082', '(75,0,130)'],
    'ivory': ['#FFFFF0', '(255,255,240)'],
    'khaki': ['#F0E68C', '(240,230,140)'],
    'lavender': ['#E6E6FA', '(230,230,250)'],
    'lavenderblush': ['#FFF0F5', '(255,240,245)'],
    'lawngreen': ['#7CFC00', '(124,252,0)'],
    'lemonchiffon': ['#FFFACD', '(255,250,205)'],
    'lightblue': ['#ADD8E6', '(173,216,230)'],
    'lightcoral': ['#F08080', '(240,128,128)'],
    'lightcyan': ['#E0FFFF', '(224,255,255)'],
    'lightgoldenrodyellow': ['#FAFAD2', '(250,250,210)'],
    'lightgray': ['#D3D3D3', '(211,211,211)'],
    'lightgrey': ['#D3D3D3', '(211,211,211)'],
    'lightgreen': ['#90EE90', '(144,238,144)'],
    'lightpink': ['#FFB6C1', '(255,182,193)'],
    'lightsalmon': ['#FFA07A', '(255,160,122)'],
    'lightseagreen': ['#20B2AA', '(32,178,170)'],
    'lightskyblue': ['#87CEFA', '(135,206,250)'],
    'lightslategray': ['#778899', '(119,136,153)'],
    'lightslategrey': ['#778899', '(119,136,153)'],
    'lightsteelblue': ['#B0C4DE', '(176,196,222)'],
    'lightyellow': ['#FFFFE0', '(255,255,224)'],
    'lime': ['#00FF00', '(0,255,0)'],
    'limegreen': ['#32CD32', '(50,205,50)'],
    'linen': ['#FAF0E6', '(250,240,230)'],
    'magenta': ['#FF00FF', '(255,0,255)'],
    'maroon': ['#800000', '(128,0,0)'],
    'mediumaquamarine': ['#66CDAA', '(102,205,170)'],
    'mediumblue': ['#0000CD', '(0,0,205)'],
    'mediumorchid': ['#BA55D3', '(186,85,211)'],
    'mediumpurple': ['#9370DB', '(147,112,219)'],
    'mediumseagreen': ['#3CB371', '(60,179,113)'],
    'mediumslateblue': ['#7B68EE', '(123,104,238)'],
    'mediumspringgreen': ['#00FA9A', '(0,250,154)'],
    'mediumturquoise': ['#48D1CC', '(72,209,204)'],
    'mediumvioletred': ['#C71585', '(199,21,133)'],
    'midnightblue': ['#191970', '(25,25,112)'],
    'mintcream': ['#F5FFFA', '(245,255,250)'],
    'mistyrose': ['#FFE4E1', '(255,228,225)'],
    'moccasin': ['#FFE4B5', '(255,228,181)'],
    'navajowhite': ['#FFDEAD', '(255,222,173)'],
    'navy': ['#000080', '(0,0,128)'],
    'oldlace': ['#FDF5E6', '(253,245,230)'],
    'olive': ['#808000', '(128,128,0)'],
    'olivedrab': ['#6B8E23', '(107,142,35)'],
    'orange': ['#FFA500', '(255,165,0)'],
    'orangered': ['#FF4500', '(255,69,0)'],
    'orchid': ['#DA70D6', '(218,112,214)'],
    'palegoldenrod': ['#EEE8AA', '(238,232,170)'],
    'palegreen': ['#98FB98', '(152,251,152)'],
    'paleturquoise': ['#AFEEEE', '(175,238,238)'],
    'palevioletred': ['#DB7093', '(219,112,147)'],
    'papayawhip': ['#FFEFD5', '(255,239,213)'],
    'peachpuff': ['#FFDAB9', '(255,218,185)'],
    'periwinkle': ['#8E82FE', '(142, 130, 254)'],
    'peru': ['#CD853F', '(205,133,63)'],
    'pink': ['#FFC0CB', '(255,192,203)'],
    'plum': ['#DDA0DD', '(221,160,221)'],
    'powderblue': ['#B0E0E6', '(176,224,230)'],
    'purple': ['#800080', '(128,0,128)'],
    'rebeccapurple': ['#663399', '(102,51,153)'],
    'red': ['#FF0000', '(255,0,0)'],
    'rosybrown': ['#BC8F8F', '(188,143,143)'],
    'royalblue': ['#4169E1', '(65,105,225)'],
    'saddlebrown': ['#8B4513', '(139,69,19)'],
    'salmon': ['#FA8072', '(250,128,114)'],
    'sandybrown': ['#F4A460', '(244,164,96)'],
    'seagreen': ['#2E8B57', '(46,139,87)'],
    'seashell': ['#FFF5EE', '(255,245,238)'],
    'sienna': ['#A0522D', '(160,82,45)'],
    'silver': ['#C0C0C0', '(192,192,192)'],
    'skyblue': ['#87CEEB', '(135,206,235)'],
    'slateblue': ['#6A5ACD', '(106,90,205)'],
    'slategray': ['#708090', '(112,128,144)'],
    'slategrey': ['#708090', '(112,128,144)'],
    'snow': ['#FFFAFA', '(255,250,250)'],
    'springgreen': ['#00FF7F', '(0,255,127)'],
    'steelblue': ['#4682B4', '(70,130,180)'],
    'tan': ['#D2B48C', '(210,180,140)'],
    'teal': ['#008080', '(0,128,128)'],
    'thistle': ['#D8BFD8', '(216,191,216)'],
    'tomato': ['#FF6347', '(255,99,71)'],
    'turquoise': ['#40E0D0', '(64,224,208)'],
    'violet': ['#EE82EE', '(238,130,238)'],
    'wheat': ['#F5DEB3', '(245,222,179)'],
    'white': ['#FFFFFF', '(255,255,255)'],
    'whitesmoke': ['#F5F5F5', '(245,245,245)'],
    'yellow': ['#FFFF00', '(255,255,0)'],
    'yellowgreen': ['#9ACD32', '(154,205,50)'],
    None: None
}
_COLORS_NAME = [
    'AliceBlue',
    'AntiqueWhite',
    'Aqua',
    'Aquamarine',
    'Azure',
    'Beige',
    'Bisque',
    'Black',
    'BlanchedAlmond',
    'Blue',
    'BlueViolet',
    'Brown',
    'BurlyWood',
    'CadetBlue',
    'Chartreuse',
    'Chocolate',
    'Coral',
    'CornflowerBlue',
    'Cornsilk',
    'Crimson',
    'Cyan',
    'DarkBlue',
    'DarkCyan',
    'DarkGoldenRod',
    'DarkGray',
    'DarkGreen',
    'DarkKhaki',
    'DarkMagenta',
    'DarkOliveGreen',
    'DarkOrange',
    'DarkOrchid',
    'DarkRed',
    'DarkSalmon',
    'DarkSeaGreen',
    'DarkSlateBlue',
    'DarkSlateGray',
    'DarkSlateGrey',
    'DarkTurquoise',
    'DarkViolet',
    'DeepPink',
    'DeepSkyBlue',
    'DimGray',
    'DimGrey',
    'DodgerBlue',
    'FireBrick',
    'FloralWhite',
    'ForestGreen',
    'Fuchsia',
    'Gainsboro',
    'GhostWhite',
    'Gold',
    'GoldenRod',
    'Gray',
    'Grey',
    'Green',
    'GreenYellow',
    'HoneyDew',
    'HotPink',
    'Iceberg',
    'IndianRed',
    'Indigo',
    'Ivory',
    'Khaki',
    'Lavender',
    'LavenderBlush',
    'LawnGreen',
    'LemonChiffon',
    'LightBlue',
    'LightCoral',
    'LightCyan',
    'LightGoldenRodYellow',
    'LightGray',
    'LightGrey',
    'LightGreen',
    'LightPink',
    'LightSalmon',
    'LightSeaGreen',
    'LightSkyBlue',
    'LightSlateGray',
    'LightSlateGrey',
    'LightSteelBlue',
    'LightYellow',
    'Lime',
    'LimeGreen',
    'Linen',
    'Magenta',
    'Maroon',
    'MediumAquaMarine',
    'MediumBlue',
    'MediumOrchid',
    'MediumPurple',
    'MediumSeaGreen',
    'MediumSlateBlue',
    'MediumSpringGreen',
    'MediumTurquoise',
    'MediumVioletRed',
    'MidnightBlue',
    'MintCream',
    'MistyRose',
    'Moccasin',
    'NavajoWhite',
    'Navy',
    'OldLace',
    'Olive',
    'OliveDrab',
    'Orange',
    'OrangeRed',
    'Orchid',
    'PaleGoldenRod',
    'PaleGreen',
    'PaleTurquoise',
    'PaleVioletRed',
    'PapayaWhip',
    'PeachPuff',
    'Periwinkle',
    'Peru',
    'Pink',
    'Plum',
    'PowderBlue',
    'Purple',
    'RebeccaPurple',
    'Red',
    'RosyBrown',
    'RoyalBlue',
    'SaddleBrown',
    'Salmon',
    'SandyBrown',
    'SeaGreen',
    'SeaShell',
    'Sienna',
    'Silver',
    'SkyBlue',
    'SlateBlue',
    'SlateGray',
    'SlateGrey',
    'Snow',
    'SpringGreen',
    'SteelBlue',
    'Tan',
    'Teal',
    'Thistle',
    'Tomato',
    'Turquoise',
    'Violet',
    'Wheat',
    'White',
    'WhiteSmoke',
    'Yellow',
    'YellowGreen'
]
_DECOR = {
    'normal': '0',
    'bold': '1',
    'dark': '2',
    'italic': '3',
    'underline': '4',
    'blink': '5',
    'rapid': '6',
    'reverse': '7',
    'concealed': '8',
    'crossed': '9',
    'b': '1',
    'i': '3',
    'u': '4',
    None: None
}
_DECORS_NAME = [key.title() for key in _DECOR.keys() if key is not None and len(key) > 1]

_URL_COLORS = {None: None, "": None}
_URL_COLORS_NAME = []
_EXPANDED = False


def expand():
    """
    Expands the colors list, extra colors will be available if this function will be executed
    """
    global _URL_COLORS
    global _URL_COLORS_NAME
    global _EXPANDED

    from requests.exceptions import ConnectionError
    try:
        _GET_COLORS = requests.get("https://raw.githubusercontent.com/jonathantneal/color-names/master/color-names.json")
    except ConnectionError as e:
        print(e, "\n")
        _GET_COLORS = {None: None, "": None}
    else:
        [_URL_COLORS.update({color.lower().replace(" ", ""): value.upper()})
         for value, color in json.loads(_GET_COLORS.text).items()]
        [_URL_COLORS_NAME.append(color_name) for color_name in json.loads(_GET_COLORS.text).values()]
        _EXPANDED = True


def _check_value(value=None, kind=None):
    """
    Check if value is valid and returns the right string to enrich the text.\n
    :param value: Value of color (hexadecimal or RGB)
    :param kind: Kind of decoration ('fore', 'back' etc...)
    :return: encoded string suitable for ANSI formatting
    :type value: str or tuple or None
    :type kind: str or None
    :rtype: str
    """
    RGB = {'fore': '38', 'back': '48'}

    if value is not None:
        if type(value) is str and not value.isdigit():
            value = value.lower().replace(" ", "")
            if value == "":
                return None
            elif kind in RGB:
                if value not in _COLORS and value not in _URL_COLORS and value[0] != "#":
                    value = "#" + value

                if value[0] == "#" and len(value) == 7:
                    r = int("0x" + value[1:3], 16)
                    g = int("0x" + value[3:5], 16)
                    b = int("0x" + value[5:7], 16)
                    return f"{RGB[kind]};2;{r};{g};{b}"

                elif value in _COLORS or value in _URL_COLORS:
                    if value in _COLORS:
                        value = _COLORS[value][0]
                    else:
                        value = _URL_COLORS[value]
                    r = int("0x" + value[1:3], 16)
                    g = int("0x" + value[3:5], 16)
                    b = int("0x" + value[5:7], 16)
                    return f"{RGB[kind]};2;{r};{g};{b}"

                else:
                    return None

            elif kind == "decor":
                return _DECOR[value]

        elif kind in RGB and type(value) is tuple:
            r = value[0]
            g = value[1]
            b = value[2]
            return f"{RGB[kind]};2;{r};{g};{b}"

        else:
            return value

    else:
        return value


def enrich(text, fore=None, back=None, decor=None):
    """
    Return colored and decorated font for rgb values or for hex.\n
    :param text: Text to be colorized
    :param fore: Hexagonal or RGB foreground color value (#RRGGBB) or (R, G, B)
    :param back: Hexagonal or RGB background color value (#RRGGBB) or (R, G, B)
    :param decor: Font decoration (Bold, underline, etc...)
    :return: Rich text from the string sent
    :type text: str
    :type fore: str or tuple or None
    :type back: str or tuple or None
    :type decor: str or None
    :rtype: str
    """

    attributes = list(filter(lambda val: val is not None,
                             [_check_value(fore, "fore"), _check_value(back, "back"), _check_value(decor, "decor")]))

    text = f"m{text}"
    rich_text = _OPEN + ";".join(attributes) + text + _CLOSE

    return rich_text


def printr(text, fore=None, back=None, decor=None, *args, **kwargs):
    """
    Prints colorized and decorated text that have sent as an argument\n
    :param text: Text to be colorized
    :param fore: Foreground color name or hexadecimal value or RGB value
    :param back: Background color name or hexadecimal value or RGB value
    :param decor: Font decoration (Bold, underline, etc...)
    :type text: str
    :type fore: str or tuple or None
    :type back: str or tuple or None
    :type decor: str or None
    """

    print(enrich(text, fore, back, decor), *args, **kwargs)


def dye(text_color):
    """
    Only determine the foreground color of the font but can accept a dictionary of strings with their different colors values.\n
    :param text_color: dictionary of every text and it's color
    ":type text_n_color: dict
    :return: Colored text
    :rtype: str
    """
    colored_text = ''

    for text, color in text_color.items():
        colored_text += enrich(text, color)

    return colored_text


def printd(*text_and_color: str):
    """
        Prints text that have sent as an argument in multiple colors.\n
        :param text_and_color: Contains multiple strings with both text and foreground color separated with the char ";"
        e.g. printd("Red ; red", "Slate Blue ; slateBlue")
        :type text_and_color: tuple of str
    """
    delimiter = ";"
    text_color_dict = {}

    for string in text_and_color:
        if string is not None:
            if string.count(delimiter) == 0:
                text = string
                color = ""

            elif string.count(delimiter) > 1:
                string = string[::-1]
                color, text = string.split(delimiter, 1)
                text = text[::-1]
                color = color[::-1]

            else:
                text, color = string.split(delimiter)

        else:
            text = ""
            color = None

        text_color_dict.update({text: color})
    print(dye(text_color_dict))


def show(text, more=False):
    """
    Shows the colors and decorations names available and their value (hexadecimal and RGB).\n
    available options:\n
    'fore' - Foreground colors\n
    'back' - Background colors\n
    'decor' - Decorations names\n
    :param text: determines what to show (can only accept specific values)
    :type text: str
    :param more: determines if the function will show the expended list of colors
    :type more: bool
    """

    text = text.lower()
    dark = ["Black", "Blue", "DarkBlue", "Indigo", "Maroon", "MediumBlue", "MidnightBlue", "Navy", "Purple"]

    if text in ["fore", "back"]:
        print(f"The following {text}ground colors are available to use:")
        for color in range(len(_COLORS_NAME)):
            color_name = _COLORS_NAME[color]
            color_hex = _COLORS[_COLORS_NAME[color].lower()][0]
            color_rgb = _COLORS[_COLORS_NAME[color].lower()][1]
            if text == "fore":
                printr(color_name + ": " + color_hex + ", " + color_rgb, color_hex)
            elif color_name not in dark:
                printr(color_name + ": " + color_hex + ", " + color_rgb, "Black", color_hex)
            else:
                printr(color_name + ": " + color_hex + ", " + color_rgb, "White", color_hex)

        if _EXPANDED and more:
            print(f"The following {text}ground colors are available to use from the expended list:")
            for color in range(len(_URL_COLORS_NAME)):
                color_name = _URL_COLORS_NAME[color]
                color_hex = _URL_COLORS[_URL_COLORS_NAME[color].lower().replace(" ", "")]
                if text == "fore":
                    printr(color_name + ": " + color_hex, color_hex)
                else:
                    printr(color_name + ": " + color_hex, back=color_hex)

    elif text == "decor":
        print("The following decorations are available to use:")
        print(enrich("Caution:", "Orange"), "Some features (such as Dark and Italic) may not work")
        for name in range(len(_DECORS_NAME)):
            printr(_DECORS_NAME[name], decor=_DECORS_NAME[name].lower())

    else:
        print("Only 'fore', 'back', 'decor' or 'more' are an available argument")


if __name__ == '__main__':
    # RGB features
    # Foreground colors
    print(enrich("Text"))
    print(enrich("Gold", "#FFD700"))
    print(enrich("SeaGreen", (45, 140, 85)), "\n")

    # Background colors
    print(enrich("Bacground color", back=(150, 130, 250)))
    print(enrich("Gold on SlateBlue", "#FFD700", (150, 130, 250)))
    print(enrich("SlateBlue on Gold", (150, 130, 250), "#FFD700"), "\n")

    # Decorations
    print(enrich("Simple underlined text", decor="underline"))
    print(enrich("Bold DarkOliveGreen", "556B2F", decor="Bold"))
    print(enrich("DarkSeaGreen on MidnightBlue", (145, 190, 145), "191970", decor="crossed"))
    print(enrich("MidnightBlue on DarkSeaGreen (Reversed)", "8FBC8F", (25, 25, 112), decor="reverse"))
    print(enrich("Italic Crimson Background", back="DC143C", decor="Italic"), "\n")

    # Color by name
    print(enrich("BurlyWood", "Burly wood"))
    print(enrich("PaleVioletRed background", back="Pale vIoLeTRed"))
    print(enrich("OrangeRed on PaleGreen", "OrangeRed", "pale green"))
    print(enrich("DodgerBlue Green on Yellow", "DodgerBlue", "Yellow", "underline"))
    print(enrich("Reverse", "DodgerBlue", "Yellow", "Reverse"), "\n")

    # Multicolor phrase
    print(dye({"Periwinkle ": "periwinkle ", "Iceberg ": "Ice berg", "and ": "", "Forest green\n": "Forest green"}))
    printd("Red ; red", "Slate Blue ; slateBlue", "default color ", "and; Orange Red\n; OrangeRed")

    # Print colorized text
    # By hexadecimal and RGB values
    printr("Underlined Slateblue on Aqua", "#6A5ACD", (120, 250, 150), "u")
    printr("Bold Turquoise on MediumSlateBlue", (64, 224, 208), "#7B68EE", "B", "\n")
    # By name
    printr("Italic GoldenRod", "Golden Rod", decor="I")
    printr("Chocolate background", back="Chocolate", end="\n\n")

    # all colors names available
    expand()
    show("fore", True)
    show("Back", True)
    show("decor")

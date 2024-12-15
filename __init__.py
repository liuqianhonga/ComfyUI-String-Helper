from .nodes.string_formatter import StringFormatter
from .nodes.string_list import StringList, StringListFromCSV, StringListToCSV
from .nodes.show_translate_string import ShowTranslateString
from .nodes.string_matcher import StringMatcher

NODE_CLASS_MAPPINGS = {
    "StringFormatter": StringFormatter,
    "StringList": StringList,
    "StringListFromCSV": StringListFromCSV,
    "StringListToCSV": StringListToCSV,
    "ShowTranslateString": ShowTranslateString,
    "StringMatcher": StringMatcher
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "StringFormatter": "String Formatter",
    "StringList": "String List",
    "StringListFromCSV": "String List From CSV",
    "StringListToCSV": "String List To CSV",
    "ShowTranslateString": "Show Translate String",
    "StringMatcher": "String Matcher"
}

WEB_DIRECTORY = "./web"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']
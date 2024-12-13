from .nodes.string_formatter import StringFormatter
from .nodes.string_list import StringList, StringListFromCSV
from .nodes.show_translate_string import ShowTranslateString

NODE_CLASS_MAPPINGS = {
    "StringFormatter": StringFormatter,
    "StringList": StringList,
    "StringListFromCSV": StringListFromCSV,
    "ShowTranslateString": ShowTranslateString
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "StringFormatter": "String Formatter",
    "StringList": "String List",
    "StringListFromCSV": "String List From CSV",
    "ShowTranslateString": "Show Translate String"
}

WEB_DIRECTORY = "./web"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']
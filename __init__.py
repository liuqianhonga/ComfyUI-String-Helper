from .nodes.string_formatter import StringFormatter
from .nodes.string_list import StringList
from .nodes.show_translate_string import ShowTranslateString

NODE_CLASS_MAPPINGS = {
    "StringFormatter": StringFormatter,
    "StringList": StringList,
    "ShowTranslateString": ShowTranslateString
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "StringFormatter": "String Formatter",
    "StringList": "String List",
    "ShowTranslateString": "Show Translate String"
}

WEB_DIRECTORY = "./web"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']
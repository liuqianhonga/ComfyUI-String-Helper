from .nodes.string_formatter import StringFormatter
from .nodes.string_list import StringList

NODE_CLASS_MAPPINGS = {
    "StringFormatter": StringFormatter,
    "StringList": StringList
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "StringFormatter": "String Formatter",
    "StringList": "String List"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
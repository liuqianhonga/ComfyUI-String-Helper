from .nodes.string_formatter import StringFormatter

NODE_CLASS_MAPPINGS = {
    "StringFormatter": StringFormatter
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "StringFormatter": "String Formatter"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS'] 
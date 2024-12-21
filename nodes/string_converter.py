import json
from .lib import ANY

class StringConverter:
    """Converts a string to a specified type (INT, FLOAT, BOOL, LIST, DICT)"""
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_string": ("STRING", {"default": "", "multiline": False}),
                "target_type": (["INT", "FLOAT", "BOOL", "LIST", "DICT"], ),
            },
        }

    RETURN_TYPES = (ANY,)
    RETURN_NAMES = ("value",)
    FUNCTION = "convert"
    CATEGORY = "String Helper"

    def convert(self, input_string: str, target_type: str):
        try:
            if target_type == "INT":
                result = int(float(input_string))
                return (result,)
            elif target_type == "FLOAT":
                result = float(input_string)
                return (result,)
            elif target_type == "BOOL":
                # Convert string to boolean
                result = input_string.lower() in ('true', '1', 'yes', 'y', 'on')
                return (result,)
            elif target_type == "LIST":
                # Convert comma-separated string to list
                if not input_string.strip():
                    return ([],)
                result = [item.strip() for item in input_string.split(",")]
                return (result,)
            elif target_type == "DICT":
                # Convert JSON string to dictionary
                result = json.loads(input_string)
                return (result,)
            else:
                raise ValueError(f"Unsupported type: {target_type}")
        except Exception as e:
            raise Exception(f"[String Type Converter] Error converting '{input_string}' to {target_type}: {str(e)}")
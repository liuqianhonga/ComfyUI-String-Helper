from .lib import ANY
import json

class StringMatcher:
    """
    A node that matches a string against a list of conditions and returns the matched value.
    Each condition in the list should be in the format "condition:value".
    """
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "condition_list": ("STRING", {
                    "multiline": True,
                    "placeholder": "Input conditions, one per line, e.g.:\nred:red color\nblue:blue color"
                }),
                "target_type": (["STRING", "INT", "FLOAT", "BOOL", "LIST", "DICT"], {"default": "STRING"}),
            },
            "optional": {
                "match_value": (ANY, {"default": None}),
                "default_value": ("STRING", {"default": ""}),
            }
        }
    
    RETURN_TYPES = (ANY,)
    RETURN_NAMES = ("value",)
    FUNCTION = "match_string"
    CATEGORY = "String Helper"
    
    def match_string(self, condition_list, target_type, match_value=None, default_value=""):
        if match_value is None:
            value = default_value
        else:
            match_str = str(match_value)
            conditions = [line.strip() for line in condition_list.split('\n') if line.strip()]
            
            value = default_value
            for condition in conditions:
                if ':' not in condition:
                    continue
                    
                cond, val = condition.split(':', 1)
                cond = cond.strip()
                val = val.strip()
                
                if cond == match_str:
                    value = val
                    break

        try:
            if target_type == "STRING" or not value.strip():
                return (value,)
            elif target_type == "INT":
                value = int(float(value))
                return (value,)
            elif target_type == "FLOAT":
                value = float(value)
                return (value,)
            elif target_type == "BOOL":
                value = value.lower() in ('true', '1', 'yes', 'y', 'on')
                return (value,)
            elif target_type == "LIST":
                if not value.strip():
                    return ([],)
                value = [item.strip() for item in value.split(",")]
                return (value,)
            elif target_type == "DICT":
                value = json.loads(value)
                return (value,)
            else:
                raise ValueError(f"Unsupported type: {target_type}")
        except Exception as e:
            raise Exception(f"[String Matcher] Error converting '{value}' to {target_type}: {str(e)}")

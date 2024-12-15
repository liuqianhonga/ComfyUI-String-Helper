from .lib import ANY

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
                "match_value": (ANY, {"default": None}),
                "default_value": ("STRING", {"default": ""}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "match_string"
    CATEGORY = "String Helper"
    
    def match_string(self, condition_list, match_value, default_value):
        match_str = str(match_value)
        
        conditions = [line.strip() for line in condition_list.split('\n') if line.strip()]
        
        for condition in conditions:
            if ':' not in condition:
                continue
                
            cond, value = condition.split(':', 1)
            cond = cond.strip()
            value = value.strip()
            
            if cond == match_str:
                return (value,)
        
        return (default_value,)

from .lib import ANY

class StringFormatter:
    """
    A node that formats a string using Python's f-string syntax.
    Supports up to 10 input arguments.
    """
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "template": ("STRING", {
                    "default": "", 
                    "multiline": True,
                    "placeholder": "Input f-string template, e.g.: 'Hello {arg1}, today is {arg2}'"
                }),
            },
            "optional": {
                **{f"arg{i}": (ANY, {"default": None}) for i in range(1, 11)}
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "format_string"
    CATEGORY = "String Helper"
    RETURN_NAMES = ("formatted_string",)
    
    @classmethod
    def format_string(cls, template, arg1=None, arg2=None, arg3=None, arg4=None, 
                     arg5=None, arg6=None, arg7=None, arg8=None, arg9=None, arg10=None):
        try:
            # Create a dictionary of all arguments
            args_dict = {
                name: value 
                for name, value in locals().items() 
                if name.startswith('arg')
            }
            
            # Format string using f-string style with the arguments dictionary
            result = eval(f"f'''{template}'''", args_dict)
            return {"ui": {"formatted_string": (result,)}, "result": (result,)}
        except Exception as e:
            error_msg = f"Format Error: {str(e)}"
            return {"ui": {"formatted_string": (error_msg,)}, "result": (error_msg,)}
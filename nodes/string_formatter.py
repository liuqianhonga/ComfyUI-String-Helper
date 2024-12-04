class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False

ANY = AnyType("*")

class StringFormatter:
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
                "arg1": (ANY, {"default": None}),
                "arg2": (ANY, {"default": None}),
                "arg3": (ANY, {"default": None}),
                "arg4": (ANY, {"default": None}),
                "arg5": (ANY, {"default": None}),
                "arg6": (ANY, {"default": None}),
                "arg7": (ANY, {"default": None}),
                "arg8": (ANY, {"default": None}),
                "arg9": (ANY, {"default": None}),
                "arg10": (ANY, {"default": None}),
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
            # Create a dictionary of non-None arguments
            args_dict = {
                name: value 
                for name, value in locals().items() 
                if name.startswith('arg') and value is not None
            }
            
            # Format string using f-string style with the arguments dictionary
            result = eval(f"f'''{template}'''", args_dict)
            return (result,)
        except Exception as e:
            return (f"Format Error: {str(e)}",) 
import datetime

class TimeFormatter:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "format_string": ("STRING", {
                    "default": "%Y-%m-%d %H:%M:%S",
                    "multiline": False
                }),
            },
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "format_time"
    CATEGORY = "String Helper"
    IS_CHANGED = True

    def format_time(self, format_string):
        try:
            current_time = datetime.datetime.now()
            formatted_time = current_time.strftime(format_string)
            return (formatted_time,)
        except Exception as e:
            return (str(e),)

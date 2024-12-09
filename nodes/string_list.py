import random
import translators.server as tss

class StringList:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "random_select_count": ("INT", {
                    "default": -1,
                    "min": -1,
                    "max": 10,
                    "step": 1
                }),
                "translate_output": ("BOOLEAN", {
                    "default": False,
                }),
                "string1": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "Input string 1"
                }),
                "string2": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "Input string 2"
                }),
                "string3": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "Input string 3"
                }),
                "string4": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "Input string 4"
                }),
                "string5": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "Input string 5"
                }),
                "string6": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "Input string 6"
                }),
                "string7": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "Input string 7"
                }),
                "string8": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "Input string 8"
                }),
                "string9": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "Input string 9"
                }),
                "string10": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "Input string 10"
                }),
            },
            "optional": {
                "string_list": ("LIST",)
            }
        }
    
    RETURN_TYPES = ("LIST", "STRING",)
    RETURN_NAMES = ("string_list", "strings",)
    FUNCTION = "process"
    CATEGORY = "String Helper"

    def translate_strings(self, strings):
        """Translate a list of strings to English using Bing translator with auto language detection"""
        try:
            return [tss.bing(text, from_language='auto', to_language='en') for text in strings]
        except Exception as e:
            print(f"Translation error: {str(e)}")
            return strings

    def process(self, random_select_count, translate_output, string1, string2, string3, string4, string5, string6, string7, string8, string9, string10, string_list=None):
        # Create a list of non-empty strings from inputs
        input_strings = [text for text in [string1, string2, string3, string4, string5, string6, string7, string8, string9, string10] if text.strip()]
        
        # Process input strings based on random_select_count
        if not input_strings:
            selected_input_strings = []
        elif random_select_count == -1:
            # Use all input strings
            selected_input_strings = input_strings
        elif random_select_count == 0:
            # Select none
            selected_input_strings = []
        else:
            # Randomly select specified number of strings
            count = min(random_select_count, len(input_strings))
            selected_input_strings = random.sample(input_strings, count)
        
        # Combine with optional string_list if provided
        if string_list is not None:
            string_list = [str(item).strip() for item in string_list if str(item).strip()]
            final_strings = selected_input_strings + string_list
        else:
            final_strings = selected_input_strings

        # Translate strings if enabled
        if translate_output and final_strings:
            final_strings = self.translate_strings(final_strings)

        # Return the same list for both outputs
        return (final_strings, final_strings)

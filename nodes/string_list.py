import random
from ..translation_utils import TranslationUtils

class BaseStringList:
    RETURN_TYPES = ("LIST", "STRING",)
    RETURN_NAMES = ("string_list", "strings",)
    OUTPUT_IS_LIST = (False, True)
    FUNCTION = "process"
    CATEGORY = "String Helper"

    def translate_strings(self, strings):
        """Translate a list of strings to English using Bing translator with auto language detection"""
        try:
            translated_strings = TranslationUtils.translate_with_length_check(strings, 'en')
            return translated_strings
        except Exception as e:
            print(f"Translation error: {str(e)}")
            return strings

    def get_selected_strings(self, all_strings, numbers_str):
        """Get strings by their numbers (1-based)"""
        try:
            # Convert numbers string to list of integers (1-based to 0-based)
            numbers = [int(i.strip()) - 1 for i in numbers_str.split(',') if i.strip()]
            # Filter valid indices and get corresponding strings
            return [all_strings[i] for i in numbers if 0 <= i < len(all_strings)]
        except ValueError:
            print("Invalid number format. Please use comma-separated numbers (e.g., '1,3,5')")
            return []

    def process_string_selection(self, input_strings, random_select_count, selected_numbers, translate_output, string_list=None):
        """Process string selection with common logic"""
        # Early return if no input strings
        if not input_strings:
            return ([], [])

        # Process string selection
        if selected_numbers.strip():
            # Use selected numbers if provided
            selected_input_strings = self.get_selected_strings(input_strings, selected_numbers)
        else:
            # Otherwise use random selection
            if random_select_count == -1:
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


class StringList(BaseStringList):
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
                "selected_numbers": ("STRING", {
                    "default": "",
                    "placeholder": "e.g. 1,3,5 (leave empty to use random_select_count)"
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

    def process(self, random_select_count, selected_numbers, translate_output, string1, string2, string3, string4, string5, string6, string7, string8, string9, string10, string_list=None):
        # Create a list of non-empty strings from inputs
        input_strings = [text for text in [string1, string2, string3, string4, string5, string6, string7, string8, string9, string10] if text.strip()]
        return self.process_string_selection(input_strings, random_select_count, selected_numbers, translate_output, string_list)


class StringListFromCSV(BaseStringList):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "csv_file": ("STRING", {
                    "default": "",
                    "placeholder": "Path to CSV file"
                }),
                "random_select_count": ("INT", {
                    "default": -1,
                    "min": -1,
                    "max": 10,
                    "step": 1
                }),
                "selected_numbers": ("STRING", {
                    "default": "",
                    "placeholder": "e.g. 1,3,5 (leave empty to use random_select_count)"
                }),
                "translate_output": ("BOOLEAN", {
                    "default": False,
                }),
            },
            "optional": {
                "string_list": ("LIST",)
            }
        }

    def read_csv_file(self, csv_file):
        """Read strings from CSV file"""
        encodings = ['utf-8', 'gbk', 'gb2312', 'gb18030', 'big5']
        
        for encoding in encodings:
            try:
                import csv
                with open(csv_file, 'r', encoding=encoding) as f:
                    reader = csv.reader(f)
                    # Read all non-empty strings from the first column
                    strings = [row[0].strip() for row in reader if row and row[0].strip()]
                print(f"Successfully read CSV file using {encoding} encoding")
                return strings
            except UnicodeDecodeError:
                continue
            except Exception as e:
                print(f"Error reading CSV file: {str(e)}")
                return []
        
        print("Failed to read CSV file with any of the supported encodings")
        return []

    def process(self, csv_file, random_select_count, selected_numbers, translate_output, string_list=None):
        # Read strings from CSV file
        input_strings = self.read_csv_file(csv_file)
        return self.process_string_selection(input_strings, random_select_count, selected_numbers, translate_output, string_list)

import random
import os
import csv
import chardet
from ..translation_utils import TranslationUtils

class BaseStringList:
    """Base class for string list operations"""
    
    RETURN_TYPES = ("LIST", "STRING",)
    RETURN_NAMES = ("string_list", "strings",)
    FUNCTION = "process"
    CATEGORY = "String Helper"

    @staticmethod
    def get_encoding(csv_path):
        with open(csv_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            return result['encoding'] if result else None

    @staticmethod
    def read_csv_with_encoding(csv_path):
        """Read CSV file and detect encoding"""
        encoding = BaseStringList.get_encoding(csv_path)
        if encoding is None:
            print("Unable to detect encoding for CSV file")
            return None, None
        print(f"Detected encoding for CSV file: {encoding}")

        try:
            with open(csv_path, 'r', encoding=encoding, errors='replace') as f:
                reader = csv.DictReader(f)
                if not reader.fieldnames or 'string' not in reader.fieldnames or 'translate_string' not in reader.fieldnames:
                    print(f"CSV file must have 'string' and 'translate_string' columns")
                    return None, None
                rows = list(reader)
            print(f"Successfully read CSV file using {encoding} encoding")
            return rows, encoding
        except Exception as e:
            print(f"Failed to read with {encoding} encoding: {str(e)}")
        return None, None

    @staticmethod
    def get_absolute_path(file_path):
        """Convert relative path to absolute path based on project root"""
        if os.path.isabs(file_path):
            return file_path
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(current_dir, file_path)

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

    OUTPUT_IS_LIST = (False, True)

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
                    "default": "template/string_list.csv",
                    "placeholder": "Path to CSV file (template: string,translate_string)"
                }),
                "use_translated": ("BOOLEAN", {
                    "default": False,
                }),
                "random_select_count": ("INT", {
                    "default": -1,
                    "min": -1,
                    "max": 999999,
                    "step": 1,
                    "display": "number"
                }),
                "selected_numbers": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "Comma-separated numbers (e.g., 1,3,5)"
                }),
                "translate_output": ("BOOLEAN", {
                    "default": False,
                }),
            },
            "optional": {
                "string_list": ("LIST",),
            }
        }
    
    RETURN_TYPES = ("LIST", "STRING",)
    RETURN_NAMES = ("string_list", "strings",)
    OUTPUT_IS_LIST = (False, True)
    FUNCTION = "read_strings_from_csv"
    CATEGORY = "String Helper"

    def read_csv_file(self, csv_file, use_translated=False):
        """Read strings from CSV file with template format"""
        csv_path = self.get_absolute_path(csv_file)
        
        rows, _ = self.read_csv_with_encoding(csv_path)
        if rows is None:
            return []
            
        # Read strings based on the use_translated flag
        column = 'translate_string' if use_translated else 'string'
        return [row[column].strip() for row in rows if row and row[column].strip()]

    def read_strings_from_csv(self, csv_file, use_translated, random_select_count, selected_numbers, translate_output, string_list=None):
        # Read strings from CSV file
        input_strings = self.read_csv_file(csv_file, use_translated)
        return self.process_string_selection(input_strings, random_select_count, selected_numbers, translate_output, string_list)


class StringListToCSV(BaseStringList):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "csv_file": ("STRING", {
                    "default": "output/string_list_output.csv",
                    "placeholder": "Path to save CSV file"
                }),
                "translate": ("BOOLEAN", {
                    "default": False,
                }),
                "append_mode": ("BOOLEAN", {
                    "default": True,
                    "label": "Append to file"
                }),
            },
            "optional": {
                "string": ("STRING", {"forceInput": True}),
                "string_list": ("LIST", {"forceInput": True}),
            }
        }
    
    RETURN_TYPES = ("LIST", "LIST",)
    RETURN_NAMES = ("processed_strings", "skipped_strings",)
    OUTPUT_NODE = True
    FUNCTION = "write_to_csv"
    CATEGORY = "String Helper"

    def write_to_csv(self, csv_file, translate, append_mode, string=None, string_list=None):
        """Write string list to CSV file with optional translation"""
        # Initialize processed_strings and skipped_strings
        processed_strings = []
        skipped_strings = []

        # If neither string nor string_list is provided, return empty lists
        if string is None and string_list is None:
            return processed_strings, skipped_strings
            
        # Merge string_list and string if both are provided
        if string_list and string:
            string_list = string_list + [string]
        elif string and not string_list:
            string_list = [string]
        elif string_list is None:
            string_list = []

        if len(string_list) == 0 or not string_list:
            return processed_strings, skipped_strings

        try:
            csv_path = self.get_absolute_path(csv_file)

            # Ensure the output directory exists
            os.makedirs(os.path.dirname(csv_path), exist_ok=True)

            # Read existing data and check for duplicates
            existing_strings = set()
            current_encoding = 'utf-8'
            if os.path.exists(csv_path):
                rows, encoding = self.read_csv_with_encoding(csv_path)
                if rows is not None:
                    existing_strings = {row['string'] for row in rows}
                    current_encoding = encoding

            # Determine write mode based on append_mode and file existence
            if not os.path.exists(csv_path):
                # If file doesn't exist, always use write mode
                mode = 'w'
            else:
                # If file exists and append mode is True, use append mode
                mode = 'a' if append_mode else 'w'

            with open(csv_path, mode, encoding=current_encoding, newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['string', 'translate_string'])
                
                # Write header if it's a new file or overwriting
                if mode == 'w':
                    writer.writeheader()
                    existing_strings.clear()  # Clear existing strings if overwriting

                # Write data
                for i, string in enumerate(string_list):
                    # Skip if string already exists in append mode
                    if mode == 'a' and string in existing_strings:
                        skipped_strings.append(string)
                        continue

                    # Translate string only when writing
                    translate_string = TranslationUtils.translate_with_length_check([string], 'zh')[0] if translate else ''

                    row = {
                        'string': string,
                        'translate_string': translate_string
                    }
                    writer.writerow(row)
                    processed_strings.append(string)

            print(f"Successfully processed {len(processed_strings)} strings ({len(skipped_strings)} skipped) to {csv_path} using {current_encoding} encoding")
            return processed_strings, skipped_strings

        except Exception as e:
            print(f"Error writing to CSV file: {str(e)}")
            return [], string_list

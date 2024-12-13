import random
import os
import csv
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
                    "default": "template/string_list.csv",
                    "placeholder": "Path to CSV file (template: string,translate_string)"
                }),
                "use_translated": ("BOOLEAN", {
                    "default": False,
                    "label": "Use Translated String"
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

    def read_csv_file(self, csv_file, use_translated=False):
        """Read strings from CSV file with template format"""
        encodings = ['utf-8', 'gbk', 'gb2312', 'gb18030', 'big5']
        
        # Handle file path
        if os.path.isabs(csv_file):
            # If it's an absolute path, use it directly
            csv_path = csv_file
        else:
            # If it's a relative path, search from project root directory
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            csv_path = os.path.join(current_dir, csv_file)
        
        for encoding in encodings:
            try:
                with open(csv_path, 'r', encoding=encoding) as f:
                    reader = csv.DictReader(f)
                    if not reader.fieldnames or 'string' not in reader.fieldnames or 'translate_string' not in reader.fieldnames:
                        print(f"CSV file must have 'string' and 'translate_string' columns")
                        return []
                    
                    # Read strings based on the use_translated flag
                    column = 'translate_string' if use_translated else 'string'
                    strings = [row[column].strip() for row in reader if row and row[column].strip()]
                
                print(f"Successfully read CSV file using {encoding} encoding")
                return strings
            except UnicodeDecodeError:
                continue
            except Exception as e:
                print(f"Error reading CSV file: {str(e)}")
                return []
        
        print("Failed to read CSV file with any of the supported encodings")
        return []

    def process(self, csv_file, use_translated, random_select_count, selected_numbers, translate_output, string_list=None):
        # Read strings from CSV file
        input_strings = self.read_csv_file(csv_file, use_translated)
        return self.process_string_selection(input_strings, random_select_count, selected_numbers, translate_output, string_list)


class StringListToCSV:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string_list": ("LIST",),
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
            }
        }
    
    RETURN_TYPES = ("LIST", "LIST",)
    RETURN_NAMES = ("processed_strings", "skipped_strings",)
    FUNCTION = "write_to_csv"
    CATEGORY = "String Helper"
    OUTPUT_NODE = True

    def write_to_csv(self, string_list, csv_file, translate, append_mode):
        """Write string list to CSV file with optional translation"""
        processed_strings = []
        skipped_strings = []
        
        try:
            # Handle file path
            if os.path.isabs(csv_file):
                # If it's an absolute path, use it directly
                csv_path = csv_file
            else:
                # If it's a relative path, search from project root directory
                current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                csv_path = os.path.join(current_dir, csv_file)

            # Ensure the output directory exists
            os.makedirs(os.path.dirname(csv_path), exist_ok=True)

            # Translate strings if needed
            translated_strings = []
            if translate:
                translated_strings = TranslationUtils.translate_with_length_check(string_list, 'zh')

            # Read existing data and check for duplicates
            existing_strings = set()
            if os.path.exists(csv_path):
                try:
                    with open(csv_path, 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        if not reader.fieldnames or 'string' not in reader.fieldnames or 'translate_string' not in reader.fieldnames:
                            print(f"Target CSV file must have 'string' and 'translate_string' columns")
                            return [], string_list
                        for row in reader:
                            existing_strings.add(row['string'])
                except Exception as e:
                    print(f"Error reading existing CSV file: {str(e)}")
                    return [], string_list

            # Determine write mode based on append_mode and file existence
            if not os.path.exists(csv_path):
                # If file doesn't exist, always use write mode
                mode = 'w'
            else:
                # If file exists and append mode is True, use append mode
                mode = 'a' if append_mode else 'w'

            with open(csv_path, mode, encoding='utf-8', newline='') as f:
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

                    row = {
                        'string': string,
                        'translate_string': translated_strings[i] if translate else ''
                    }
                    writer.writerow(row)
                    processed_strings.append(string)

            print(f"Successfully processed {len(processed_strings)} strings ({len(skipped_strings)} skipped) to {csv_path}")
            return processed_strings, skipped_strings

        except Exception as e:
            print(f"Error writing to CSV file: {str(e)}")
            return [], string_list

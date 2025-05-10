import random
import os
import csv
import chardet
from ..translation_utils import translate_texts

class BaseStringList:
    """Base class for string list operations"""

    def __init__(self):
        self.current_index = 0

    @staticmethod
    def get_encoding(csv_path):
        """Read CSV file and detect encoding"""
        try:
            with open(csv_path, 'rb') as f:
                raw_data = f.read()
                result = chardet.detect(raw_data)
                return result['encoding']
        except Exception as e:
            print(f"Error detecting encoding: {str(e)}")
            return 'utf-8'

    def read_csv_with_encoding(self, csv_path):
        """Read CSV file and detect encoding"""
        try:
            encoding = self.get_encoding(csv_path)
            with open(csv_path, 'r', encoding=encoding) as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                return rows, encoding
        except Exception as e:
            print(f"Error reading CSV file: {str(e)}")
            return None, 'utf-8'

    def get_absolute_path(self, file_path):
        """Convert relative path to absolute path based on project root"""
        if os.path.isabs(file_path):
            return file_path
        
        # Get the project root directory (parent of custom_nodes)
        current_dir = os.path.dirname(os.path.abspath(__file__))  # nodes directory
        project_root = os.path.abspath(os.path.join(current_dir, '..', '..', '..', '..'))
        
        # Combine with the relative path
        return os.path.join(project_root, file_path)

    def save_to_csv(self, csv_file, rows_to_write, append_mode=True, check_duplicates=True):
        """Common method to save data to CSV file
        
        Args:
            csv_file: Path to the CSV file
            rows_to_write: List of dictionaries with keys 'string', 'zh', and 'tags'
            append_mode: Whether to append to existing file
            check_duplicates: Whether to check and skip duplicate strings
            
        Returns:
            tuple: (processed_rows, skipped_rows)
        """
        try:
            csv_path = self.get_absolute_path(csv_file)
            processed_rows = []
            skipped_rows = []

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

            # Determine write mode
            if not os.path.exists(csv_path):
                mode = 'w'
            else:
                mode = 'a' if append_mode else 'w'

            with open(csv_path, mode, encoding=current_encoding, newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['string', 'zh', 'tags'])
                
                # Write header if it's a new file or overwriting
                if mode == 'w':
                    writer.writeheader()
                    existing_strings.clear()

                # Write data
                for row in rows_to_write:
                    # Skip if string already exists in append mode
                    if check_duplicates and mode == 'a' and row['string'] in existing_strings:
                        skipped_rows.append(row)
                        continue

                    writer.writerow(row)
                    processed_rows.append(row)

            return processed_rows, skipped_rows

        except Exception as e:
            print(f"Error writing to CSV: {e}")
            return [], rows_to_write

    def translate_strings(self, strings):
        """Translate a list of strings to English using Bing translator with auto language detection"""
        try:
            translated_strings = translate_texts(strings, 'en')
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

    def process_string_selection(self, input_strings, p3_select_random_count, p1_select_by_numbers, translate_output, p2_select_sequential=False, string_list=None):
        """Process string selection with common logic
        
        Args:
            input_strings: List of input strings to select from
            p1_select_by_numbers: Priority 1 - Select strings by their numbers (comma-separated)
            p2_select_sequential: Priority 2 - Select strings sequentially
            p3_select_random_count: Priority 3 - Number of strings to select randomly
            translate_output: Whether to translate the selected strings
            string_list: Optional additional strings to append
        """
        # Early return if no input strings
        if not input_strings:
            return ([], [])

        # Process string selection
        if p1_select_by_numbers.strip():
            # Use selected numbers if provided (highest priority)
            selected_input_strings = self.get_selected_strings(input_strings, p1_select_by_numbers)
        elif p2_select_sequential:
            # Use sequential selection if enabled (second priority)
            if not input_strings:
                selected_input_strings = []
            else:
                selected_input_strings = [input_strings[self.current_index]]
                # Update index for next selection
                self.current_index = (self.current_index + 1) % len(input_strings)
        else:
            # Otherwise use random selection (lowest priority)
            if p3_select_random_count == -1:
                # Use all input strings
                selected_input_strings = input_strings
            elif p3_select_random_count == 0:
                # Select none
                selected_input_strings = []
            else:
                # Randomly select specified number of strings
                count = min(p3_select_random_count, len(input_strings))
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

class StringTranslate(BaseStringList):
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "translate_output": ("BOOLEAN", {"default": False}),
                "string": ("STRING", {"multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)
    FUNCTION = "process_string"
    CATEGORY = "String Helper"

    def process_string(self, string, translate_output):
        if translate_output:
            final_strings = self.translate_strings(string)
            return (final_strings,)
        return (string,)

class StringList(BaseStringList):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "p1_select_by_numbers": ("STRING", {
                    "default": "",
                    "placeholder": "Priority 1: Comma-separated numbers (e.g. 1,3,5)"
                }),
                "p2_select_sequential": ("BOOLEAN", {
                    "default": False,
                }),
                "p3_select_random_count": ("INT", {
                    "default": -1,
                    "min": -1,
                    "max": 10,
                    "step": 1,
                    "display": "number"
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
    OUTPUT_IS_LIST = (False, True)
    FUNCTION = "process"
    CATEGORY = "String Helper"
    IS_CHANGED = True

    def process(self, p1_select_by_numbers, p2_select_sequential, p3_select_random_count, translate_output, string1, string2, string3, string4, string5, string6, string7, string8, string9, string10, string_list=None):
        # Create a list of all strings from inputs, including empty ones
        input_strings = [string1, string2, string3, string4, string5, string6, string7, string8, string9, string10]
        return self.process_string_selection(input_strings, p3_select_random_count, p1_select_by_numbers, translate_output, p2_select_sequential, string_list)


class StringListFromCSV(BaseStringList):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "csv_file": ("STRING", {
                    "default": "template/string_list.csv",
                    "placeholder": "Path to CSV file (template: string,zh)"
                }),
                "use_translated": ("BOOLEAN", {
                    "default": False,
                }),
                "filter_tags": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "Filter by tags (comma-separated)"
                }),
                "p1_select_by_numbers": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "Priority 1: Comma-separated numbers (e.g. 1,3,5)"
                }),
                "p2_select_sequential": ("BOOLEAN", {
                    "default": False,
                }),
                "p3_select_random_count": ("INT", {
                    "default": -1,
                    "min": -1,
                    "max": 999999,
                    "step": 1,
                    "display": "number"
                }),
                "translate_output": ("BOOLEAN", {
                    "default": False,
                }),
                "reuse_last_result": ("BOOLEAN", {
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
    IS_CHANGED = True

    def __init__(self):
        super().__init__()
        self.last_result = None

    def read_csv_file(self, csv_file, filter_tags="", use_translated=False):
        """Read strings from CSV file with template format"""
        csv_path = self.get_absolute_path(csv_file)
        
        rows, _ = self.read_csv_with_encoding(csv_path)
        if rows is None:
            return []
            
        # Parse filter tags
        filter_tag_list = [tag.strip() for tag in filter_tags.split(',') if tag.strip()]
        
        # Read strings based on the use_translated flag and filter by tags
        column = 'zh' if use_translated else 'string'
        filtered_rows = []
        for row in rows:
            if not row or not row.get(column, '').strip():
                continue
                
            # If filter tags are specified, check if any tag matches
            if filter_tag_list:
                row_tags = row.get('tags', '')
                if not any(tag in row_tags for tag in filter_tag_list):
                    continue
                    
            filtered_rows.append(row[column].strip())
            
        return filtered_rows

    def read_strings_from_csv(self, csv_file, use_translated, filter_tags, p1_select_by_numbers, p2_select_sequential, p3_select_random_count, translate_output, reuse_last_result, string_list=None):
        # If reusing last result and it exists, return it directly
        if reuse_last_result and self.last_result is not None:
            return self.last_result

        # Read and process strings
        input_strings = self.read_csv_file(csv_file, filter_tags, use_translated)
        result = self.process_string_selection(
            input_strings, 
            p3_select_random_count, 
            p1_select_by_numbers, 
            translate_output,
            p2_select_sequential,
            string_list
        )
        
        # Save result for future reuse
        self.last_result = result
        return result


class StringListToCSV(BaseStringList):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "csv_file": ("STRING", {
                    "default": "output/string_list_output.csv",
                    "placeholder": "Path to save CSV file"
                }),
                "tags": ("STRING", {
                    "default": "",
                    "placeholder": "Comma-separated tags for the prompt"
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

    def write_to_csv(self, csv_file, tags, translate, append_mode, string=None, string_list=None):
        """Write string list to CSV file with optional translation"""
        # Initialize processed_strings and skipped_strings
        processed_strings = []
        skipped_strings = []

        # If neither string nor string_list is provided, return empty lists
        if string is None and string_list is None:
            return processed_strings, skipped_strings
            
        # Convert string to list if it's a list or tuple
        if string is not None:
            if isinstance(string, (list, tuple)):
                string_list = (string_list or []) + list(string)
            else:
                string_list = (string_list or []) + [string]
        elif string_list is None:
            string_list = []

        if len(string_list) == 0 or not string_list:
            return processed_strings, skipped_strings

        # Prepare rows for CSV
        rows_to_write = []
        for string_value in string_list:
            zh_text = translate_texts([string_value], 'zh')[0] if translate else ''
            rows_to_write.append({
                'string': string_value,
                'zh': zh_text,
                'tags': tags
            })

        # Save to CSV using common method
        processed_rows, skipped_rows = self.save_to_csv(csv_file, rows_to_write, append_mode)
        
        # Extract strings from processed and skipped rows
        processed_strings = [row['string'] for row in processed_rows]
        skipped_strings = [row['string'] for row in skipped_rows]
        
        return processed_strings, skipped_strings


class JsonToCSV(BaseStringList):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "json_string": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "placeholder": '{"description": "Detailed image description", "zh": "中文描述", "tags": "Tags with translations"}'
                }),
                "csv_file": ("STRING", {
                    "default": "output/string_list_output.csv",
                    "placeholder": "Path to save CSV file"
                }),
                "append_mode": ("BOOLEAN", {
                    "default": True,
                    "label": "Append to file"
                }),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("message",)
    OUTPUT_NODE = True
    FUNCTION = "write_json_to_csv"
    CATEGORY = "String Helper"

    def write_json_to_csv(self, json_string, csv_file, append_mode):
        """Write JSON string to CSV file and return log message"""
        import json

        try:
            # Parse JSON string
            data = json.loads(json_string)
            
            # Validate required fields
            required_fields = ['description', 'zh', 'tags']
            if not all(field in data for field in required_fields):
                message = f"Error: JSON must contain all required fields: {required_fields}"
                print(message)
                return (message,)

            # Prepare row for CSV
            row = {
                'string': data['description'],
                'zh': data['zh'],
                'tags': data['tags']
            }

            # Save to CSV using common method
            processed_rows, skipped_rows = self.save_to_csv(csv_file, [row], append_mode)
            
            processed_count = len(processed_rows)
            skipped_count = len(skipped_rows)
            
            # Build log message
            messages = []
            if processed_count > 0:
                messages.append(f"Successfully wrote {processed_count} row(s) to {csv_file}")
            if skipped_count > 0:
                messages.append(f"Skipped {skipped_count} duplicate row(s)")
                
            message = ". ".join(messages) if messages else "No changes made"
            print(message)
            
            return (message,)

        except json.JSONDecodeError as e:
            message = f"Error parsing JSON string: {e}"
            print(message)
            return (message,)
        except Exception as e:
            message = f"Error writing to CSV: {e}"
            print(message)
            return (message,)

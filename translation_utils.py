import translators.server as tss
import re

class TranslationUtils:
    @staticmethod
    def translate_with_length_check(strings, target_language):
        translated_strings = []
        for text in strings:
            # Check if the string is too long and split if necessary
            if len(text) > 500:  
                parts = text.split('\n')  # Split by paragraphs
                temp_translated_strings = []
                for part in parts:
                    if len(part) > 500:
                        sub_parts = re.split(r'(?<=[.!?]) +', part)  # Split long paragraphs by sentences
                        for sub_part in sub_parts:
                            if len(sub_part) > 500:
                                sub_sub_parts = [sub_part[i:i+500] for i in range(0, len(sub_part), 500)]  
                                for sub_sub_part in sub_sub_parts:
                                    try:
                                        translated_string = tss.bing(sub_sub_part, from_language='auto', to_language=target_language)
                                        temp_translated_strings.append(translated_string)
                                    except Exception as e:
                                        temp_translated_strings.append(f"Translation error: {str(e)}")  
                            else:
                                try:
                                    translated_string = tss.bing(sub_part, from_language='auto', to_language=target_language)
                                    temp_translated_strings.append(translated_string)
                                except Exception as e:
                                    temp_translated_strings.append(f"Translation error: {str(e)}")  
                    else:
                        try:
                            translated_string = tss.bing(part, from_language='auto', to_language=target_language)
                            temp_translated_strings.append(translated_string)
                        except Exception as e:
                            temp_translated_strings.append(f"Translation error: {str(e)}")  
                # Merge translated strings if they were split
                if len(temp_translated_strings) > 1:
                    translated_strings.append(' '.join(temp_translated_strings))
                else:
                    translated_strings.append(temp_translated_strings[0] if temp_translated_strings else '')
            else:
                try:
                    translated_string = tss.bing(text, from_language='auto', to_language=target_language)
                    translated_strings.append(translated_string)
                except Exception as e:
                    translated_strings.append(f"Translation error: {str(e)}")  

        return translated_strings

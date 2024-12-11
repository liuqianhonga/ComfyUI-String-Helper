from ..translation_utils import TranslationUtils

class ShowTranslateString:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_strings": ("STRING", {
                    "forceInput": True
                }),
                "target_language": (["en", "zh", "es", "fr", "de", "ja", "ko"], {
                    "default": "zh"
                })
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("translated_strings",)
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "translate"
    CATEGORY = "String Helper"

    def translate(self, input_strings, target_language):
        """Translate the input strings to the target language using Bing translator"""
        # Ensure input_strings is a list
        if isinstance(input_strings, str):
            strings_to_translate = [input_strings]
        elif isinstance(input_strings, (list, tuple)):
            strings_to_translate = [str(s) for s in input_strings]
        else:
            strings_to_translate = [str(input_strings)]
        
        #逐个翻译每个字符串
        translated_strings = TranslationUtils.translate_with_length_check(strings_to_translate, target_language)
        
        return {"ui": {"translated_strings": translated_strings}, "result": (translated_strings,)}

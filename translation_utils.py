import translators as ts
import re

def split_text_for_translation(text):
    """
    按段落和完整句子拆分文本，返回句子列表（保持原有段落结构）。
    """
    paragraphs = text.split('\n')
    split_paragraphs = []
    # 句子分隔符：句号、问号、感叹号（中英文）
    sentence_pattern = re.compile(r'([^。！？!?\r\n]+[。！？!?])', re.M)
    for para in paragraphs:
        if not para.strip():
            split_paragraphs.append([''])
            continue
        sentences = sentence_pattern.findall(para)
        # 若正则未能分出句子，则整体作为一句
        if not sentences:
            sentences = [para]
        split_paragraphs.append(sentences)
    return split_paragraphs

def translate_text(text, to_lang='zh'):
    """
    自动处理长文本，按段落和句子拆分，逐句翻译，组合返回。
    """
    if not text:
        return ""
    try:
        # 拆分文本为段落和句子
        split_paragraphs = split_text_for_translation(text)
        translated_paragraphs = []
        for sentences in split_paragraphs:
            if sentences == ['']:
                translated_paragraphs.append('')
                continue
            translated_sentences = []
            for sent in sentences:
                sent = sent.strip()
                if not sent:
                    continue
                # 逐句翻译
                translated = ts.translate_text(sent, translator='bing', from_language='auto', to_language=to_lang)
                translated_sentences.append(translated)
            translated_paragraphs.append(''.join(translated_sentences))
        return '\n'.join(translated_paragraphs)
    except Exception as e:
        return f"[翻译失败] {str(e)}"

def translate_texts(strings, target_language):
    translated_strings = []
    for text in strings:
        try:
            translated_string = translate_text(text, target_language)
            translated_strings.append(translated_string)
        except Exception as e:
            translated_strings.append(f"Translation error: {str(e)}")  

    return translated_strings

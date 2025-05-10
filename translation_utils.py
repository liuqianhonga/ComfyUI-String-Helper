import translators as ts
import re

# 输入长度限制
INPUT_LIMIT = 1000

def split_text_for_translation(text):
    """
    按段落和完整句子拆分文本，返回句子列表（保持原有段落结构）。
    """
    paragraphs = text.split('\n')
    split_paragraphs = []
    # 句子分隔符：句号、问号、感叹号（英文和中文）
    sentence_pattern = re.compile(r'([^.!?。！？]+[.!?。！？])', re.M)
    
    for para in paragraphs:
        if not para.strip():
            split_paragraphs.append([''])
            continue
        
        # 如果段落长度小于INPUT_LIMIT，直接添加
        if len(para) < INPUT_LIMIT:
            split_paragraphs.append([para])
            continue
        
        # 分割句子
        sentences = sentence_pattern.findall(para)
        
        # 若正则未能分出句子，则按照INPUT_LIMIT拆分
        if not sentences:
            sentences = [para[i:i+INPUT_LIMIT] for i in range(0, len(para), INPUT_LIMIT)]
        
        # 组合句子的逻辑
        optimized_sentences = []
        current_group = []
        current_length = 0
        
        for sent in sentences:
            # 计算当前句子长度
            sent_length = len(sent)
            
            # 如果加入这个句子后总长度小于INPUT_LIMIT，则加入
            if current_length + sent_length < INPUT_LIMIT:
                current_group.append(sent)
                current_length += sent_length
            else:
                # 如果当前组不为空，先保存当前组
                if current_group:
                    optimized_sentences.append(''.join(current_group))
                
                # 重置组
                current_group = [sent]
                current_length = sent_length
        
        # 添加最后一组
        if current_group:
            optimized_sentences.append(''.join(current_group))
        
        split_paragraphs.append(optimized_sentences)
    
    return split_paragraphs

def translate_text(text, from_lang='en', to_lang='zh'):
    """
    自动处理长文本，按段落和句子拆分，逐句翻译，组合返回。
    对于短文本，直接翻译。
    """
    if not text:
        return ""
    
    try:
        # 如果整个文本长度小于INPUT_LIMIT，直接翻译
        if len(text) < INPUT_LIMIT:
            return ts.translate_text(text, translator='bing', from_language=from_lang, to_language=to_lang)
        
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
                translated = ts.translate_text(sent, translator='bing', from_language=from_lang, to_language=to_lang)
                translated_sentences.append(translated)
            translated_paragraphs.append(''.join(translated_sentences))
        
        return '\n'.join(translated_paragraphs)
    except Exception as e:
        return f"[翻译失败] {str(e)}"


def translate_texts(strings, target_language):
    translated_strings = []
    for text in strings:
        try:
            translated_string = translate_text(text, 'auto', target_language)
            translated_strings.append(translated_string)
        except Exception as e:
            translated_strings.append(f"Translation error: {str(e)}")  

    return translated_strings

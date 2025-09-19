# 文本预处理模块
# 负责文本的清洗、分词、向量化等预处理工作

import re
import jieba
from collections import Counter

# 中文停用词列表（简化版）
STOP_WORDS = {
    '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', 
    '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好',
    '自己', '这', '那', '他', '她', '它', '们', '我们', '你们', '他们', '这个',
    '那个', '什么', '怎么', '为什么', '因为', '所以', '但是', '然后', '如果',
    '虽然', '不过', '而且', '或者', '还是', '就是', '只是', '已经', '正在',
    '可以', '应该', '需要', '必须', '可能', '也许', '大概', '似乎', '看起来'
}

def clean_text(text):
    """
    清洗文本，去除特殊字符和多余空格
    """
    if not text:
        return ""
    
    # 去除换行符和制表符
    text = text.replace('\n', ' ').replace('\t', ' ')
    
    # 去除多余空格
    text = re.sub(r'\s+', ' ', text)
    
    # 去除标点符号（保留中文标点）
    text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9\s]', '', text)
    
    # 去除数字（可选，根据需求决定）
    # text = re.sub(r'\d+', '', text)
    
    return text.strip()

def tokenize_text(text):
    """
    对文本进行分词处理
    """
    if not text:
        return []
    
    # 使用jieba进行中文分词
    words = jieba.lcut(text)
    
    # 过滤空字符串和单字符
    words = [word for word in words if len(word) > 1]
    
    return words

def remove_stop_words(words):
    """
    去除停用词
    """
    if not words:
        return []
    
    return [word for word in words if word not in STOP_WORDS]

def preprocess_text(text):
    """
    完整的文本预处理流程
    """
    # 1. 清洗文本
    clean_text_result = clean_text(text)
    
    # 2. 分词
    words = tokenize_text(clean_text_result)
    
    # 3. 去除停用词
    filtered_words = remove_stop_words(words)
    
    return filtered_words

def get_word_frequency(words):
    """
    计算词频
    """
    if not words:
        return {}
    
    return Counter(words)

def vectorize_text(text):
    """
    将文本转换为向量表示（词频向量）
    """
    words = preprocess_text(text)
    word_freq = get_word_frequency(words)
    
    # 返回词频字典
    return dict(word_freq)

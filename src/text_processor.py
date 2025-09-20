# -*- coding: utf-8 -*-
"""
论文查重系统 - 文本预处理模块
============================

本模块负责文本的预处理工作，包括文本清洗、中文分词、
停用词过滤、向量化等核心功能。主要特点：

1. 支持中文文本处理
2. 使用jieba进行中文分词
3. 内置中文停用词库
4. 性能优化和缓存机制
5. 支持大文件流式处理
6. 并行处理支持

作者：3123004462
创建时间：2024年9月
版本：1.0.0
"""

import re
import jieba
from collections import Counter
from functools import lru_cache
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor

# 中文停用词列表（简化版）
STOP_WORDS = {
    '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', 
    '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好',
    '自己', '这', '那', '他', '她', '它', '们', '我们', '你们', '他们', '这个',
    '那个', '什么', '怎么', '为什么', '因为', '所以', '但是', '然后', '如果',
    '虽然', '不过', '而且', '或者', '还是', '就是', '只是', '已经', '正在',
    '可以', '应该', '需要', '必须', '可能', '也许', '大概', '似乎', '看起来'
}

# 性能优化：简化jieba初始化，避免重复初始化

# 性能优化：使用更激进的分词优化策略
def ultra_fast_tokenize(text):
    """
    超快速分词函数，使用最简化的jieba配置
    """
    if not text:
        return []
    try:
        # 性能优化：使用jieba的最快模式
        # 1. 关闭HMM（隐马尔可夫模型）
        # 2. 使用精确模式但跳过一些复杂计算
        # 3. 限制文本长度以避免过长的处理时间
        if len(text) > 10000:  # 对于超长文本，截取前10000个字符
            text = text[:10000]
        
        words = jieba.lcut(text, cut_all=False, HMM=False)
        # 只保留长度大于1的词，并转换为tuple以支持缓存
        return tuple(word for word in words if len(word) > 1)
    except Exception as e:
        raise ValueError(f"分词处理失败: {e}")

# 性能优化：备用轻量分词方法
def lightweight_tokenize(text):
    """
    轻量级分词函数，当jieba太慢时的备用方案
    """
    if not text:
        return []
    try:
        # 使用简单的字符分割作为备用方案
        # 按标点符号和空格分割
        import re
        words = re.findall(r'[\u4e00-\u9fa5]+', text)  # 只保留中文字符
        return tuple(word for word in words if len(word) > 1)
    except Exception as e:
        raise ValueError(f"轻量分词处理失败: {e}")

# 性能优化：分词结果缓存，避免重复计算
@lru_cache(maxsize=512)
def cached_tokenize(text):
    """
    缓存的分词函数，避免重复计算相同文本
    """
    return ultra_fast_tokenize(text)

# 性能优化：文本预处理缓存
@lru_cache(maxsize=256)
def cached_preprocess(text):
    """
    缓存完整的文本预处理结果
    """
    if not text:
        return []
    
    # 清洗文本
    clean_text_result = clean_text(text)
    
    # 分词
    words_tuple = cached_tokenize(clean_text_result)
    words = list(words_tuple)
    
    # 去除停用词
    filtered_words = remove_stop_words(words)
    
    return tuple(filtered_words)

# 性能优化：流式处理大文件
def process_large_file(file_path, chunk_size=10000):
    """
    流式处理大文件，避免内存溢出
    
    Args:
        file_path (str): 文件路径
        chunk_size (int): 每次读取的字符数
        
    Yields:
        str: 处理后的文本块
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                # 对每个块进行预处理
                processed_chunk = preprocess_text(chunk)
                yield processed_chunk
    except Exception as e:
        raise ValueError(f"流式处理文件失败: {e}")

# 性能优化：大文件相似度计算
def calculate_large_file_similarity(file1_path, file2_path, chunk_size=10000):
    """
    计算两个大文件的相似度，使用流式处理
    
    Args:
        file1_path (str): 第一个文件路径
        file2_path (str): 第二个文件路径
        chunk_size (int): 每次处理的字符数
        
    Returns:
        float: 相似度值
    """
    try:
        # 收集所有处理后的词汇
        all_words1 = []
        all_words2 = []
        
        # 流式处理第一个文件
        for chunk_words in process_large_file(file1_path, chunk_size):
            all_words1.extend(chunk_words)
        
        # 流式处理第二个文件
        for chunk_words in process_large_file(file2_path, chunk_size):
            all_words2.extend(chunk_words)
        
        # 计算相似度
        from .similarity_calculator import enhanced_jaccard_similarity
        return enhanced_jaccard_similarity(all_words1, all_words2)
        
    except Exception as e:
        raise ValueError(f"大文件相似度计算失败: {e}")

# 性能优化：并行处理文本（多进程版本）
def parallel_preprocess_texts(texts):
    """
    并行处理多个文本，提高处理效率
    支持多进程和线程池两种模式
    """
    if len(texts) <= 1:
        return [preprocess_text(text) for text in texts]
    
    # 对于CPU密集型任务，使用多进程
    if len(texts) >= 4:  # 当文本数量较多时使用多进程
        try:
            with mp.Pool(processes=min(4, len(texts))) as pool:
                results = pool.map(preprocess_text, texts)
            return results
        except Exception:
            # 如果多进程失败，回退到线程池
            pass
    
    # 默认使用线程池
    with ThreadPoolExecutor(max_workers=min(2, len(texts))) as executor:
        results = list(executor.map(preprocess_text, texts))
    return results

def clean_text(text):
    """
    清洗文本，去除特殊字符和多余空格
    =================================
    
    对原始文本进行清洗处理，包括：
    1. 去除换行符和制表符
    2. 合并多余空格
    3. 去除标点符号（保留中文标点）
    4. 文本长度限制检查
    5. 去除首尾空格
    
    Args:
        text (str): 原始文本，不能为None
        
    Returns:
        str: 清洗后的文本，去除特殊字符和多余空格
        
    Raises:
        TypeError: 当输入不是字符串类型时抛出
        ValueError: 当文本过长（超过500万字符）时抛出
        
    示例:
        >>> clean_text("这是  一个\n测试\t文本。")
        "这是 一个 测试 文本"
        
    性能说明:
        - 使用正则表达式优化处理速度
        - 支持最大500万字符的文本
        - 处理时间与文本长度成正比
    """
    # 输入验证
    if text is None:
        return ""
    
    if not isinstance(text, str):
        raise TypeError(f"文本必须是字符串类型，当前类型: {type(text)}")
    
    # 检查文本长度（确保内存使用不超过2048MB）
    if len(text) > 5000000:  # 500万字符限制，确保内存使用合理
        raise ValueError(f"文本过长 ({len(text)} 字符)，超过500万字符限制")
    
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
    对文本进行分词处理（优化版本，使用缓存）
    
    Args:
        text (str): 待分词的文本
        
    Returns:
        list: 分词结果列表
        
    Raises:
        TypeError: 输入不是字符串类型
        ValueError: 文本内容无效
    """
    # 输入验证
    if not text:
        return []
    
    if not isinstance(text, str):
        raise TypeError(f"文本必须是字符串类型，当前类型: {type(text)}")
    
    try:
        # 使用缓存的分词函数
        words_tuple = cached_tokenize(text)
        return list(words_tuple)
    except Exception as e:
        raise ValueError(f"分词处理失败: {e}")

def remove_stop_words(words):
    """
    去除停用词
    
    Args:
        words (list): 词汇列表
        
    Returns:
        list: 去除停用词后的词汇列表
        
    Raises:
        TypeError: 输入不是列表类型
    """
    if not words:
        return []
    
    if not isinstance(words, list):
        raise TypeError(f"词汇列表必须是列表类型，当前类型: {type(words)}")
    
    return [word for word in words if word not in STOP_WORDS]

def preprocess_text(text):
    """
    完整的文本预处理流程
    
    Args:
        text (str): 原始文本
        
    Returns:
        list: 预处理后的词汇列表
        
    Raises:
        TypeError: 输入类型错误
        ValueError: 文本内容无效
    """
    try:
        # 1. 清洗文本
        clean_text_result = clean_text(text)
        
        # 2. 分词
        words = tokenize_text(clean_text_result)
        
        # 3. 去除停用词
        filtered_words = remove_stop_words(words)
        
        return filtered_words
    except (TypeError, ValueError) as e:
        # 重新抛出已知异常
        raise
    except Exception as e:
        raise ValueError(f"文本预处理失败: {e}")

def get_word_frequency(words):
    """
    计算词频
    
    Args:
        words (list): 词汇列表
        
    Returns:
        dict: 词频字典
        
    Raises:
        TypeError: 输入不是列表类型
    """
    if not words:
        return {}
    
    if not isinstance(words, list):
        raise TypeError(f"词汇列表必须是列表类型，当前类型: {type(words)}")
    
    return Counter(words)

def vectorize_text(text):
    """
    将文本转换为向量表示（词频向量）
    
    Args:
        text (str): 原始文本
        
    Returns:
        dict: 词频向量字典
        
    Raises:
        TypeError: 输入类型错误
        ValueError: 文本内容无效
    """
    try:
        # 性能优化：直接使用缓存的分词结果，避免重复预处理
        words_tuple = cached_tokenize(text)
        words = list(words_tuple)
        
        # 去除停用词
        filtered_words = remove_stop_words(words)
        
        # 计算词频
        word_freq = get_word_frequency(filtered_words)
        
        # 返回词频字典
        return dict(word_freq)
    except (TypeError, ValueError) as e:
        # 重新抛出已知异常
        raise
    except Exception as e:
        raise ValueError(f"文本向量化失败: {e}")

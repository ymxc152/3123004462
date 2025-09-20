# -*- coding: utf-8 -*-
"""
论文查重系统 - 核心算法模块
============================

本模块是论文查重系统的核心算法模块，负责整合各个子模块，
实现完整的查重流程。主要功能包括：

1. 文本相似度计算
2. 模块延迟导入和缓存优化
3. 大文件流式处理
4. 异常处理和错误恢复

作者：3123004462
创建时间：2024年9月
版本：1.0.0
"""

# 性能优化：模块级缓存，避免重复导入
_imported_modules = {}  # 存储已导入的模块
_module_functions = {}  # 存储已缓存的函数

def lazy_import(module_name):
    """
    延迟导入模块，实现模块级缓存
    
    Args:
        module_name (str): 模块名称
        
    Returns:
        module: 导入的模块
    """
    if module_name not in _imported_modules:
        try:
            if module_name == 'text_processor':
                from . import text_processor
                _imported_modules[module_name] = text_processor
            elif module_name == 'similarity_calculator':
                from . import similarity_calculator
                _imported_modules[module_name] = similarity_calculator
            elif module_name == 'file_utils':
                from . import file_utils
                _imported_modules[module_name] = file_utils
            else:
                _imported_modules[module_name] = __import__(module_name)
        except ImportError as e:
            raise ImportError(f"无法导入模块 {module_name}: {e}")
    return _imported_modules[module_name]

def get_cached_function(module_name, function_name):
    """
    获取缓存的函数，避免重复查找
    
    Args:
        module_name (str): 模块名称
        function_name (str): 函数名称
        
    Returns:
        function: 缓存的函数
    """
    cache_key = f"{module_name}.{function_name}"
    if cache_key not in _module_functions:
        module = lazy_import(module_name)
        _module_functions[cache_key] = getattr(module, function_name)
    return _module_functions[cache_key]

# 性能优化：延迟导入核心模块
def get_text_processor():
    """获取文本处理模块"""
    return lazy_import('text_processor')

def get_similarity_calculator():
    """获取相似度计算模块"""
    return lazy_import('similarity_calculator')

def get_file_utils():
    """获取文件工具模块"""
    return lazy_import('file_utils')

def calculate_similarity(text1, text2):
    """
    计算两段文本的相似度（主入口函数）
    ===================================
    
    这是论文查重系统的核心函数，负责计算两段文本的相似度。
    使用改进的Jaccard相似度算法，考虑词频权重，提高查重准确度。
    
    算法流程：
    1. 输入验证和预处理
    2. 文本分词和清洗
    3. 去除停用词
    4. 计算词频向量
    5. 使用改进Jaccard算法计算相似度
    6. 返回0.0-1.0范围的相似度值
    
    Args:
        text1 (str): 原文文本，不能为空
        text2 (str): 抄袭版文本，不能为空
    
    Returns:
        float: 相似度值，范围0.0-1.0
               0.0表示完全不相似
               1.0表示完全相同
        
    Raises:
        TypeError: 当输入不是字符串类型时抛出
        ValueError: 当文本内容无效或计算失败时抛出
        
    示例:
        >>> similarity = calculate_similarity("这是原文", "这是抄袭版")
        >>> print(f"相似度: {similarity:.2f}")
        相似度: 0.75
        
    性能说明:
        - 使用缓存机制避免重复计算
        - 支持最大500万字符的文本
        - 处理时间通常在1秒以内
    """
    # 输入验证
    if not text1 or not text2:
        return 0.0
    
    if not isinstance(text1, str) or not isinstance(text2, str):
        raise TypeError("文本必须是字符串类型")
    
    try:
        # 直接导入，避免复杂的延迟导入开销
        from .text_processor import cached_preprocess, get_word_frequency
        from .similarity_calculator import enhanced_jaccard_similarity
        
        # 获取完整的预处理结果（使用缓存）
        words1_tuple = cached_preprocess(text1)
        words2_tuple = cached_preprocess(text2)
        
        # 转换为列表
        words1 = list(words1_tuple)
        words2 = list(words2_tuple)
        
        # 向量化（直接使用已处理的词汇）
        vec1 = get_word_frequency(words1)
        vec2 = get_word_frequency(words2)
        
        # 使用改进的Jaccard相似度计算
        # 考虑词频权重，提高准确度
        jaccard_sim = enhanced_jaccard_similarity(words1, words2)
        
        # 确保结果在有效范围内
        return max(0.0, min(1.0, jaccard_sim))
        
    except (TypeError, ValueError) as e:
        # 重新抛出已知异常
        raise
    except Exception as e:
        raise ValueError(f"相似度计算失败: {e}")

def calculate_large_file_similarity(file1_path, file2_path, chunk_size=10000):
    """
    计算两个大文件的相似度，使用流式处理
    这是对原有calculate_similarity的扩展，专门处理大文件
    
    Args:
        file1_path (str): 第一个文件路径
        file2_path (str): 第二个文件路径
        chunk_size (int): 每次处理的字符数
        
    Returns:
        float: 相似度值 (0.0-1.0)
    """
    try:
        # 使用延迟导入获取大文件处理函数
        text_processor = get_text_processor()
        calculate_large_file_similarity_func = get_cached_function('text_processor', 'calculate_large_file_similarity')
        
        return calculate_large_file_similarity_func(file1_path, file2_path, chunk_size)
        
    except Exception as e:
        raise ValueError(f"大文件相似度计算失败: {e}")

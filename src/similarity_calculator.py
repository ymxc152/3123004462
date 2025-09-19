# 相似度计算模块
# 负责计算两个文本向量的相似度

import math
from collections import Counter

def cosine_similarity(vec1, vec2):
    """
    计算余弦相似度
    
    Args:
        vec1 (dict): 第一个文本的词频向量
        vec2 (dict): 第二个文本的词频向量
        
    Returns:
        float: 余弦相似度值 (0.0-1.0)
        
    Raises:
        TypeError: 输入不是字典类型
        ValueError: 向量内容无效
    """
    # 输入验证
    if not vec1 or not vec2:
        return 0.0
    
    if not isinstance(vec1, dict) or not isinstance(vec2, dict):
        raise TypeError("向量必须是字典类型")
    
    try:
        # 获取所有词汇
        all_words = set(vec1.keys()) | set(vec2.keys())
        
        if not all_words:
            return 0.0
        
        # 构建向量
        v1 = [vec1.get(word, 0) for word in all_words]
        v2 = [vec2.get(word, 0) for word in all_words]
        
        # 验证向量值
        for val in v1 + v2:
            if not isinstance(val, (int, float)) or val < 0:
                raise ValueError("向量值必须是非负数字")
        
        # 计算点积
        dot_product = sum(a * b for a, b in zip(v1, v2))
        
        # 计算模长
        norm1 = math.sqrt(sum(a * a for a in v1))
        norm2 = math.sqrt(sum(b * b for b in v2))
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        result = dot_product / (norm1 * norm2)
        
        # 确保结果在有效范围内
        return max(0.0, min(1.0, result))
        
    except (ValueError, TypeError) as e:
        raise
    except Exception as e:
        raise ValueError(f"余弦相似度计算失败: {e}")

def jaccard_similarity(set1, set2):
    """
    计算Jaccard相似度
    
    Args:
        set1 (set): 第一个集合
        set2 (set): 第二个集合
        
    Returns:
        float: Jaccard相似度值 (0.0-1.0)
        
    Raises:
        TypeError: 输入不是集合类型
    """
    # 输入验证
    if not isinstance(set1, set) or not isinstance(set2, set):
        raise TypeError("输入必须是集合类型")
    
    if not set1 and not set2:
        return 1.0
    if not set1 or not set2:
        return 0.0
    
    try:
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        
        return intersection / union if union > 0 else 0.0
    except Exception as e:
        raise ValueError(f"Jaccard相似度计算失败: {e}")

def word_overlap_similarity(words1, words2):
    """
    计算词汇重叠相似度
    
    Args:
        words1 (list): 第一个文本的词汇列表
        words2 (list): 第二个文本的词汇列表
        
    Returns:
        float: 词汇重叠相似度值 (0.0-1.0)
        
    Raises:
        TypeError: 输入不是列表类型
    """
    # 输入验证
    if not isinstance(words1, list) or not isinstance(words2, list):
        raise TypeError("词汇列表必须是列表类型")
    
    if not words1 and not words2:
        return 1.0
    if not words1 or not words2:
        return 0.0
    
    try:
        set1 = set(words1)
        set2 = set(words2)
        
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        
        return intersection / union if union > 0 else 0.0
    except Exception as e:
        raise ValueError(f"词汇重叠相似度计算失败: {e}")

def calculate_similarity(text1, text2):
    """
    计算两段文本的相似度（主函数）
    使用多种方法计算并取平均值
    """
    if not text1 or not text2:
        return 0.0
    
    # 简单的词汇分割
    words1 = text1.split()
    words2 = text2.split()
    
    # 计算词汇重叠相似度
    overlap_sim = word_overlap_similarity(words1, words2)
    
    # 计算字符级别的相似度
    char_sim = jaccard_similarity(set(text1), set(text2))
    
    # 取平均值
    similarity = (overlap_sim + char_sim) / 2
    
    return min(similarity, 1.0)  # 确保不超过1.0

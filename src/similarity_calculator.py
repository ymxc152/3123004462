# 相似度计算模块
# 负责计算两个文本向量的相似度

import math
from collections import Counter

def cosine_similarity(vec1, vec2):
    """
    计算余弦相似度
    """
    if not vec1 or not vec2:
        return 0.0
    
    # 获取所有词汇
    all_words = set(vec1.keys()) | set(vec2.keys())
    
    # 构建向量
    v1 = [vec1.get(word, 0) for word in all_words]
    v2 = [vec2.get(word, 0) for word in all_words]
    
    # 计算点积
    dot_product = sum(a * b for a, b in zip(v1, v2))
    
    # 计算模长
    norm1 = math.sqrt(sum(a * a for a in v1))
    norm2 = math.sqrt(sum(b * b for b in v2))
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    return dot_product / (norm1 * norm2)

def jaccard_similarity(set1, set2):
    """
    计算Jaccard相似度
    """
    if not set1 and not set2:
        return 1.0
    if not set1 or not set2:
        return 0.0
    
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    
    return intersection / union if union > 0 else 0.0

def word_overlap_similarity(words1, words2):
    """
    计算词汇重叠相似度
    """
    if not words1 and not words2:
        return 1.0
    if not words1 or not words2:
        return 0.0
    
    set1 = set(words1)
    set2 = set(words2)
    
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    
    return intersection / union if union > 0 else 0.0

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

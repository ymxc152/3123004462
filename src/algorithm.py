# 查重算法主模块
# 整合各个子模块，实现完整的查重流程

from .text_processor import preprocess_text, vectorize_text
from .similarity_calculator import cosine_similarity, jaccard_similarity, word_overlap_similarity

def calculate_similarity(text1, text2):
    """
    计算两段文本的相似度（主入口函数）
    
    Args:
        text1: 原文文本
        text2: 抄袭版文本
    
    Returns:
        float: 相似度值 (0.0-1.0)
    """
    if not text1 or not text2:
        return 0.0
    
    # 文本预处理
    words1 = preprocess_text(text1)
    words2 = preprocess_text(text2)
    
    # 向量化
    vec1 = vectorize_text(text1)
    vec2 = vectorize_text(text2)
    
    # 计算多种相似度
    cosine_sim = cosine_similarity(vec1, vec2)
    jaccard_sim = jaccard_similarity(set(words1), set(words2))
    overlap_sim = word_overlap_similarity(words1, words2)
    
    # 取平均值作为最终结果
    similarity = (cosine_sim + jaccard_sim + overlap_sim) / 3
    
    return min(similarity, 1.0)  # 确保不超过1.0

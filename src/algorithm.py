# 查重算法主模块
# 整合各个子模块，实现完整的查重流程

from .text_processor import clean_text, tokenize_text, vectorize_text
from .similarity_calculator import calculate_similarity as calc_sim
from .result_formatter import format_similarity

def calculate_similarity(text1, text2):
    """
    计算两段文本的相似度（主入口函数）
    
    Args:
        text1: 原文文本
        text2: 抄袭版文本
    
    Returns:
        float: 相似度值 (0.0-1.0)
    """
    # 文本预处理
    clean_text1 = clean_text(text1)
    clean_text2 = clean_text(text2)
    
    # 分词
    tokens1 = tokenize_text(clean_text1)
    tokens2 = tokenize_text(clean_text2)
    
    # 向量化
    vec1 = vectorize_text(clean_text1)
    vec2 = vectorize_text(clean_text2)
    
    # 计算相似度
    similarity = calc_sim(clean_text1, clean_text2)
    
    return similarity

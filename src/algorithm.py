# 查重算法主模块
# 整合各个子模块，实现完整的查重流程

from .text_processor import preprocess_text, vectorize_text
from .similarity_calculator import cosine_similarity, jaccard_similarity, word_overlap_similarity

def calculate_similarity(text1, text2):
    """
    计算两段文本的相似度（主入口函数）
    
    Args:
        text1 (str): 原文文本
        text2 (str): 抄袭版文本
    
    Returns:
        float: 相似度值 (0.0-1.0)
        
    Raises:
        TypeError: 输入类型错误
        ValueError: 文本内容无效
    """
    # 输入验证
    if not text1 or not text2:
        return 0.0
    
    if not isinstance(text1, str) or not isinstance(text2, str):
        raise TypeError("文本必须是字符串类型")
    
    try:
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
        
        # 确保结果在有效范围内
        return max(0.0, min(1.0, similarity))
        
    except (TypeError, ValueError) as e:
        # 重新抛出已知异常
        raise
    except Exception as e:
        raise ValueError(f"相似度计算失败: {e}")

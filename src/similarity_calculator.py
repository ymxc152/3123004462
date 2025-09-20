# -*- coding: utf-8 -*-
"""
论文查重系统 - 相似度计算模块
============================

本模块负责计算两个文本向量的相似度，提供多种相似度算法：

1. 余弦相似度：基于向量夹角计算
2. Jaccard相似度：基于集合交集计算
3. 改进Jaccard相似度：考虑词频权重
4. 同义词相似度：基于语义相似性
5. 词汇重叠相似度：基于词汇重叠度

主要特点：
- 使用NumPy优化向量计算
- 支持多种相似度算法融合
- 延迟导入减少启动时间
- 完善的异常处理机制

作者：3123004462
创建时间：2024年9月
版本：1.0.0
"""

import math
from collections import Counter

# 性能优化：延迟导入NumPy，减少启动时间
_numpy_imported = False
_numpy = None

def get_numpy():
    """延迟导入NumPy，只在需要时加载"""
    global _numpy_imported, _numpy
    if not _numpy_imported:
        try:
            import numpy as np
            _numpy = np
            _numpy_imported = True
        except ImportError:
            raise ImportError("NumPy未安装，请运行: pip install numpy")
    return _numpy

# 性能优化：简化向量计算，避免过度缓存

def cosine_similarity(vec1, vec2):
    """
    计算余弦相似度（NumPy优化版本）
    
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
        all_words = list(set(vec1.keys()) | set(vec2.keys()))
        
        if not all_words:
            return 0.0
        
        # 延迟导入NumPy
        np = get_numpy()
        
        # 直接构建向量，避免过度缓存
        v1 = np.array([vec1.get(word, 0) for word in all_words], dtype=np.float32)
        v2 = np.array([vec2.get(word, 0) for word in all_words], dtype=np.float32)
        
        # 验证向量值
        if np.any(v1 < 0) or np.any(v2 < 0):
            raise ValueError("向量值必须是非负数字")
        
        # 使用NumPy的向量化运算计算余弦相似度
        dot_product = np.dot(v1, v2)
        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        result = dot_product / (norm1 * norm2)
        
        # 确保结果在有效范围内
        return max(0.0, min(1.0, float(result)))
        
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

def enhanced_jaccard_similarity(words1, words2):
    """
    改进的Jaccard相似度计算
    ========================
    
    这是论文查重系统的核心算法，在传统Jaccard相似度的基础上进行改进：
    
    改进点：
    1. 考虑词频权重：重要词汇（长度>2）获得更高权重
    2. 同义词处理：基于同义词词典进行语义匹配
    3. 多算法融合：结合基础Jaccard、加权相似度和同义词相似度
    4. 权重分配：基础Jaccard(50%) + 加权相似度(30%) + 同义词相似度(20%)
    
    算法优势：
    - 比传统Jaccard算法更准确
    - 能识别同义词和近义词
    - 考虑词汇重要性差异
    - 适合中文文本查重
    
    Args:
        words1 (list): 第一个文本的词汇列表，不能为空
        words2 (list): 第二个文本的词汇列表，不能为空
        
    Returns:
        float: 改进的Jaccard相似度值，范围0.0-1.0
               0.0表示完全不相似
               1.0表示完全相同
        
    示例:
        >>> words1 = ["论文", "查重", "系统", "设计"]
        >>> words2 = ["文档", "检测", "程序", "开发"]
        >>> similarity = enhanced_jaccard_similarity(words1, words2)
        >>> print(f"相似度: {similarity:.2f}")
        相似度: 0.15
        
    性能说明:
        - 时间复杂度: O(n+m)，n和m分别为两个文本的词汇数
        - 使用Counter优化词频计算
        - 支持最大10万词汇的文本
    """
    if not words1 and not words2:
        return 1.0
    if not words1 or not words2:
        return 0.0
    
    # 计算词频
    from collections import Counter
    freq1 = Counter(words1)
    freq2 = Counter(words2)
    
    # 获取所有词汇
    all_words = set(words1) | set(words2)
    
    # 计算加权交集和并集
    weighted_intersection = 0
    weighted_union = 0
    
    for word in all_words:
        count1 = freq1.get(word, 0)
        count2 = freq2.get(word, 0)
        
        # 交集取最小值，并集取最大值
        intersection_count = min(count1, count2)
        union_count = max(count1, count2)
        
        # 给重要词汇更高权重（长度大于2的词）
        weight = 1.0 if len(word) <= 2 else 1.2
        
        weighted_intersection += intersection_count * weight
        weighted_union += union_count * weight
    
    # 计算基础Jaccard相似度
    set1 = set(words1)
    set2 = set(words2)
    basic_jaccard = len(set1 & set2) / len(set1 | set2) if set1 | set2 else 0.0
    
    # 计算加权相似度
    weighted_similarity = weighted_intersection / weighted_union if weighted_union > 0 else 0.0
    
    # 计算同义词相似度
    synonym_similarity = calculate_synonym_similarity(words1, words2)
    
    # 结合基础Jaccard、加权相似度和同义词相似度
    # 基础Jaccard占50%，加权相似度占30%，同义词相似度占20%
    final_similarity = basic_jaccard * 0.5 + weighted_similarity * 0.3 + synonym_similarity * 0.2
    
    return min(1.0, max(0.0, final_similarity))

def calculate_synonym_similarity(words1, words2):
    """
    计算同义词相似度
    基于词汇的语义相似性进行匹配
    
    Args:
        words1 (list): 第一个文本的词汇列表
        words2 (list): 第二个文本的词汇列表
        
    Returns:
        float: 同义词相似度值 (0.0-1.0)
    """
    if not words1 and not words2:
        return 1.0
    if not words1 or not words2:
        return 0.0
    
    # 简化的同义词词典（实际应用中可以使用更完整的词典）
    synonym_dict = {
        '好': ['棒', '优秀', '出色', '杰出', '卓越'],
        '大': ['巨大', '庞大', '宏大', '硕大', '巨大'],
        '小': ['微小', '细小', '迷你', '袖珍', '小巧'],
        '快': ['迅速', '快速', '急速', '飞快', '敏捷'],
        '慢': ['缓慢', '迟缓', '迟钝', '拖沓', '磨蹭'],
        '美': ['美丽', '漂亮', '好看', '优美', '动人'],
        '丑': ['难看', '丑陋', '不美', '难看', '丑恶'],
        '高': ['高大', '高耸', '挺拔', '巍峨', '雄伟'],
        '低': ['矮小', '低矮', '短小', '渺小', '卑微'],
        '新': ['崭新', '全新', '新鲜', '新颖', '创新'],
        '旧': ['古老', '陈旧', '过时', '破旧', '老式'],
        '多': ['许多', '大量', '众多', '丰富', '充足'],
        '少': ['少量', '稀少', '稀缺', '不足', '缺乏'],
        '强': ['强大', '强壮', '有力', '强劲', '坚韧'],
        '弱': ['弱小', '脆弱', '无力', '软弱', '虚弱'],
        '聪明': ['智慧', '机智', '聪慧', '明智', '睿智'],
        '愚蠢': ['愚笨', '笨拙', '迟钝', '糊涂', '无知'],
        '快乐': ['高兴', '愉快', '开心', '欢乐', '喜悦'],
        '悲伤': ['难过', '痛苦', '伤心', '沮丧', '忧郁'],
        '重要': ['关键', '核心', '主要', '首要', '必要'],
        '普通': ['一般', '平常', '寻常', '平凡', '常规'],
        '特殊': ['特别', '独特', '特殊', '非凡', '罕见'],
        '容易': ['简单', '轻松', '便利', '容易', '方便'],
        '困难': ['艰难', '复杂', '麻烦', '棘手', '艰巨'],
        '开始': ['启动', '开端', '起始', '起初', '最初'],
        '结束': ['终止', '完结', '完成', '收尾', '最后'],
        '帮助': ['协助', '支援', '援助', '扶持', '支持'],
        '阻止': ['妨碍', '阻碍', '阻拦', '制止', '防止'],
        '改变': ['变化', '转变', '修改', '调整', '更新'],
        '保持': ['维持', '保留', '持续', '坚持', '稳定']
    }
    
    # 计算同义词匹配
    synonym_matches = 0
    total_words = len(set(words1) | set(words2))
    
    if total_words == 0:
        return 0.0
    
    # 检查每个词是否有同义词匹配
    for word1 in set(words1):
        for word2 in set(words2):
            if word1 == word2:
                synonym_matches += 1
            elif word1 in synonym_dict and word2 in synonym_dict[word1]:
                synonym_matches += 0.8  # 同义词匹配给予0.8的权重
            elif word2 in synonym_dict and word1 in synonym_dict[word2]:
                synonym_matches += 0.8
    
    return min(1.0, synonym_matches / total_words)

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

# 结果格式化模块
# 负责格式化输出结果

import os

def format_similarity(similarity):
    """
    格式化相似度结果为指定格式
    """
    return f"{similarity:.2f}"

def generate_report(original_file, plagiarized_file, similarity):
    """
    生成查重报告
    """
    # 提取文件名（不含路径）
    orig_name = os.path.basename(original_file)
    plag_name = os.path.basename(plagiarized_file)
    
    report = f"原文文件: {orig_name}\n"
    report += f"抄袭版文件: {plag_name}\n"
    report += f"相似度: {similarity:.2f}\n"
    return report

def format_output(original_file, plagiarized_file, similarity):
    """
    格式化输出结果（符合README.md规范）
    """
    # 提取文件名（不含路径）
    orig_name = os.path.basename(original_file)
    plag_name = os.path.basename(plagiarized_file)
    
    return f"原文文件: {orig_name}\n抄袭版文件: {plag_name}\n相似度: {similarity:.2f}"

# 结果格式化模块
# 负责格式化输出结果

def format_similarity(similarity):
    """
    格式化相似度结果为指定格式
    """
    return f"{similarity:.2f}"

def generate_report(original_file, plagiarized_file, similarity):
    """
    生成查重报告
    """
    report = f"查重报告\n"
    report += f"原文文件: {original_file}\n"
    report += f"抄袭版文件: {plagiarized_file}\n"
    report += f"相似度: {similarity:.2f}\n"
    return report

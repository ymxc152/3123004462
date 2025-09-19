# 文件处理工具模块

import os
from datetime import datetime

def read_file(file_path):
    """
    读取文件内容
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"读取文件失败: {e}")
        return ""

def generate_output_filename(original_file, plagiarized_file, output_file):
    """
    生成带时间戳的输出文件名
    """
    # 获取当前时间戳
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 提取文件名（不含路径和扩展名）
    orig_name = os.path.splitext(os.path.basename(original_file))[0]
    plag_name = os.path.splitext(os.path.basename(plagiarized_file))[0]
    
    # 获取输出目录
    output_dir = os.path.dirname(output_file)
    if not output_dir:
        output_dir = "output"
    
    # 生成新的文件名
    new_filename = f"{orig_name}_vs_{plag_name}_{timestamp}.txt"
    return os.path.join(output_dir, new_filename)

def write_result(file_path, original_file, plagiarized_file, similarity):
    """
    写入结果到文件（包含原文名、抄袭版名和相似度）
    """
    try:
        from .result_formatter import format_output
        
        # 生成带时间戳的文件名
        timestamped_file = generate_output_filename(original_file, plagiarized_file, file_path)
        
        # 格式化输出内容
        output_content = format_output(original_file, plagiarized_file, similarity)
        
        with open(timestamped_file, 'w', encoding='utf-8') as f:
            f.write(output_content)
        
        print(f"结果已保存到: {timestamped_file}")
        return True
    except Exception as e:
        print(f"写入文件失败: {e}")
        return False

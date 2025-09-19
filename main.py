
# 论文查重作业 - 3123004462
# 第一次个人编程作业

import sys
import os
from src.file_utils import read_file, write_result
from src.algorithm import calculate_similarity

def main():
    # 检查命令行参数
    if len(sys.argv) != 4:
        print("用法: python main.py [原文文件] [抄袭版文件] [输出文件]")
        print("例如: python main.py orig.txt copy.txt result.txt")
        sys.exit(1)
    
    original_file = sys.argv[1]
    plagiarized_file = sys.argv[2] 
    output_file = sys.argv[3]
    
    # 检查文件是否存在
    if not os.path.exists(original_file):
        print(f"错误: 原文文件不存在 - {original_file}")
        sys.exit(1)
        
    if not os.path.exists(plagiarized_file):
        print(f"错误: 抄袭版文件不存在 - {plagiarized_file}")
        sys.exit(1)
    
    print(f"原文文件: {original_file}")
    print(f"抄袭版文件: {plagiarized_file}")
    print(f"输出文件: {output_file}")
    
    # 读取文件内容
    print("读取文件...")
    original_text = read_file(original_file)
    plagiarized_text = read_file(plagiarized_file)
    
    if not original_text or not plagiarized_text:
        print("错误: 文件读取失败")
        sys.exit(1)
    
    # 计算相似度
    print("计算相似度...")
    result = calculate_similarity(original_text, plagiarized_text)
    
    # 写入结果
    if write_result(output_file, result):
        print(f"查重完成，相似度: {result:.2f}")
    else:
        print("错误: 结果写入失败")
        sys.exit(1)

if __name__ == "__main__":
    main()

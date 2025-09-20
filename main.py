
# 论文查重作业 - 3123004462
# 第一次个人编程作业

import sys
import os
import time

# 性能优化：简化导入，避免过度优化

def main():
    """
    主函数 - 论文查重系统入口
    按照作业要求：输入输出采用文件输入输出，输出浮点数精确到小数点后两位
    """
    # 记录开始时间，确保5秒内完成
    start_time = time.time()
    
    try:
        # 检查命令行参数
        if len(sys.argv) != 4:
            print("错误: 参数数量不正确")
            print("用法: python main.py [原文文件绝对路径] [抄袭版文件绝对路径] [输出文件绝对路径]")
            sys.exit(1)
        
        original_file = sys.argv[1]
        plagiarized_file = sys.argv[2] 
        output_file = sys.argv[3]
        
        # 验证文件路径
        if not original_file.strip() or not plagiarized_file.strip() or not output_file.strip():
            print("错误: 文件路径不能为空")
            sys.exit(1)
        
        # 验证是否为绝对路径
        if not os.path.isabs(original_file):
            print(f"错误: 原文文件路径必须是绝对路径: {original_file}")
            sys.exit(1)
        if not os.path.isabs(plagiarized_file):
            print(f"错误: 抄袭版文件路径必须是绝对路径: {plagiarized_file}")
            sys.exit(1)
        if not os.path.isabs(output_file):
            print(f"错误: 输出文件路径必须是绝对路径: {output_file}")
            sys.exit(1)
        
        # 读取文件内容
        try:
            from src.file_utils import read_file
            
            original_text = read_file(original_file)
            plagiarized_text = read_file(plagiarized_file)
        except FileNotFoundError as e:
            print(f"错误: 文件不存在 - {e}")
            sys.exit(1)
        except PermissionError as e:
            print(f"错误: 文件权限不足 - {e}")
            sys.exit(1)
        except IsADirectoryError as e:
            print(f"错误: 路径是目录而非文件 - {e}")
            sys.exit(1)
        except UnicodeDecodeError as e:
            print(f"错误: 文件编码无法识别 - {e}")
            sys.exit(1)
        except ValueError as e:
            print(f"错误: 文件内容无效 - {e}")
            sys.exit(1)
        except Exception as e:
            print(f"错误: 文件读取失败 - {e}")
            sys.exit(1)
        
        if not original_text or not plagiarized_text:
            print("错误: 文件内容为空或读取失败")
            sys.exit(1)
        
        # 计算相似度
        try:
            from src.algorithm import calculate_similarity
            
            result = calculate_similarity(original_text, plagiarized_text)
                
        except TypeError as e:
            print(f"错误: 类型错误 - {e}")
            sys.exit(1)
        except ValueError as e:
            print(f"错误: 计算错误 - {e}")
            sys.exit(1)
        except Exception as e:
            print(f"错误: 相似度计算失败 - {e}")
            sys.exit(1)
        
        # 写入结果（只输出相似度数值，精确到小数点后两位）
        try:
            from src.file_utils import write_result
            
            if write_result(output_file, original_file, plagiarized_file, result):
                # 检查是否超时（5秒限制）
                elapsed_time = time.time() - start_time
                if elapsed_time > 5.0:
                    print(f"错误: 程序运行超时 ({elapsed_time:.2f}秒)，超过5秒限制")
                    sys.exit(1)
            else:
                print("错误: 结果写入失败")
                sys.exit(1)
        except PermissionError as e:
            print(f"错误: 输出权限不足 - {e}")
            sys.exit(1)
        except OSError as e:
            print(f"错误: 系统错误 - {e}")
            sys.exit(1)
        except ValueError as e:
            print(f"错误: 参数错误 - {e}")
            sys.exit(1)
        except Exception as e:
            print(f"错误: 结果保存失败 - {e}")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("错误: 程序被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"错误: 程序运行错误 - {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

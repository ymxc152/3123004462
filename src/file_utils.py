# 文件处理工具模块

import os
import chardet
from datetime import datetime

def read_file(file_path):
    """
    读取文件内容，支持多种编码格式自动检测
    
    Args:
        file_path (str): 文件路径
        
    Returns:
        str: 文件内容，失败时返回空字符串
        
    Raises:
        FileNotFoundError: 文件不存在
        PermissionError: 文件权限不足
        IsADirectoryError: 路径是目录而非文件
        UnicodeDecodeError: 文件编码无法识别
    """
    # 检查文件是否存在
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    # 检查是否为目录
    if os.path.isdir(file_path):
        raise IsADirectoryError(f"路径是目录而非文件: {file_path}")
    
    # 检查文件权限
    if not os.access(file_path, os.R_OK):
        raise PermissionError(f"文件读取权限不足: {file_path}")
    
    # 检查文件大小（避免读取过大的文件，确保内存不超过2048MB）
    file_size = os.path.getsize(file_path)
    if file_size > 100 * 1024 * 1024:  # 100MB限制，确保内存使用不超过2048MB
        raise ValueError(f"文件过大 ({file_size / 1024 / 1024:.1f}MB)，超过100MB限制")
    
    # 尝试多种编码方式读取文件
    encodings = ['utf-8', 'gbk', 'gb2312', 'big5', 'latin-1']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
                # 检查文件是否为空
                if not content.strip():
                    print(f"警告: 文件为空或只包含空白字符: {file_path}")
                return content
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"使用编码 {encoding} 读取文件失败: {e}")
            continue
    
    # 如果所有编码都失败，尝试自动检测编码
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            detected = chardet.detect(raw_data)
            if detected['encoding'] and detected['confidence'] > 0.7:
                with open(file_path, 'r', encoding=detected['encoding']) as f:
                    content = f.read()
                    print(f"使用自动检测的编码 {detected['encoding']} 成功读取文件")
                    return content
    except Exception as e:
        print(f"自动检测编码失败: {e}")
    
    # 所有方法都失败
    raise UnicodeDecodeError("无法识别文件编码，请检查文件格式")

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
    写入结果到文件（按照作业要求，只输出相似度数值）
    
    Args:
        file_path (str): 输出文件路径
        original_file (str): 原文文件路径（用于日志记录）
        plagiarized_file (str): 抄袭版文件路径（用于日志记录）
        similarity (float): 相似度值
        
    Returns:
        bool: 写入成功返回True，失败返回False
        
    Raises:
        ValueError: 相似度值无效
        PermissionError: 输出目录权限不足
        OSError: 磁盘空间不足或其他系统错误
    """
    # 验证相似度值
    if not isinstance(similarity, (int, float)):
        raise ValueError(f"相似度值必须是数字，当前类型: {type(similarity)}")
    
    if similarity < 0 or similarity > 1:
        raise ValueError(f"相似度值必须在0-1之间，当前值: {similarity}")
    
    try:
        # 检查输出目录是否存在，不存在则创建
        output_dir = os.path.dirname(file_path)
        if output_dir and not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir, exist_ok=True)
                print(f"创建输出目录: {output_dir}")
            except PermissionError:
                raise PermissionError(f"无法创建输出目录，权限不足: {output_dir}")
            except OSError as e:
                raise OSError(f"创建输出目录失败: {e}")
        
        # 检查输出目录的写入权限
        if not os.access(output_dir if output_dir else '.', os.W_OK):
            raise PermissionError(f"输出目录写入权限不足: {output_dir}")
        
        # 按照作业要求，只输出相似度数值（保留两位小数）
        output_content = f"{similarity:.2f}"
        
        # 检查磁盘空间（简单检查）
        try:
            statvfs = os.statvfs(output_dir if output_dir else '.')
            free_space = statvfs.f_frsize * statvfs.f_bavail
            if free_space < 1024 * 1024:  # 至少需要1MB空间
                print(f"警告: 磁盘空间不足，剩余 {free_space / 1024 / 1024:.1f}MB")
        except (OSError, AttributeError):
            # Windows系统或无法获取磁盘信息时跳过检查
            pass
        
        # 写入文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(output_content)
        
        print(f"结果已保存到: {file_path}")
        return True
        
    except PermissionError as e:
        print(f"权限错误: {e}")
        return False
    except OSError as e:
        print(f"系统错误: {e}")
        return False
    except ValueError as e:
        print(f"参数错误: {e}")
        return False
    except Exception as e:
        print(f"写入文件失败: {e}")
        return False

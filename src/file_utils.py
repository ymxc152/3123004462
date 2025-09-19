# 文件处理工具模块

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

def write_result(file_path, result):
    """
    写入结果到文件
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"{result:.2f}")
        return True
    except Exception as e:
        print(f"写入文件失败: {e}")
        return False

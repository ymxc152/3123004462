
"""
批量测试文件
测试所有老师提供的测试数据
"""

import sys
import os
import time
import json
from datetime import datetime

# 设置编码
os.environ['PYTHONIOENCODING'] = 'utf-8'

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def run_batch_tests():
    """运行批量测试"""
    print("开始批量测试...")
    print("-" * 50)
    
    from src.algorithm import calculate_similarity
    from src.file_utils import read_file
    
    # 测试数据文件
    test_files = [
        ("orig.txt", "orig_0.8_add.txt", "添加内容测试"),
        ("orig.txt", "orig_0.8_del.txt", "删除内容测试"),
        ("orig.txt", "orig_0.8_dis_1.txt", "轻微修改测试"),
        ("orig.txt", "orig_0.8_dis_10.txt", "中等修改测试"),
        ("orig.txt", "orig_0.8_dis_15.txt", "较大修改测试")
    ]
    
    results = []
    
    for orig_file, test_file, test_name in test_files:
        print(f"测试: {test_name}")
        
        orig_path = f"data/{orig_file}"
        test_path = f"data/{test_file}"
        
        if not os.path.exists(orig_path) or not os.path.exists(test_path):
            print(f"  文件不存在，跳过: {orig_file} / {test_file}")
            continue
        
        try:
            start_time = time.time()
            
            # 读取文件内容
            orig_text = read_file(orig_path)
            test_text = read_file(test_path)
            
            if not orig_text or not test_text:
                print(f"  文件读取失败")
                continue
            
            # 计算相似度
            similarity = calculate_similarity(orig_text, test_text)
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            result = {
                "test_name": test_name,
                "orig_file": orig_file,
                "test_file": test_file,
                "similarity": similarity,
                "execution_time": execution_time,
                "status": "success"
            }
            
            results.append(result)
            
            print(f"  相似度: {similarity:.3f}, 耗时: {execution_time:.3f}秒")
            
        except Exception as e:
            print(f"  测试异常: {e}")
            results.append({
                "test_name": test_name,
                "orig_file": orig_file,
                "test_file": test_file,
                "similarity": 0.0,
                "execution_time": 0.0,
                "status": "error"
            })
        
        print()
    
    return results

def generate_batch_report(results):
    """生成批量测试报告"""
    print("\n" + "=" * 80)
    print("批量测试报告生成")
    print("=" * 80)
    
    # 创建报告目录
    report_dir = "test_reports"
    os.makedirs(report_dir, exist_ok=True)
    
    # 生成时间戳
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 生成报告数据
    report_data = {
        "timestamp": timestamp,
        "test_time": datetime.now().isoformat(),
        "batch_tests": results,
        "summary": {
            "total_batch_tests": len(results),
            "successful_tests": len([r for r in results if r["status"] == "success"]),
            "failed_tests": len([r for r in results if r["status"] != "success"]),
            "overall_status": "success" if all(test["status"] == "success" for test in results) else "failed"
        }
    }
    
    # 保存JSON报告
    json_path = f"{report_dir}/batch_test_report_{timestamp}.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)
    
    # 生成HTML报告
    html_path = f"{report_dir}/batch_test_report_{timestamp}.html"
    from src.report_generator import generate_html_report
    generate_html_report(report_data, html_path, "批量测试")
    
    print(f"JSON报告: {json_path}")
    print(f"HTML报告: {html_path}")
    
    return report_data

# HTML报告生成已移至 src/report_generator.py

def main():
    """主函数"""
    print("=" * 80)
    print("论文查重系统 - 批量测试")
    print("=" * 80)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 运行批量测试
    results = run_batch_tests()
    
    # 生成报告
    report_data = generate_batch_report(results)
    
    print("\n" + "=" * 80)
    print("批量测试完成!")
    print("=" * 80)
    
    return report_data

if __name__ == '__main__':
    main()

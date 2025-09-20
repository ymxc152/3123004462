
"""
测试运行器
调用所有测试文件并生成综合报告
"""

import sys
import os
import time
import json
from datetime import datetime

# 设置环境变量确保正确的编码
os.environ['PYTHONIOENCODING'] = 'utf-8'

def run_unit_tests():
    """运行单元测试"""
    print(f"\n{'='*60}")
    print("运行 单元测试")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    try:
        # 直接导入并运行单元测试
        from tests.test_algorithm import (
            TestPlagiarismDetection, TestTextProcessor, TestSimilarityCalculator,
            TestFileUtils, TestReportGenerator, TestResultFormatter,
            TestAlgorithmAdvanced, TestTextProcessorAdvanced, TestSimilarityCalculatorAdvanced
        )
        import unittest
        
        # 创建测试套件
        suite = unittest.TestSuite()
        
        # 添加所有测试类
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestPlagiarismDetection))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestTextProcessor))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestSimilarityCalculator))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestFileUtils))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestReportGenerator))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestResultFormatter))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestAlgorithmAdvanced))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestTextProcessorAdvanced))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestSimilarityCalculatorAdvanced))
        
        # 运行测试
        runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
        result = runner.run(suite)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        print(f"\n单元测试 耗时: {execution_time:.2f}秒")
        
        if result.wasSuccessful():
            print("✅ 单元测试 完成!")
            return {
                "test_name": "单元测试",
                "test_file": "tests/test_algorithm.py",
                "status": "success",
                "execution_time": execution_time,
                "tests_run": result.testsRun,
                "failures": len(result.failures),
                "errors": len(result.errors)
            }
        else:
            print("❌ 单元测试 失败!")
            return {
                "test_name": "单元测试",
                "test_file": "tests/test_algorithm.py",
                "status": "failed",
                "execution_time": execution_time,
                "tests_run": result.testsRun,
                "failures": len(result.failures),
                "errors": len(result.errors)
            }
            
    except Exception as e:
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"❌ 单元测试 错误: {e}")
        return {
            "test_name": "单元测试",
            "test_file": "tests/test_algorithm.py",
            "status": "error",
            "execution_time": execution_time,
            "error": str(e)
        }

def run_batch_tests():
    """运行批量测试"""
    print(f"\n{'='*60}")
    print("运行 批量测试")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    try:
        # 直接导入并运行批量测试
        from tests.test_batch import run_batch_tests as batch_test_func, generate_batch_report
        
        # 运行批量测试
        results = batch_test_func()
        
        # 生成报告
        report_data = generate_batch_report(results)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        print(f"\n批量测试 耗时: {execution_time:.2f}秒")
        print("✅ 批量测试 完成!")
        
        return {
            "test_name": "批量测试",
            "test_file": "tests/test_batch.py",
            "status": "success",
            "execution_time": execution_time,
            "tests_run": len(results),
            "successful": len([r for r in results if r['status'] == 'success'])
        }
        
    except Exception as e:
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"❌ 批量测试 错误: {e}")
        return {
            "test_name": "批量测试",
            "test_file": "tests/test_batch.py",
            "status": "error",
            "execution_time": execution_time,
            "error": str(e)
        }


def generate_comprehensive_report(test_results):
    """生成综合测试报告"""
    print("\n" + "=" * 80)
    print("生成综合测试报告")
    print("=" * 80)
    
    # 创建报告目录
    report_dir = "test_reports"
    os.makedirs(report_dir, exist_ok=True)
    
    # 生成时间戳
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 统计信息
    total_tests = len(test_results)
    successful_tests = len([r for r in test_results if r["status"] == "success"])
    failed_tests = len([r for r in test_results if r["status"] == "failed"])
    error_tests = len([r for r in test_results if r["status"] == "error"])
    total_time = sum([r["execution_time"] for r in test_results])
    
    # 生成报告数据
    report_data = {
        "timestamp": timestamp,
        "test_time": datetime.now().isoformat(),
        "test_results": test_results,
        "summary": {
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "failed_tests": failed_tests,
            "error_tests": error_tests,
            "total_execution_time": total_time,
            "overall_status": "success" if failed_tests == 0 and error_tests == 0 else "failed"
        }
    }
    
    # 保存JSON报告
    json_path = f"{report_dir}/comprehensive_test_report_{timestamp}.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)
    
    # 生成HTML报告
    html_path = f"{report_dir}/comprehensive_test_report_{timestamp}.html"
    from src.report_generator import generate_html_report
    generate_html_report(report_data, html_path, "综合测试")
    
    print(f"JSON报告: {json_path}")
    print(f"HTML报告: {html_path}")
    
    return report_data

# HTML报告生成已移至 src/report_generator.py

def main():
    """主函数"""
    print("=" * 80)
    print("论文查重系统 - 综合测试运行器")
    print("=" * 80)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    test_results = []
    
    # 运行所有测试
    test_results.append(run_unit_tests())
    test_results.append(run_batch_tests())
    
    # 生成综合报告
    report_data = generate_comprehensive_report(test_results)
    
    print("\n" + "=" * 80)
    print("所有测试完成!")
    print("=" * 80)
    
    # 输出总结
    total = len(test_results)
    success = len([r for r in test_results if r["status"] == "success"])
    failed = len([r for r in test_results if r["status"] == "failed"])
    error = len([r for r in test_results if r["status"] == "error"])
    
    print(f"总测试数: {total}")
    print(f"成功: {success}")
    print(f"失败: {failed}")
    print(f"错误: {error}")
    print(f"总体状态: {'成功' if failed == 0 and error == 0 else '失败'}")
    
    return report_data

if __name__ == '__main__':
    main()
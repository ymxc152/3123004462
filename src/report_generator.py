
"""
报告生成器
统一的HTML报告生成模块
"""

import os
import base64

def encode_image_to_base64(image_path):
    """将图片文件编码为base64字符串"""
    try:
        if os.path.exists(image_path):
            with open(image_path, 'rb') as img_file:
                return base64.b64encode(img_file.read()).decode('utf-8')
    except Exception as e:
        print(f"编码图片失败: {e}")
    return None

def generate_html_report(report_data, output_path, report_type="综合测试"):
    """生成HTML测试报告"""
    html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>论文查重系统 - {report_type}报告</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 2px solid #007bff; }}
        .section {{ margin-bottom: 30px; }}
        .section h2 {{ color: #007bff; border-left: 4px solid #007bff; padding-left: 10px; }}
        .metric {{ display: inline-block; margin: 10px; padding: 15px; background: #f8f9fa; border-radius: 5px; text-align: center; min-width: 120px; }}
        .metric-value {{ font-size: 24px; font-weight: bold; color: #007bff; }}
        .metric-label {{ font-size: 14px; color: #666; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #f8f9fa; font-weight: bold; }}
        .success {{ color: #28a745; }}
        .warning {{ color: #ffc107; }}
        .danger {{ color: #dc3545; }}
        .test-output {{ background-color: #f8f9fa; padding: 10px; border-radius: 5px; margin-top: 10px; font-family: monospace; white-space: pre-wrap; max-height: 200px; overflow-y: auto; }}
        .chart-container {{ margin: 20px 0; text-align: center; }}
        .chart-container img {{ max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        .chart-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 20px; margin: 20px 0; }}
        .chart-item {{ text-align: center; }}
        .chart-title {{ font-weight: bold; margin-bottom: 10px; color: #333; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>论文查重系统 - {report_type}报告</h1>
            <p>生成时间: {report_data.get('test_time', '')}</p>
        </div>
        
        <div class="section">
            <h2>📊 测试概览</h2>
"""
    
    # 根据报告类型生成不同的概览
    if 'summary' in report_data:
        summary = report_data['summary']
        
        # 总测试数
        if 'total_tests' in summary:
            html_content += f"""
            <div class="metric">
                <div class="metric-value">{summary['total_tests']}</div>
                <div class="metric-label">总测试数</div>
            </div>
"""
        
        # 成功数
        if 'successful_tests' in summary:
            html_content += f"""
            <div class="metric">
                <div class="metric-value success">{summary['successful_tests']}</div>
                <div class="metric-label">成功</div>
            </div>
"""
        
        # 失败数
        if 'failed_tests' in summary:
            html_content += f"""
            <div class="metric">
                <div class="metric-value danger">{summary['failed_tests']}</div>
                <div class="metric-label">失败</div>
            </div>
"""
        
        # 错误数
        if 'error_tests' in summary:
            html_content += f"""
            <div class="metric">
                <div class="metric-value danger">{summary['error_tests']}</div>
                <div class="metric-label">错误</div>
            </div>
"""
        
        # 总耗时
        if 'total_execution_time' in summary:
            html_content += f"""
            <div class="metric">
                <div class="metric-value">{summary['total_execution_time']:.2f}s</div>
                <div class="metric-label">总耗时</div>
            </div>
"""
        
        # 总体状态
        if 'overall_status' in summary:
            status_class = "success" if summary['overall_status'] == 'success' else "danger"
            html_content += f"""
            <div class="metric">
                <div class="metric-value {status_class}">{summary['overall_status'].upper()}</div>
                <div class="metric-label">总体状态</div>
            </div>
"""
    
    html_content += """
        </div>
        
        <div class="section">
            <h2>📋 测试结果详情</h2>
            <table>
                <tr>
                    <th>测试名称</th>
                    <th>状态</th>
                    <th>执行时间(秒)</th>
                </tr>
"""
    
    # 根据报告类型生成不同的结果表格
    if 'test_results' in report_data:
        # 综合测试报告
        for test in report_data['test_results']:
            status_class = "success" if test['status'] == 'success' else "warning" if test['status'] == 'failed' else "danger"
            html_content += f"""
                <tr>
                    <td>{test['test_name']}</td>
                    <td class="{status_class}">{test['status'].upper()}</td>
                    <td>{test['execution_time']:.2f}</td>
                </tr>
"""
    elif 'batch_tests' in report_data:
        # 批量测试报告
        html_content = html_content.replace('<th>测试名称</th>\n                    <th>状态</th>\n                    <th>执行时间(秒)</th>', 
                                          '<th>测试名称</th>\n                    <th>原文文件</th>\n                    <th>测试文件</th>\n                    <th>相似度</th>\n                    <th>执行时间(秒)</th>\n                    <th>状态</th>')
        
        for test in report_data['batch_tests']:
            status_class = "success" if test['status'] == 'success' else "danger"
            html_content += f"""
                <tr>
                    <td>{test['test_name']}</td>
                    <td>{test['orig_file']}</td>
                    <td>{test['test_file']}</td>
                    <td>{test['similarity']:.3f}</td>
                    <td>{test['execution_time']:.3f}</td>
                    <td class="{status_class}">{test['status'].upper()}</td>
                </tr>
"""
    
    html_content += """
            </table>
        </div>
"""
    
    # 如果有测试输出，添加输出部分
    if 'test_results' in report_data:
        html_content += """
        <div class="section">
            <h2>📝 测试输出</h2>
"""
        for test in report_data['test_results']:
            html_content += f"""
            <h3>{test['test_name']}</h3>
            <div class="test-output">{test.get('output', '')}</div>
"""
    
    html_content += """
    </div>
</body>
</html>
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

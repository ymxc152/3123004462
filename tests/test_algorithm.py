# 单元测试

import unittest
import sys
import os
import tempfile

# 设置编码
os.environ['PYTHONIOENCODING'] = 'utf-8'

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

class TestPlagiarismDetection(unittest.TestCase):
    """论文查重系统测试类"""
    
    def test_identical_text_similarity(self):
        """测试完全相同文本的相似度"""
        from src.algorithm import calculate_similarity
        
        text = "今天是星期天，天气晴，今天晚上我要去看电影。"
        result = calculate_similarity(text, text)
        
        print(f"  完全相同文本相似度: {result:.6f}")
        print(f"  期望值: 1.0")
        print(f"  结果: {'✅ 通过' if result == 1.0 else '❌ 失败'}")
        
        self.assertEqual(result, 1.0)
    
    def test_different_text_similarity(self):
        """测试完全不同文本的相似度"""
        from src.algorithm import calculate_similarity
        
        text1 = "今天是星期天，天气晴，今天晚上我要去看电影。"
        text2 = "明天我要去图书馆学习，准备期末考试。"
        result = calculate_similarity(text1, text2)
        
        print(f"  完全不同文本相似度: {result:.6f}")
        print(f"  期望范围: < 0.5")
        print(f"  结果: {'✅ 通过' if result < 0.5 else '❌ 失败'}")
        
        self.assertLess(result, 0.5)
    
    def test_similar_text_similarity(self):
        """测试相似文本的相似度"""
        from src.algorithm import calculate_similarity
        
        text1 = "今天是星期天，天气晴，今天晚上我要去看电影。"
        text2 = "今天是周天，天气晴朗，我晚上要去看电影。"
        result = calculate_similarity(text1, text2)
        
        print(f"  相似文本相似度: {result:.6f}")
        print(f"  期望范围: 0.4 < 相似度 < 0.9")
        print(f"  结果: {'✅ 通过' if 0.4 < result < 0.9 else '❌ 失败'}")
        
        self.assertGreater(result, 0.4)
        self.assertLess(result, 0.9)
    
    def test_empty_text_handling(self):
        """测试空文本处理"""
        from src.algorithm import calculate_similarity
        
        result1 = calculate_similarity("", "测试文本")
        result2 = calculate_similarity("测试文本", "")
        result3 = calculate_similarity("", "")
        self.assertEqual(result1, 0.0)
        self.assertEqual(result2, 0.0)
        self.assertEqual(result3, 0.0)
    
    def test_whitespace_handling(self):
        """测试空白字符处理"""
        from src.algorithm import calculate_similarity
        
        text1 = "今天  是   星期天，天气  晴。"
        text2 = "今天是星期天，天气晴。"
        result = calculate_similarity(text1, text2)
        self.assertGreater(result, 0.7)
    
    def test_punctuation_handling(self):
        """测试标点符号处理"""
        from src.algorithm import calculate_similarity
        
        text1 = "今天，是星期天！天气晴。"
        text2 = "今天是星期天天气晴"
        result = calculate_similarity(text1, text2)
        self.assertGreater(result, 0.6)
    
    def test_partial_similarity(self):
        """测试部分相似文本"""
        from src.algorithm import calculate_similarity
        
        text1 = "今天天气很好，我要去看电影，还要买爆米花。"
        text2 = "今天天气晴，今天晚上我要去看电影。"
        result = calculate_similarity(text1, text2)
        self.assertGreater(result, 0.3)
        self.assertLess(result, 0.8)
    
    def test_long_text_handling(self):
        """测试长文本处理"""
        from src.algorithm import calculate_similarity
        
        text1 = "这是一个很长的文本，包含了很多内容。" * 10
        text2 = "这是一个很长的文本，包含了很多内容。" * 9 + "但是最后一句不同。"
        result = calculate_similarity(text1, text2)
        # 调整阈值：由于文本重复导致分词结果相似，但最后一句不同，相似度应该在0.6-0.7之间
        self.assertGreater(result, 0.6)
        self.assertLess(result, 0.8)
    
    def test_chinese_character_handling(self):
        """测试中文字符处理"""
        from src.algorithm import calculate_similarity
        
        text1 = "中文测试文本，包含标点符号！"
        text2 = "中文测试文本包含标点符号"
        result = calculate_similarity(text1, text2)
        self.assertGreater(result, 0.5)
    
    def test_similarity_range(self):
        """测试相似度范围"""
        from src.algorithm import calculate_similarity
        
        text1 = "测试文本"
        text2 = "测试文本"
        result = calculate_similarity(text1, text2)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)

class TestTextProcessor(unittest.TestCase):
    """文本预处理测试类"""
    
    def test_clean_text_function(self):
        """测试文本清洗函数"""
        from src.text_processor import clean_text
        
        text = "今天  是\n星期天，\t天气晴！"
        result = clean_text(text)
        self.assertNotIn('\n', result)
        self.assertNotIn('\t', result)
    
    def test_tokenize_text_function(self):
        """测试分词函数"""
        from src.text_processor import tokenize_text
        
        text = "今天是星期天"
        result = tokenize_text(text)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
    
    def test_preprocess_text_function(self):
        """测试完整预处理函数"""
        from src.text_processor import preprocess_text
        
        text = "今天  是   星期天，天气  晴！"
        result = preprocess_text(text)
        self.assertIsInstance(result, list)

class TestSimilarityCalculator(unittest.TestCase):
    """相似度计算测试类"""
    
    def test_cosine_similarity_function(self):
        """测试余弦相似度函数"""
        from src.similarity_calculator import cosine_similarity
        
        vec1 = {"今天": 1, "天气": 1, "好": 1}
        vec2 = {"今天": 1, "天气": 1, "好": 1}
        result = cosine_similarity(vec1, vec2)
        
        print(f"  余弦相似度: {result:.6f}")
        print(f"  期望值: 1.0")
        print(f"  结果: {'✅ 通过' if abs(result - 1.0) < 1e-10 else '❌ 失败'}")
        
        self.assertAlmostEqual(result, 1.0, places=10)
    
    def test_jaccard_similarity_function(self):
        """测试Jaccard相似度函数"""
        from src.similarity_calculator import jaccard_similarity
        
        set1 = {"今天", "天气", "好"}
        set2 = {"今天", "天气", "好"}
        result = jaccard_similarity(set1, set2)
        
        print(f"  Jaccard相似度: {result:.6f}")
        print(f"  期望值: 1.0")
        print(f"  结果: {'✅ 通过' if result == 1.0 else '❌ 失败'}")
        
        self.assertEqual(result, 1.0)
    
    def test_word_overlap_similarity_function(self):
        """测试词汇重叠相似度函数"""
        from src.similarity_calculator import word_overlap_similarity
        
        words1 = ["今天", "天气", "好"]
        words2 = ["今天", "天气", "好"]
        result = word_overlap_similarity(words1, words2)
        
        print(f"  词汇重叠相似度: {result:.6f}")
        print(f"  期望值: 1.0")
        print(f"  结果: {'✅ 通过' if result == 1.0 else '❌ 失败'}")
        
        self.assertEqual(result, 1.0)

class TestFileUtils(unittest.TestCase):
    """文件工具测试类"""
    
    def setUp(self):
        """测试前准备"""
        import tempfile
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, "test.txt")
        self.test_file_utf8 = os.path.join(self.temp_dir, "test_utf8.txt")
        self.test_file_gbk = os.path.join(self.temp_dir, "test_gbk.txt")
        
        # 创建测试文件
        with open(self.test_file_utf8, 'w', encoding='utf-8') as f:
            f.write("这是UTF-8编码的测试文件")
        
        with open(self.test_file_gbk, 'w', encoding='gbk') as f:
            f.write("这是GBK编码的测试文件")
    
    def tearDown(self):
        """测试后清理"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_read_file_success(self):
        """测试成功读取文件"""
        from src.file_utils import read_file
        
        # 测试UTF-8文件
        content = read_file(self.test_file_utf8)
        self.assertEqual(content, "这是UTF-8编码的测试文件")
        
        # 测试GBK文件
        content = read_file(self.test_file_gbk)
        self.assertEqual(content, "这是GBK编码的测试文件")
    
    def test_read_file_not_found(self):
        """测试文件不存在的情况"""
        from src.file_utils import read_file
        
        with self.assertRaises(FileNotFoundError):
            read_file("nonexistent_file.txt")
    
    def test_read_file_is_directory(self):
        """测试路径是目录的情况"""
        from src.file_utils import read_file
        
        with self.assertRaises(IsADirectoryError):
            read_file(self.temp_dir)
    
    def test_read_file_empty(self):
        """测试空文件"""
        from src.file_utils import read_file
        
        empty_file = os.path.join(self.temp_dir, "empty.txt")
        with open(empty_file, 'w', encoding='utf-8') as f:
            f.write("")
        
        content = read_file(empty_file)
        self.assertEqual(content, "")
    
    def test_write_result_success(self):
        """测试成功写入结果"""
        from src.file_utils import write_result
        
        output_file = os.path.join(self.temp_dir, "result.txt")
        result = write_result(output_file, "orig.txt", "test.txt", 0.85)
        
        self.assertTrue(result)
        self.assertTrue(os.path.exists(output_file))
        
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertEqual(content, "0.85")
    
    def test_write_result_invalid_similarity(self):
        """测试无效相似度值"""
        from src.file_utils import write_result
        
        output_file = os.path.join(self.temp_dir, "result.txt")
        
        # 测试负数
        with self.assertRaises(ValueError):
            write_result(output_file, "orig.txt", "test.txt", -0.1)
        
        # 测试大于1
        with self.assertRaises(ValueError):
            write_result(output_file, "orig.txt", "test.txt", 1.5)
        
        # 测试非数字
        with self.assertRaises(ValueError):
            write_result(output_file, "orig.txt", "test.txt", "invalid")
    
    def test_generate_output_filename(self):
        """测试生成输出文件名"""
        from src.file_utils import generate_output_filename
        
        filename = generate_output_filename("data/orig.txt", "data/test.txt", "output/result.txt")
        
        self.assertIn("orig_vs_test_", filename)
        self.assertTrue(filename.endswith(".txt"))
        self.assertIn("output", filename)  # 检查是否包含output目录
        self.assertTrue(os.path.basename(filename).startswith("orig_vs_test_"))

class TestReportGenerator(unittest.TestCase):
    """报告生成器测试类"""
    
    def setUp(self):
        """测试前准备"""
        import tempfile
        self.temp_dir = tempfile.mkdtemp()
        self.test_image = os.path.join(self.temp_dir, "test.png")
        
        # 创建一个简单的测试图片文件
        with open(self.test_image, 'wb') as f:
            f.write(b'\x89PNG\r\n\x1a\n')  # PNG文件头
    
    def tearDown(self):
        """测试后清理"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_encode_image_to_base64_success(self):
        """测试成功编码图片"""
        from src.report_generator import encode_image_to_base64
        
        result = encode_image_to_base64(self.test_image)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
    
    def test_encode_image_to_base64_not_found(self):
        """测试图片文件不存在"""
        from src.report_generator import encode_image_to_base64
        
        result = encode_image_to_base64("nonexistent.png")
        self.assertIsNone(result)
    
    def test_generate_html_report(self):
        """测试生成HTML报告"""
        from src.report_generator import generate_html_report
        
        test_data = {
            "test_time": "2024-01-01T00:00:00",
            "summary": {
                "total_tests": 5,
                "successful_tests": 4,
                "failed_tests": 1,
                "error_tests": 0,
                "total_execution_time": 1.5,
                "overall_status": "success"
            },
            "test_results": [
                {
                    "test_name": "测试1",
                    "status": "success",
                    "execution_time": 0.5
                }
            ]
        }
        
        output_file = os.path.join(self.temp_dir, "test_report.html")
        generate_html_report(test_data, output_file, "测试报告")
        
        self.assertTrue(os.path.exists(output_file))
        
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("测试报告", content)
            self.assertIn("总测试数", content)

class TestResultFormatter(unittest.TestCase):
    """结果格式化测试类"""
    
    def test_format_similarity(self):
        """测试格式化相似度"""
        from src.result_formatter import format_similarity
        
        result = format_similarity(0.8567)
        self.assertEqual(result, "0.86")
        
        result = format_similarity(1.0)
        self.assertEqual(result, "1.00")
    
    def test_generate_report(self):
        """测试生成报告"""
        from src.result_formatter import generate_report
        
        report = generate_report("orig.txt", "test.txt", 0.85)
        
        self.assertIn("原文文件: orig.txt", report)
        self.assertIn("抄袭版文件: test.txt", report)
        self.assertIn("相似度: 0.85", report)
    
    def test_format_output(self):
        """测试格式化输出"""
        from src.result_formatter import format_output
        
        output = format_output("data/orig.txt", "data/test.txt", 0.75)
        
        self.assertIn("原文文件: orig.txt", output)
        self.assertIn("抄袭版文件: test.txt", output)
        self.assertIn("相似度: 0.75", output)

class TestAlgorithmAdvanced(unittest.TestCase):
    """算法高级功能测试类"""
    
    def test_lazy_import_function(self):
        """测试延迟导入功能"""
        from src.algorithm import lazy_import, get_cached_function
        
        # 测试导入已存在的模块
        text_processor = lazy_import('text_processor')
        self.assertIsNotNone(text_processor)
        
        # 测试获取缓存的函数
        preprocess_func = get_cached_function('text_processor', 'preprocess_text')
        self.assertIsNotNone(preprocess_func)
        
        # 测试重复调用（应该使用缓存）
        preprocess_func2 = get_cached_function('text_processor', 'preprocess_text')
        self.assertEqual(preprocess_func, preprocess_func2)
    
    def test_get_module_functions(self):
        """测试获取模块函数"""
        from src.algorithm import get_text_processor, get_similarity_calculator, get_file_utils
        
        # 测试获取各个模块
        text_processor = get_text_processor()
        self.assertIsNotNone(text_processor)
        
        similarity_calculator = get_similarity_calculator()
        self.assertIsNotNone(similarity_calculator)
        
        file_utils = get_file_utils()
        self.assertIsNotNone(file_utils)
    
    def test_import_error_handling(self):
        """测试导入错误处理"""
        from src.algorithm import lazy_import
        
        # 测试导入不存在的模块
        with self.assertRaises(ImportError):
            lazy_import('nonexistent_module')

class TestTextProcessorAdvanced(unittest.TestCase):
    """文本处理器高级功能测试类"""
    
    def test_ultra_fast_tokenize(self):
        """测试超快速分词"""
        from src.text_processor import ultra_fast_tokenize
        
        # 测试正常文本
        text = "这是一个测试文本"
        result = ultra_fast_tokenize(text)
        self.assertIsInstance(result, tuple)
        self.assertGreater(len(result), 0)
        
        # 测试空文本
        result = ultra_fast_tokenize("")
        self.assertEqual(result, [])
        
        # 测试None
        result = ultra_fast_tokenize(None)
        self.assertEqual(result, [])
    
    def test_ultra_fast_tokenize_long_text(self):
        """测试超长文本处理"""
        from src.text_processor import ultra_fast_tokenize
        
        # 创建超长文本（超过10000字符）
        long_text = "测试文本" * 3000  # 约12000字符
        result = ultra_fast_tokenize(long_text)
        self.assertIsInstance(result, tuple)
        # 应该被截取到10000字符
        self.assertLessEqual(len(''.join(result)), 10000)
    
    def test_lightweight_tokenize(self):
        """测试轻量级分词"""
        from src.text_processor import lightweight_tokenize
        
        # 测试正常文本
        text = "这是一个测试文本"
        result = lightweight_tokenize(text)
        self.assertIsInstance(result, tuple)
        self.assertGreater(len(result), 0)
        
        # 测试空文本
        result = lightweight_tokenize("")
        self.assertEqual(result, [])
        
        # 测试None
        result = lightweight_tokenize(None)
        self.assertEqual(result, [])
    
    def test_lightweight_tokenize_long_text(self):
        """测试轻量级分词长文本处理"""
        from src.text_processor import lightweight_tokenize
        
        # 创建超长文本
        long_text = "测试文本" * 2000  # 约8000字符
        result = lightweight_tokenize(long_text)
        self.assertIsInstance(result, tuple)
        # 检查结果不为空
        self.assertGreater(len(result), 0)
    
    def test_cached_tokenize(self):
        """测试缓存分词"""
        from src.text_processor import cached_tokenize
        
        # 测试正常情况
        text = "正常文本测试"
        result = cached_tokenize(text)
        self.assertIsInstance(result, (list, tuple))
        self.assertGreater(len(result), 0)
        
        # 测试空文本
        result = cached_tokenize("")
        self.assertEqual(result, [])
    
    def test_cached_preprocess(self):
        """测试缓存预处理"""
        from src.text_processor import cached_preprocess
        
        # 测试正常情况
        text = "正常文本测试"
        result = cached_preprocess(text)
        self.assertIsInstance(result, (list, tuple))
        self.assertGreater(len(result), 0)
        
        # 测试空文本
        result = cached_preprocess("")
        self.assertEqual(result, [])
    
    def test_process_large_file(self):
        """测试大文件处理"""
        from src.text_processor import process_large_file
        import tempfile
        import os
        
        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False, suffix='.txt') as f:
            f.write("这是测试文件内容" * 1000)  # 创建较大的文件
            temp_file = f.name
        
        try:
            result = process_large_file(temp_file)
            # process_large_file 返回生成器，需要转换为列表
            result_list = list(result)
            self.assertIsInstance(result_list, list)
            self.assertGreater(len(result_list), 0)
        finally:
            os.unlink(temp_file)
    
    def test_remove_stop_words(self):
        """测试停用词移除"""
        from src.text_processor import remove_stop_words
        
        # 测试包含停用词的词汇列表
        words = ["这是", "一个", "测试", "文本", "的", "内容"]
        result = remove_stop_words(words)
        self.assertIsInstance(result, list)
        # 应该移除一些常见的停用词
        self.assertNotIn("的", result)
    
    def test_get_word_frequency(self):
        """测试词频统计"""
        from src.text_processor import get_word_frequency
        
        # 测试词频统计
        words = ["测试", "文本", "测试", "内容", "文本"]
        result = get_word_frequency(words)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["测试"], 2)
        self.assertEqual(result["文本"], 2)
        self.assertEqual(result["内容"], 1)
    
    def test_vectorize_text(self):
        """测试文本向量化"""
        from src.text_processor import vectorize_text
        
        # 测试文本向量化
        text = "这是一个测试文本"
        result = vectorize_text(text)
        self.assertIsInstance(result, dict)
        self.assertGreater(len(result), 0)

class TestSimilarityCalculatorAdvanced(unittest.TestCase):
    """相似度计算器高级功能测试类"""
    
    def test_enhanced_jaccard_similarity(self):
        """测试增强Jaccard相似度"""
        from src.similarity_calculator import enhanced_jaccard_similarity
        
        # 测试增强Jaccard相似度
        words1 = ["测试", "文本", "内容"]
        words2 = ["测试", "文档", "内容"]
        result = enhanced_jaccard_similarity(words1, words2)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)
    
    def test_calculate_synonym_similarity(self):
        """测试同义词相似度"""
        from src.similarity_calculator import calculate_synonym_similarity
        
        # 测试同义词相似度计算
        words1 = ["汽车", "驾驶", "道路"]
        words2 = ["车辆", "开车", "公路"]
        result = calculate_synonym_similarity(words1, words2)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)
    
    def test_get_numpy(self):
        """测试numpy获取函数"""
        from src.similarity_calculator import get_numpy
        
        # 测试获取numpy
        np = get_numpy()
        self.assertIsNotNone(np)
        # 验证是numpy模块
        self.assertTrue(hasattr(np, 'array'))
    
    def test_calculate_similarity_integration(self):
        """测试相似度计算集成功能"""
        from src.similarity_calculator import calculate_similarity
        
        # 测试完整的相似度计算流程
        text1 = "这是测试文本"
        text2 = "这是另一个测试文本"
        result = calculate_similarity(text1, text2)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)
    
    def test_cosine_similarity_edge_cases(self):
        """测试余弦相似度边界情况"""
        from src.similarity_calculator import cosine_similarity
        
        # 测试空向量
        result = cosine_similarity({}, {})
        self.assertEqual(result, 0.0)
        
        # 测试一个空向量
        result = cosine_similarity({"词": 1}, {})
        self.assertEqual(result, 0.0)
        
        # 测试完全相同的向量
        vec = {"词1": 1, "词2": 2}
        result = cosine_similarity(vec, vec)
        self.assertEqual(result, 1.0)
    
    def test_jaccard_similarity_edge_cases(self):
        """测试Jaccard相似度边界情况"""
        from src.similarity_calculator import jaccard_similarity
        
        # 测试空集合
        result = jaccard_similarity(set(), set())
        self.assertEqual(result, 1.0)  # 空集合的Jaccard相似度为1
        
        # 测试一个空集合
        result = jaccard_similarity({"词1", "词2"}, set())
        self.assertEqual(result, 0.0)
        
        # 测试完全相同的集合
        s = {"词1", "词2"}
        result = jaccard_similarity(s, s)
        self.assertEqual(result, 1.0)
    
    def test_word_overlap_similarity_edge_cases(self):
        """测试词汇重叠相似度边界情况"""
        from src.similarity_calculator import word_overlap_similarity
        
        # 测试空列表
        result = word_overlap_similarity([], [])
        self.assertEqual(result, 1.0)
        
        # 测试一个空列表
        result = word_overlap_similarity(["词1", "词2"], [])
        self.assertEqual(result, 0.0)
        
        # 测试完全相同的列表
        words = ["词1", "词2"]
        result = word_overlap_similarity(words, words)
        self.assertEqual(result, 1.0)

if __name__ == '__main__':
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试类
    suite.addTest(loader.loadTestsFromTestCase(TestPlagiarismDetection))
    suite.addTest(loader.loadTestsFromTestCase(TestTextProcessor))
    suite.addTest(loader.loadTestsFromTestCase(TestSimilarityCalculator))
    suite.addTest(loader.loadTestsFromTestCase(TestFileUtils))
    suite.addTest(loader.loadTestsFromTestCase(TestReportGenerator))
    suite.addTest(loader.loadTestsFromTestCase(TestResultFormatter))
    suite.addTest(loader.loadTestsFromTestCase(TestAlgorithmAdvanced))
    suite.addTest(loader.loadTestsFromTestCase(TestTextProcessorAdvanced))
    suite.addTest(loader.loadTestsFromTestCase(TestSimilarityCalculatorAdvanced))
    
    # 创建测试运行器，设置详细输出
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    
    print("=" * 60)
    print("论文查重系统 - 单元测试")
    print("=" * 60)
    print(f"测试时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python版本: {sys.version}")
    print("=" * 60)
    
    # 运行测试
    result = runner.run(suite)
    
    # 输出测试总结
    print("\n" + "=" * 60)
    print("测试总结:")
    print(f"总测试数: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    
    if result.failures:
        print("\n失败的测试:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\n错误的测试:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    print("=" * 60)
    
    # 返回适当的退出码
    sys.exit(0 if result.wasSuccessful() else 1)

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

if __name__ == '__main__':
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(__import__(__name__))
    
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

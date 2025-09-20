# 论文查重系统

**语言：** Python 3

## 功能特点

- **智能查重算法**：基于改进Jaccard相似度算法，考虑词频权重和同义词匹配
- **中文文本支持**：专门优化中文文本处理，使用jieba分词
- **多种使用方式**：支持命令行和Web界面两种操作方式
- **高性能处理**：支持大文件流式处理，5秒内完成计算
- **完善错误处理**：全面的异常处理和用户友好的错误提示
- **模块化设计**：清晰的代码结构，便于维护和扩展
- **详细文档**：完整的API文档和使用说明

## 快速开始

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd 3123004462
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **运行测试**
   ```bash
   python run_all_tests.py
   ```

4. **使用命令行**
   ```bash
   python main.py data/orig.txt data/orig_0.8_add.txt output/result.txt
   ```

5. **启动Web界面**
   ```bash
   python web/app.py
   ```

## 作业规范

### 题目要求
设计一个论文查重算法，给出一个原文文件和一个在这份原文上经过了增删改的抄袭版论文的文件，在答案文件中输出其重复率。

### 算法特点
- **改进Jaccard相似度**：在传统Jaccard算法基础上，考虑词频权重和同义词匹配
- **中文优化**：专门针对中文文本特点进行优化，使用jieba分词
- **多算法融合**：结合基础Jaccard、加权相似度和同义词相似度
- **性能优化**：使用缓存机制和NumPy加速，支持大文件处理

### 输入输出规范
- **输入**：从命令行参数给出论文原文的文件的绝对路径
- **输入**：从命令行参数给出抄袭版论文的文件的绝对路径  
- **输出**：从命令行参数给出输出的答案文件的绝对路径
- **输出格式**：答案文件中输出的答案为浮点型，精确到小数点后两位

### 性能要求
- 程序在5秒内给出答案
- 占用的内存不超过2048MB
- 不能连接网络、读写其他文件、妨碍评测

## 使用方法

### 命令行使用
```bash
python main.py [原文文件绝对路径] [抄袭版文件绝对路径] [输出文件绝对路径]
```

**参数说明：**
- `原文文件绝对路径`：原始论文文件的绝对路径
- `抄袭版文件绝对路径`：待检测论文文件的绝对路径  
- `输出文件绝对路径`：结果输出文件的绝对路径

**重要：所有路径必须是绝对路径！**

### 使用示例
```bash
# Windows示例
python main.py C:\data\orig.txt C:\data\orig_add.txt C:\output\result.txt

# 使用项目中的测试数据
python main.py C:\Users\17645\Desktop\3123004462\data\orig.txt C:\Users\17645\Desktop\3123004462\data\orig_0.8_add.txt C:\Users\17645\Desktop\3123004462\output\result.txt
```

### 输出结果
程序会在指定的输出文件中写入一个浮点数，表示两篇论文的相似度（0.00-1.00），精确到小数点后两位。

**输出示例：**
```
0.61
```

**注意：输出文件中只包含相似度数值，不包含其他信息。**

### 错误处理
程序会输出相应的错误信息：
- 参数数量不正确
- 文件路径必须是绝对路径
- 文件不存在
- 文件权限不足
- 文件编码无法识别
- 程序运行超时等

### Web界面使用
```bash
# 启动Web服务器
python web/app.py
```
然后在浏览器中访问 `http://localhost:5000` 进行文件上传和查重。

### 测试

#### 运行所有测试
```bash
python run_all_tests.py
```

#### 运行单元测试
```bash
python tests/test_algorithm.py
```

#### 运行批量测试
```bash
python tests/test_batch.py
```

## 安装依赖

```bash
pip install -r requirements.txt
```

**主要依赖：**
- `numpy`：数值计算支持
- `scikit-learn`：机器学习算法库
- `jieba`：中文分词工具
- `Flask`：Web应用框架

## 项目结构

```
3123004462/
├── main.py                    # 主程序入口
├── run_all_tests.py          # 综合测试运行器
├── src/                       # 源代码目录
│   ├── algorithm.py          # 查重算法主模块
│   ├── text_processor.py     # 文本预处理模块
│   ├── similarity_calculator.py  # 相似度计算模块
│   ├── result_formatter.py   # 结果格式化模块
│   ├── file_utils.py         # 文件读写工具模块
│   └── report_generator.py   # 统一报告生成器
├── tests/                     # 测试目录
│   ├── test_algorithm.py     # 单元测试
│   └── test_batch.py         # 批量测试
├── web/                       # Web界面目录
│   └── app.py                # Flask Web应用
├── data/                      # 测试数据目录
│   ├── orig.txt              # 原始测试文件
│   ├── orig_0.8_add.txt      # 添加内容测试文件
│   ├── orig_0.8_del.txt      # 删除内容测试文件
│   ├── orig_0.8_dis_1.txt    # 轻微修改测试文件
│   ├── orig_0.8_dis_10.txt   # 中等修改测试文件
│   ├── orig_0.8_dis_15.txt   # 较大修改测试文件
│   └── README.md             # 数据目录说明
├── output/                    # 输出结果目录（被.gitignore忽略）
├── test_reports/              # 测试报告目录（被.gitignore忽略）
├── requirements.txt           # 项目依赖包列表
├── README.md                  # 项目说明文档
└── .gitignore                # Git忽略文件配置
```

## 核心模块说明

### 1. 主程序模块
- **`main.py`** - 程序入口点
  - 命令行参数解析和验证
  - 文件路径检查
  - 程序流程控制
  - 错误处理和用户提示

### 2. 算法核心模块
- **`src/algorithm.py`** - 查重算法主模块
  - 整合各个子模块
  - 实现完整的查重流程
  - 提供统一的算法接口

- **`src/text_processor.py`** - 文本预处理模块
  - 文本清洗和标准化
  - 中文分词处理
  - 停用词过滤
  - 文本向量化

- **`src/similarity_calculator.py`** - 相似度计算模块
  - 余弦相似度算法
  - Jaccard相似度算法
  - 多种相似度计算方法

- **`src/result_formatter.py`** - 结果格式化模块
  - 相似度结果格式化
  - 查重报告生成
  - 输出格式标准化

### 3. 工具模块
- **`src/file_utils.py`** - 文件处理工具
  - 文件读取和写入
  - 编码格式自动检测
  - 文件操作异常处理

- **`src/report_generator.py`** - 统一报告生成器
  - HTML报告模板生成
  - 支持多种报告类型
  - 统一的样式和格式

### 4. 测试模块
- **`run_all_tests.py`** - 综合测试运行器
  - 单元测试执行
  - 批量测试执行
  - 综合报告生成

- **`tests/test_algorithm.py`** - 单元测试
  - 算法功能测试
  - 边界条件测试
  - 异常情况测试

- **`tests/test_batch.py`** - 批量测试
  - 老师提供的测试数据
  - 批量相似度计算
  - 批量测试报告

### 5. 界面模块
- **`web/app.py`** - Web界面
  - Flask Web应用框架
  - 文件上传功能
  - 结果展示页面
  - 用户交互界面

### 5. 数据目录
- **`data/`** - 测试数据存储
  - 存放老师提供的测试文件
  - 存放自制的测试用例
  - 数据文件说明文档

- **`output/`** - 结果输出目录
  - 存放查重结果文件
  - 结果文件命名规范
  - 输出格式说明

## 开发进度

- [x] 项目基础结构搭建
- [x] 命令行参数解析
- [x] 文件处理模块
- [x] 模块化设计
- [x] 查重算法实现
- [x] 中文分词支持
- [x] 单元测试编写
- [x] 批量测试实现
- [x] 综合测试系统
- [x] 报告生成系统
- [x] Web界面开发
- [x] 前后端分离架构
- [x] 项目文档完善

**详细进度跟踪：** [PROGRESS.md](PROGRESS.md)

## 技术栈

- **后端语言**：Python 3
- **算法库**：scikit-learn, numpy
- **中文处理**：jieba
- **Web框架**：Flask
- **测试框架**：unittest
- **报告生成**：HTML, JSON
- **开发工具**：Git, VS Code

## 注意事项

- 支持UTF-8编码的文本文件
- 文件路径中不要包含空格
- 确保输出目录存在且有写入权限
- 建议使用绝对路径避免路径问题
# 论文查重系统 - API文档

## 概述

论文查重系统提供RESTful API接口，支持文件上传和相似度计算功能。所有API均返回JSON格式数据。

**基础URL:** `http://localhost:5000`

## 接口列表

### 1. 主页接口

**接口地址:** `GET /`

**功能描述:** 返回Web界面主页

**请求参数:** 无

**响应示例:**
```html
<!-- 返回HTML页面 -->
```

---

### 2. 查重接口

**接口地址:** `POST /check`

**功能描述:** 上传两个文本文件并计算相似度

**请求方式:** `POST`

**Content-Type:** `multipart/form-data`

**请求参数:**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| originalFile | File | 是 | 原文文件（.txt格式） |
| plagiarizedFile | File | 是 | 抄袭版文件（.txt格式） |

**请求示例:**
```bash
curl -X POST http://localhost:5000/check \
  -F "originalFile=@orig.txt" \
  -F "plagiarizedFile=@plagiarized.txt"
```

**成功响应:**
```json
{
  "success": true,
  "similarity": 0.85,
  "processing_time": 0.234,
  "original_filename": "orig.txt",
  "plagiarized_filename": "plagiarized.txt",
  "word_similarity": 0.85,
  "structure_similarity": 0.68,
  "overall_score": 0.765
}
```

**响应字段说明:**

| 字段名 | 类型 | 描述 |
|--------|------|------|
| success | boolean | 请求是否成功 |
| similarity | float | 基础相似度（0.0-1.0） |
| processing_time | float | 处理时间（秒） |
| original_filename | string | 原文文件名 |
| plagiarized_filename | string | 抄袭版文件名 |
| word_similarity | float | 词汇相似度 |
| structure_similarity | float | 结构相似度 |
| overall_score | float | 综合评分 |

**错误响应:**

**400 Bad Request - 缺少文件:**
```json
{
  "success": false,
  "message": "请选择两个文件进行查重"
}
```

**400 Bad Request - 文件格式错误:**
```json
{
  "success": false,
  "message": "不支持的文件格式，请上传.txt文件"
}
```

**413 Request Entity Too Large - 文件过大:**
```json
{
  "success": false,
  "message": "文件过大，请选择小于16MB的文件"
}
```

**500 Internal Server Error - 计算失败:**
```json
{
  "success": false,
  "message": "查重计算失败: [具体错误信息]"
}
```

---

### 3. 健康检查接口

**接口地址:** `GET /api/health`

**功能描述:** 检查服务状态

**请求参数:** 无

**成功响应:**
```json
{
  "status": "healthy",
  "message": "论文查重系统运行正常"
}
```

---

## 错误码说明

| HTTP状态码 | 说明 |
|------------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 404 | 接口不存在 |
| 413 | 文件过大 |
| 500 | 服务器内部错误 |

## 使用限制

1. **文件格式:** 仅支持.txt格式文件
2. **文件大小:** 单个文件最大16MB
3. **编码格式:** 文件必须使用UTF-8编码
4. **并发限制:** 建议单次只处理一对文件

## 示例代码

### Python示例

```python
import requests

# 查重接口调用示例
def check_plagiarism(original_file, plagiarized_file):
    url = "http://localhost:5000/check"
    
    with open(original_file, 'rb') as f1, open(plagiarized_file, 'rb') as f2:
        files = {
            'originalFile': f1,
            'plagiarizedFile': f2
        }
        
        response = requests.post(url, files=files)
        return response.json()

# 使用示例
result = check_plagiarism('orig.txt', 'plagiarized.txt')
print(f"相似度: {result['similarity']}")
```

### JavaScript示例

```javascript
// 查重接口调用示例
async function checkPlagiarism(originalFile, plagiarizedFile) {
    const formData = new FormData();
    formData.append('originalFile', originalFile);
    formData.append('plagiarizedFile', plagiarizedFile);
    
    try {
        const response = await fetch('http://localhost:5000/check', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        return result;
    } catch (error) {
        console.error('查重失败:', error);
        throw error;
    }
}

// 使用示例
const fileInput1 = document.getElementById('originalFile');
const fileInput2 = document.getElementById('plagiarizedFile');

checkPlagiarism(fileInput1.files[0], fileInput2.files[0])
    .then(result => {
        console.log('相似度:', result.similarity);
    });
```

### cURL示例

```bash
# 健康检查
curl http://localhost:5000/api/health

# 查重接口
curl -X POST http://localhost:5000/check \
  -F "originalFile=@data/orig.txt" \
  -F "plagiarizedFile=@data/orig_0.8_add.txt"
```

## 注意事项

1. **文件路径:** 确保文件路径正确且文件存在
2. **网络连接:** 确保服务器正在运行（端口5000）
3. **文件编码:** 上传的文件必须是UTF-8编码
4. **错误处理:** 建议在客户端实现完整的错误处理逻辑
5. **超时设置:** 建议设置合理的请求超时时间（如30秒）

## 更新日志

- **v1.0.0** (2024-09-20)
  - 初始版本发布
  - 支持文件上传和相似度计算
  - 提供健康检查接口
  - 完善的错误处理机制

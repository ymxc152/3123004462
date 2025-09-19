# 输出结果目录

## 目录说明
此目录用于存放论文查重结果文件。

## 输出格式规范
按照作业要求，每个结果文件只包含一个浮点数，表示相似度：
- 格式：`[0.00-1.00]`
- 精确到小数点后两位
- 例如：`0.61`

## 文件命名
- 直接使用指定的输出文件名
- 不添加时间戳或其他前缀
- 例如：`result.txt`, `result_del.txt`, `result_dis_1.txt`

## 示例文件
```
0.61    # orig.txt vs orig_0.8_add.txt
0.67    # orig.txt vs orig_0.8_del.txt  
0.88    # orig.txt vs orig_0.8_dis_1.txt
0.65    # orig.txt vs orig_0.8_dis_10.txt
0.46    # orig.txt vs orig_0.8_dis_15.txt
```

## 使用说明
- 程序按照作业要求直接写入指定的输出文件
- 输出文件中只包含相似度数值，不包含其他信息
- 所有路径必须使用绝对路径

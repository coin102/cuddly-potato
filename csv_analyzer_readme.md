# 📊 CSV 数据分析工具

一个纯 Python 实现的 CSV 文件分析工具，无需安装第三方库，支持数据统计、类型检测、缺失值分析等功能。

---

## 一、程序功能

- **数据加载**：自动检测编码和分隔符，支持大文件处理
- **数据预览**：显示表格形式的数据预览
- **类型检测**：自动识别整数、浮点数、日期、布尔值、字符串等类型
- **统计分析**：计算每列的非空值、空值率、唯一值数量
- **数值统计**：对数值列计算最小值、最大值、平均值、总和
- **频率分析**：对字符串列统计最常见的值
- **报告导出**：支持导出 JSON 格式的分析报告

---

## 二、运行环境

- **Python 版本**: 3.8+
- **依赖库**: 仅使用 Python 标准库
- **操作系统**: Windows / macOS / Linux

---

## 三、使用方法

### 基本用法

```bash
python csv_analyzer.py <csv文件路径>
```

### 命令行参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `csv_file` | CSV 文件路径（必填） | `data.csv` |
| `-p, --preview` | 预览行数（默认 5） | `-p 10` |
| `-e, --export` | 导出 JSON 报告 | `-e report.json` |
| `--no-preview` | 不显示数据预览 | `--no-preview` |
| `-v, --version` | 显示版本信息 | `-v` |

### 使用示例

```bash
# 基本分析
python csv_analyzer.py sample_data.csv

# 预览前 10 行
python csv_analyzer.py sample_data.csv -p 10

# 导出分析报告
python csv_analyzer.py sample_data.csv -e analysis_report.json

# 不显示预览，只显示统计
python csv_analyzer.py sample_data.csv --no-preview

# 组合使用
python csv_analyzer.py sample_data.csv -p 3 -e report.json
```

---

## 四、运行效果展示

### 分析示例数据

```bash
python csv_analyzer.py sample_data.csv
```

**输出结果：**

```
🔍 正在分析数据...

================================================================================
📊 数据摘要
================================================================================
文件路径: sample_data.csv
文件大小: 0.00 MB
总行数: 18
总列数: 7

================================================================================
📋 数据预览（前 5 行）
================================================================================
姓名     | 年龄       | 部门       | 薪资       | 入职日期   | 绩效评分   | 是否在职
----------------------------------------------------------------------------------
张三     | 28         | 技术部     | 15000      | 2021-03-15 | 85         | 是
李四     | 32         | 销售部     | 12000      | 2020-07-20 | 92         | 是
王五     | 25         | 技术部     | 18000      | 2022-01-10 | 78         | 是
赵六     | 35         | 人事部     | 10000      | 2019-11-05 | 88         | 是
钱七     | 29         | 销售部     | 13500      | 2021-09-12 | 95         | 是

... 还有 13 行数据 ...

================================================================================
📈 列统计分析
================================================================================

【姓名】
  数据类型: string
  非空值: 18 / 18
  空值率: 0.0%
  唯一值: 18
  最常见值:
    - 张三: 1 次
    - 李四: 1 次
    - 王五: 1 次

【年龄】
  数据类型: integer
  非空值: 18 / 18
  空值率: 0.0%
  唯一值: 10
  最小值: 24.00
  最大值: 35.00
  平均值: 29.17
  总和: 525.00

【部门】
  数据类型: string
  非空值: 18 / 18
  空值率: 0.0%
  唯一值: 5
  最常见值:
    - 技术部: 6 次
    - 销售部: 5 次
    - 人事部: 3 次

【薪资】
  数据类型: integer
  非空值: 18 / 18
  空值率: 0.0%
  唯一值: 18
  最小值: 9500.00
  最大值: 19500.00
  平均值: 13861.11
  总和: 249500.00

【入职日期】
  数据类型: datetime
  非空值: 18 / 18
  空值率: 0.0%
  唯一值: 18

【绩效评分】
  数据类型: integer
  非空值: 18 / 18
  空值率: 0.0%
  唯一值: 15
  最小值: 75.00
  最大值: 95.00
  平均值: 86.17
  总和: 1551.00

【是否在职】
  数据类型: boolean
  非空值: 18 / 18
  空值率: 0.0%
  唯一值: 1
```

---

## 五、数据类型检测

工具会自动检测以下数据类型：

| 类型 | 说明 | 示例 |
|------|------|------|
| `integer` | 整数 | 123, -456 |
| `float` | 浮点数 | 3.14, -0.5 |
| `datetime` | 日期时间 | 2024-01-15, 2024/01/15 10:30:00 |
| `boolean` | 布尔值 | true/false, yes/no, 1/0, 是/否 |
| `string` | 字符串 | 其他所有文本 |
| `empty` | 全空列 | - |

---

## 六、错误处理

程序内置完善的异常处理机制：

| 错误类型 | 处理方式 |
|----------|----------|
| 文件不存在 | 提示 "文件不存在" |
| 权限不足 | 提示 "没有权限读取文件" |
| 编码错误 | 提示 "文件编码错误，请使用 UTF-8" |
| CSV 格式错误 | 提示具体的格式错误信息 |
| 空文件 | 提示 "CSV 文件为空" |
| 大文件警告 | 超过 100MB 时给出警告 |

---

## 七、JSON 报告格式

导出 JSON 报告示例：

```json
{
  "file_info": {
    "path": "sample_data.csv",
    "size_bytes": 714,
    "size_mb": 0.0
  },
  "data_summary": {
    "total_rows": 18,
    "total_columns": 7,
    "columns": ["姓名", "年龄", "部门", "薪资", "入职日期", "绩效评分", "是否在职"]
  },
  "column_analysis": {
    "姓名": {
      "name": "姓名",
      "type": "string",
      "total_count": 18,
      "non_empty_count": 18,
      "empty_count": 0,
      "unique_count": 18,
      "null_rate": 0.0
    },
    "年龄": {
      "name": "年龄",
      "type": "integer",
      "total_count": 18,
      "non_empty_count": 18,
      "empty_count": 0,
      "unique_count": 10,
      "null_rate": 0.0,
      "min": 24.0,
      "max": 35.0,
      "mean": 29.17,
      "sum": 525.0
    }
  },
  "generated_at": "2024-01-15T10:30:00.000000"
}
```

---

## 八、代码结构

```
csv_analyzer.py
├── CSVAnalyzer 类
│   ├── validate_file()      # 文件验证
│   ├── load_data()          # 数据加载
│   ├── detect_data_type()   # 类型检测
│   ├── analyze_column()     # 单列分析
│   ├── analyze_all_columns() # 全部分析
│   ├── print_preview()      # 数据预览
│   ├── print_summary()      # 摘要输出
│   ├── print_column_stats() # 统计输出
│   └── export_report()      # 报告导出
├── create_parser()          # 参数解析
└── main()                   # 程序入口
```

---

## 九、自定义扩展

### 添加新的数据类型检测

在 `detect_data_type` 方法中添加新的检测逻辑：

```python
def detect_data_type(self, values: List[str]) -> str:
    # ... 现有代码 ...
    
    # 检测邮箱
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if all(re.match(email_pattern, v) for v in non_empty):
        return "email"
    
    # ...
```

### 添加新的统计指标

在 `analyze_column` 方法中添加：

```python
def analyze_column(self, column_name: str) -> Dict[str, Any]:
    # ... 现有代码 ...
    
    # 添加中位数计算
    if stats['type'] in ['integer', 'float']:
        numeric_values.sort()
        mid = len(numeric_values) // 2
        stats['median'] = numeric_values[mid]
    
    return stats
```

---

## 十、文件清单

```
d:\clone\
├── csv_analyzer.py          # 主程序
├── sample_data.csv          # 示例数据
└── csv_analyzer_readme.md   # 使用文档
```

---

**祝您使用愉快！🎉**

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSV 数据分析工具
===============
程序功能：读取 CSV 文件并进行数据统计分析，包括列统计、数据类型检测、缺失值分析等
输入方式：通过命令行参数指定 CSV 文件路径
输出要求：在控制台打印分析结果，支持导出为 JSON 报告
使用库限制：仅使用 Python 标准库（csv, json, argparse, collections 等）
错误处理：处理文件不存在、权限错误、格式错误等异常情况
代码结构：模块化设计，包含完整的注释和文档字符串
运行环境：Python 3.8+
附加要求：支持命令行参数，提供使用示例，包含数据预览功能

使用方法：
    python csv_analyzer.py <csv文件路径> [选项]
    
示例：
    python csv_analyzer.py data.csv
    python csv_analyzer.py data.csv --export report.json
    python csv_analyzer.py data.csv --preview 10
"""

import argparse
import csv
import json
import os
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union


class CSVAnalyzer:
    """CSV 文件分析器类"""
    
    def __init__(self, file_path: str):
        """
        初始化分析器
        
        Args:
            file_path: CSV 文件路径
        """
        self.file_path = Path(file_path)
        self.data: List[Dict[str, str]] = []
        self.headers: List[str] = []
        self.row_count: int = 0
        self.column_stats: Dict[str, Dict[str, Any]] = {}
        self.analysis_report: Dict[str, Any] = {}
    
    def validate_file(self) -> bool:
        """
        验证文件是否可读取
        
        Returns:
            验证是否通过
        """
        if not self.file_path.exists():
            print(f"❌ 错误: 文件不存在 - {self.file_path}")
            return False
        
        if not self.file_path.is_file():
            print(f"❌ 错误: 路径不是文件 - {self.file_path}")
            return False
        
        # 检查文件扩展名
        if self.file_path.suffix.lower() != '.csv':
            print(f"⚠️  警告: 文件扩展名不是 .csv，但会尝试读取")
        
        # 检查文件大小（超过 100MB 给出警告）
        file_size = self.file_path.stat().st_size
        if file_size > 100 * 1024 * 1024:
            print(f"⚠️  警告: 文件较大 ({file_size / 1024 / 1024:.1f} MB)，分析可能需要较长时间")
        
        return True
    
    def load_data(self) -> bool:
        """
        加载 CSV 数据
        
        Returns:
            加载是否成功
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8-sig', newline='') as f:
                # 尝试检测分隔符
                sample = f.read(4096)
                f.seek(0)
                
                # 使用 csv.Sniffer 检测分隔符
                try:
                    dialect = csv.Sniffer().sniff(sample, delimiters=',;\t|')
                except csv.Error:
                    dialect = None
                
                # 读取 CSV
                reader = csv.DictReader(f, dialect=dialect)
                self.headers = reader.fieldnames or []
                self.data = list(reader)
                self.row_count = len(self.data)
                
            if self.row_count == 0:
                print("⚠️  警告: CSV 文件为空或没有数据行")
                return False
            
            if len(self.headers) == 0:
                print("❌ 错误: 无法读取列标题")
                return False
            
            return True
            
        except UnicodeDecodeError:
            print("❌ 错误: 文件编码错误，请确保文件使用 UTF-8 编码")
            return False
        except csv.Error as e:
            print(f"❌ 错误: CSV 格式错误 - {e}")
            return False
        except PermissionError:
            print(f"❌ 错误: 没有权限读取文件 - {self.file_path}")
            return False
        except Exception as e:
            print(f"❌ 错误: 读取文件时发生未知错误 - {e}")
            return False
    
    def detect_data_type(self, values: List[str]) -> str:
        """
        检测列的数据类型
        
        Args:
            values: 列的所有值
            
        Returns:
            数据类型描述
        """
        if not values:
            return "unknown"
        
        # 过滤空值
        non_empty = [v for v in values if v.strip()]
        if not non_empty:
            return "empty"
        
        # 检测是否为整数
        int_count = 0
        for v in non_empty:
            try:
                int(v.replace(',', ''))
                int_count += 1
            except ValueError:
                pass
        
        if int_count == len(non_empty):
            return "integer"
        
        # 检测是否为浮点数
        float_count = 0
        for v in non_empty:
            try:
                float(v.replace(',', ''))
                float_count += 1
            except ValueError:
                pass
        
        if float_count == len(non_empty):
            return "float"
        
        # 检测是否为日期
        date_patterns = [
            '%Y-%m-%d', '%Y/%m/%d', '%d-%m-%Y', '%d/%m/%Y',
            '%Y-%m-%d %H:%M:%S', '%Y/%m/%d %H:%M:%S'
        ]
        date_count = 0
        for v in non_empty[:10]:  # 只检测前10个值
            for pattern in date_patterns:
                try:
                    datetime.strptime(v.strip(), pattern)
                    date_count += 1
                    break
                except ValueError:
                    continue
        
        if date_count >= min(5, len(non_empty)):
            return "datetime"
        
        # 检测是否为布尔值
        bool_values = {'true', 'false', 'yes', 'no', '1', '0', '是', '否'}
        if all(v.lower() in bool_values for v in non_empty):
            return "boolean"
        
        return "string"
    
    def analyze_column(self, column_name: str) -> Dict[str, Any]:
        """
        分析单列数据
        
        Args:
            column_name: 列名
            
        Returns:
            列统计信息字典
        """
        values = [row.get(column_name, '') for row in self.data]
        non_empty = [v for v in values if v.strip()]
        
        stats = {
            'name': column_name,
            'type': self.detect_data_type(values),
            'total_count': len(values),
            'non_empty_count': len(non_empty),
            'empty_count': len(values) - len(non_empty),
            'unique_count': len(set(values)),
            'null_rate': (len(values) - len(non_empty)) / len(values) * 100 if values else 0
        }
        
        # 数值型统计
        if stats['type'] in ['integer', 'float']:
            try:
                numeric_values = [float(v.replace(',', '')) for v in non_empty]
                stats['min'] = min(numeric_values)
                stats['max'] = max(numeric_values)
                stats['mean'] = sum(numeric_values) / len(numeric_values)
                stats['sum'] = sum(numeric_values)
            except (ValueError, TypeError):
                pass
        
        # 字符串统计：最常见值
        if stats['type'] == 'string' and non_empty:
            most_common = Counter(non_empty).most_common(5)
            stats['most_common'] = most_common
        
        return stats
    
    def analyze_all_columns(self):
        """分析所有列"""
        print("🔍 正在分析数据...")
        
        for header in self.headers:
            self.column_stats[header] = self.analyze_column(header)
        
        # 生成分析报告
        self.analysis_report = {
            'file_info': {
                'path': str(self.file_path),
                'size_bytes': self.file_path.stat().st_size,
                'size_mb': round(self.file_path.stat().st_size / 1024 / 1024, 2)
            },
            'data_summary': {
                'total_rows': self.row_count,
                'total_columns': len(self.headers),
                'columns': self.headers
            },
            'column_analysis': self.column_stats,
            'generated_at': datetime.now().isoformat()
        }
    
    def print_preview(self, row_limit: int = 5):
        """
        打印数据预览
        
        Args:
            row_limit: 显示的行数
        """
        print("\n" + "=" * 80)
        print("📋 数据预览（前 {} 行）".format(min(row_limit, self.row_count)))
        print("=" * 80)
        
        # 计算每列的最大宽度
        col_widths = {}
        for header in self.headers:
            values = [str(row.get(header, '')) for row in self.data[:row_limit]]
            col_widths[header] = max(
                len(header),
                max((len(v) for v in values), default=0),
                10
            )
            col_widths[header] = min(col_widths[header], 30)  # 最大宽度限制
        
        # 打印表头
        header_line = " | ".join(
            header[:col_widths[header]].ljust(col_widths[header])
            for header in self.headers
        )
        print(header_line)
        print("-" * len(header_line))
        
        # 打印数据行
        for row in self.data[:row_limit]:
            row_line = " | ".join(
                str(row.get(header, ''))[:col_widths[header]].ljust(col_widths[header])
                for header in self.headers
            )
            print(row_line)
        
        if self.row_count > row_limit:
            print(f"\n... 还有 {self.row_count - row_limit} 行数据 ...")
    
    def print_summary(self):
        """打印数据摘要"""
        print("\n" + "=" * 80)
        print("📊 数据摘要")
        print("=" * 80)
        print(f"文件路径: {self.file_path}")
        print(f"文件大小: {self.analysis_report['file_info']['size_mb']:.2f} MB")
        print(f"总行数: {self.row_count}")
        print(f"总列数: {len(self.headers)}")
        print()
    
    def print_column_stats(self):
        """打印列统计信息"""
        print("\n" + "=" * 80)
        print("📈 列统计分析")
        print("=" * 80)
        
        for header, stats in self.column_stats.items():
            print(f"\n【{header}】")
            print(f"  数据类型: {stats['type']}")
            print(f"  非空值: {stats['non_empty_count']} / {stats['total_count']}")
            print(f"  空值率: {stats['null_rate']:.1f}%")
            print(f"  唯一值: {stats['unique_count']}")
            
            # 数值型额外信息
            if stats['type'] in ['integer', 'float']:
                if 'min' in stats:
                    print(f"  最小值: {stats['min']:.2f}")
                    print(f"  最大值: {stats['max']:.2f}")
                    print(f"  平均值: {stats['mean']:.2f}")
                    print(f"  总和: {stats['sum']:.2f}")
            
            # 字符串最常见值
            if stats['type'] == 'string' and 'most_common' in stats:
                print(f"  最常见值:")
                for value, count in stats['most_common'][:3]:
                    print(f"    - {value}: {count} 次")
    
    def export_report(self, output_path: str):
        """
        导出分析报告为 JSON
        
        Args:
            output_path: 输出文件路径
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.analysis_report, f, ensure_ascii=False, indent=2)
            print(f"\n✅ 报告已导出: {output_path}")
        except PermissionError:
            print(f"❌ 错误: 没有权限写入文件 - {output_path}")
        except Exception as e:
            print(f"❌ 错误: 导出报告失败 - {e}")
    
    def run(self, preview_rows: int = 5, export_path: Optional[str] = None):
        """
        运行完整分析流程
        
        Args:
            preview_rows: 预览行数，0 表示不预览
            export_path: 导出报告路径，None 表示不导出
            
        Returns:
            分析是否成功
        """
        # 验证文件
        if not self.validate_file():
            return False
        
        # 加载数据
        if not self.load_data():
            return False
        
        # 分析数据
        self.analyze_all_columns()
        
        # 打印结果
        self.print_summary()
        
        if preview_rows > 0:
            self.print_preview(preview_rows)
        
        self.print_column_stats()
        
        # 导出报告
        if export_path:
            self.export_report(export_path)
        
        return True


def create_parser() -> argparse.ArgumentParser:
    """
    创建命令行参数解析器
    
    Returns:
        参数解析器
    """
    parser = argparse.ArgumentParser(
        description='CSV 数据分析工具 - 快速分析 CSV 文件结构和内容',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用示例:
  %(prog)s data.csv                    # 基本分析
  %(prog)s data.csv -p 10              # 预览前10行
  %(prog)s data.csv -e report.json     # 导出 JSON 报告
  %(prog)s data.csv --no-preview       # 不显示数据预览
        '''
    )
    
    parser.add_argument(
        'csv_file',
        help='要分析的 CSV 文件路径'
    )
    
    parser.add_argument(
        '-p', '--preview',
        type=int,
        default=5,
        metavar='N',
        help='预览前 N 行数据 (默认: 5, 设为 0 则不预览)'
    )
    
    parser.add_argument(
        '-e', '--export',
        metavar='FILE',
        help='将分析报告导出为 JSON 文件'
    )
    
    parser.add_argument(
        '--no-preview',
        action='store_true',
        help='不显示数据预览'
    )
    
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )
    
    return parser


def main():
    """程序入口"""
    # 检查 Python 版本
    if sys.version_info < (3, 8):
        print("❌ 错误: 需要 Python 3.8 或更高版本")
        sys.exit(1)
    
    # 解析命令行参数
    parser = create_parser()
    args = parser.parse_args()
    
    # 创建分析器并运行
    analyzer = CSVAnalyzer(args.csv_file)
    
    preview_rows = 0 if args.no_preview else args.preview
    success = analyzer.run(preview_rows, args.export)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

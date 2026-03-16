#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简易计算器
==========
程序功能：实现一个支持基本数学运算、表达式计算和历史记录功能的计算器
输入方式：用户通过命令行输入表达式或选择菜单选项
输出要求：在控制台打印计算结果，支持显示计算历史
使用库限制：仅使用 Python 标准库（math 模块）
错误处理：处理除零错误、无效输入、语法错误等异常情况
代码结构：模块化设计，包含完整的注释和文档字符串
运行环境：Python 3.8+
附加要求：支持命令行参数直接计算、交互式模式、计算历史记录

使用方法：
    python calculator.py                    # 交互式模式
    python calculator.py "2 + 3 * 4"        # 直接计算表达式
    python calculator.py --history          # 显示历史记录

支持运算：
    + 加法      - 减法      * 乘法      / 除法
    // 整除     % 取余      ** 幂运算   () 括号
    以及 math 模块函数：sin, cos, tan, sqrt, log, log10, exp 等
"""

import argparse
import math
import re
import sys
from datetime import datetime
from typing import List, Optional, Tuple


class Calculator:
    """计算器核心类"""
    
    def __init__(self):
        """初始化计算器"""
        self.history: List[dict] = []
        self.max_history = 100  # 最大历史记录数
    
    def evaluate(self, expression: str) -> Tuple[bool, float, str]:
        """
        计算数学表达式
        
        Args:
            expression: 数学表达式字符串
            
        Returns:
            (成功标志, 结果值, 错误信息)
        """
        # 清理表达式
        expression = expression.strip()
        
        if not expression:
            return False, 0.0, "表达式不能为空"
        
        # 预处理表达式：替换数学函数
        processed_expr = self._preprocess_expression(expression)
        
        # 安全检查：只允许合法的字符
        if not self._is_safe_expression(processed_expr):
            return False, 0.0, "表达式包含非法字符"
        
        try:
            # 使用 eval 计算表达式，但限制可用的函数和变量
            safe_dict = {
                'sin': math.sin,
                'cos': math.cos,
                'tan': math.tan,
                'sqrt': math.sqrt,
                'log': math.log,
                'log10': math.log10,
                'exp': math.exp,
                'abs': abs,
                'round': round,
                'max': max,
                'min': min,
                'pow': pow,
                'pi': math.pi,
                'e': math.e,
                'degrees': math.degrees,
                'radians': math.radians,
            }
            
            result = eval(processed_expr, {"__builtins__": {}}, safe_dict)
            
            # 检查结果是否为有效数字
            if not isinstance(result, (int, float)):
                return False, 0.0, "计算结果不是数字"
            
            if math.isinf(result):
                return False, 0.0, "结果溢出（无穷大）"
            
            if math.isnan(result):
                return False, 0.0, "结果无效（非数字）"
            
            return True, float(result), ""
            
        except ZeroDivisionError:
            return False, 0.0, "除零错误"
        except SyntaxError:
            return False, 0.0, "表达式语法错误"
        except NameError as e:
            return False, 0.0, f"未知函数或变量: {str(e)}"
        except Exception as e:
            return False, 0.0, f"计算错误: {str(e)}"
    
    def _preprocess_expression(self, expression: str) -> str:
        """
        预处理表达式，替换特殊符号和函数
        
        Args:
            expression: 原始表达式
            
        Returns:
            处理后的表达式
        """
        # 替换 ^ 为 **（幂运算）
        expr = expression.replace('^', '**')
        
        # 替换中文括号为英文括号
        expr = expr.replace('（', '(').replace('）', ')')
        
        # 处理隐式乘法，如 "2(3+4)" -> "2*(3+4)"
        expr = re.sub(r'(\d)\(', r'\1*(', expr)
        expr = re.sub(r'\)(\d)', r')*\1', expr)
        
        return expr
    
    def _is_safe_expression(self, expression: str) -> bool:
        """
        检查表达式是否安全（只包含允许的字符）
        
        Args:
            expression: 要检查的表达式
            
        Returns:
            是否安全
        """
        # 允许的字符：数字、运算符、括号、空格、字母（用于函数名）
        allowed_pattern = r'^[\d\+\-\*\/\%\(\)\.\,\s\_a-zA-Z]+$'
        
        if not re.match(allowed_pattern, expression):
            return False
        
        # 检查危险关键字
        dangerous_keywords = ['import', 'exec', 'eval', 'compile', 'open', 'file', '__']
        for keyword in dangerous_keywords:
            if keyword in expression.lower():
                return False
        
        return True
    
    def add_to_history(self, expression: str, result: float, success: bool):
        """
        添加记录到历史
        
        Args:
            expression: 表达式
            result: 计算结果
            success: 是否成功
        """
        record = {
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'expression': expression,
            'result': result,
            'success': success
        }
        
        self.history.append(record)
        
        # 限制历史记录数量
        if len(self.history) > self.max_history:
            self.history.pop(0)
    
    def get_history(self, count: Optional[int] = None) -> List[dict]:
        """
        获取历史记录
        
        Args:
            count: 获取最近的记录数，None 表示全部
            
        Returns:
            历史记录列表
        """
        if count is None:
            return self.history.copy()
        return self.history[-count:]
    
    def clear_history(self):
        """清空历史记录"""
        self.history.clear()
    
    def format_number(self, num: float) -> str:
        """
        格式化数字显示
        
        Args:
            num: 数字
            
        Returns:
            格式化后的字符串
        """
        # 如果是整数，显示为整数
        if num == int(num):
            return str(int(num))
        
        # 否则显示为浮点数，最多保留 10 位小数
        formatted = f"{num:.10f}"
        
        # 去除末尾的 0
        formatted = formatted.rstrip('0').rstrip('.')
        
        return formatted


class CalculatorCLI:
    """计算器命令行界面类"""
    
    def __init__(self):
        """初始化 CLI"""
        self.calculator = Calculator()
    
    def clear_screen(self):
        """清屏"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """打印标题"""
        print("=" * 60)
        print("           🧮  简 易 计 算 器  🧮")
        print("=" * 60)
        print()
    
    def print_help(self):
        """打印帮助信息"""
        print("使用说明:")
        print("-" * 60)
        print("基本运算:")
        print("  +  加法        例: 2 + 3")
        print("  -  减法        例: 5 - 2")
        print("  *  乘法        例: 4 * 5")
        print("  /  除法        例: 10 / 2")
        print("  // 整除        例: 10 // 3")
        print("  %  取余        例: 10 % 3")
        print("  ** 幂运算      例: 2 ** 3")
        print()
        print("高级函数:")
        print("  sin(x)    正弦函数      sqrt(x)   平方根")
        print("  cos(x)    余弦函数      log(x)    自然对数")
        print("  tan(x)    正切函数      log10(x)  常用对数")
        print("  abs(x)    绝对值        exp(x)    指数函数")
        print()
        print("常量:")
        print("  pi        圆周率 π")
        print("  e         自然常数 e")
        print()
        print("特殊命令:")
        print("  help      显示帮助")
        print("  history   显示历史记录")
        print("  clear     清屏")
        print("  exit/quit 退出程序")
        print("-" * 60)
        print()
    
    def get_input(self, prompt: str) -> str:
        """
        获取用户输入
        
        Args:
            prompt: 提示信息
            
        Returns:
            用户输入的字符串
        """
        try:
            return input(prompt).strip()
        except KeyboardInterrupt:
            print("\n\n👋 程序已退出")
            sys.exit(0)
    
    def show_history(self):
        """显示计算历史"""
        print("\n📜 计算历史")
        print("-" * 60)
        
        history = self.calculator.get_history()
        
        if not history:
            print("暂无计算记录")
        else:
            for i, record in enumerate(history, 1):
                status = "✓" if record['success'] else "✗"
                result_str = self.calculator.format_number(record['result'])
                print(f"{i:3}. [{record['time']}] {status} {record['expression']} = {result_str}")
        
        print("-" * 60)
        print()
    
    def run(self):
        """运行交互式计算器"""
        self.clear_screen()
        self.print_header()
        self.print_help()
        
        print("💡 提示: 输入 'help' 查看帮助，输入 'exit' 退出\n")
        
        while True:
            try:
                # 获取输入
                user_input = self.get_input(">>> ")
                
                # 处理空输入
                if not user_input:
                    continue
                
                # 处理特殊命令
                cmd = user_input.lower()
                
                if cmd in ['exit', 'quit', 'q']:
                    print("\n👋 感谢使用，再见！")
                    break
                
                elif cmd == 'help':
                    self.print_help()
                    continue
                
                elif cmd == 'history':
                    self.show_history()
                    continue
                
                elif cmd == 'clear':
                    self.clear_screen()
                    self.print_header()
                    continue
                
                elif cmd == 'clear history':
                    self.calculator.clear_history()
                    print("✅ 历史记录已清空\n")
                    continue
                
                # 执行计算
                success, result, error = self.calculator.evaluate(user_input)
                
                # 添加到历史
                self.calculator.add_to_history(user_input, result, success)
                
                # 显示结果
                if success:
                    result_str = self.calculator.format_number(result)
                    print(f"= {result_str}\n")
                else:
                    print(f"❌ 错误: {error}\n")
                
            except Exception as e:
                print(f"❌ 发生错误: {e}\n")


def create_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        description='简易计算器 - 支持基本运算和数学函数',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用示例:
  %(prog)s                    # 交互式模式
  %(prog)s "2 + 3 * 4"        # 直接计算表达式
  %(prog)s "sqrt(16) + pi"    # 使用数学函数
  %(prog)s --history          # 显示历史记录
  %(prog)s --clear-history    # 清空历史记录
        '''
    )
    
    parser.add_argument(
        'expression',
        nargs='?',
        help='要计算的数学表达式（可选）'
    )
    
    parser.add_argument(
        '-H', '--history',
        action='store_true',
        help='显示计算历史记录'
    )
    
    parser.add_argument(
        '--clear-history',
        action='store_true',
        help='清空计算历史记录'
    )
    
    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='强制进入交互式模式'
    )
    
    return parser


def main():
    """程序入口"""
    # 检查 Python 版本
    if sys.version_info < (3, 8):
        print("❌ 错误: 需要 Python 3.8 或更高版本")
        sys.exit(1)
    
    parser = create_parser()
    args = parser.parse_args()
    
    calc = Calculator()
    cli = CalculatorCLI()
    cli.calculator = calc
    
    # 显示历史记录
    if args.history:
        cli.show_history()
        return
    
    # 清空历史记录
    if args.clear_history:
        calc.clear_history()
        print("✅ 历史记录已清空")
        return
    
    # 直接计算表达式
    if args.expression:
        expression = args.expression
        success, result, error = calc.evaluate(expression)
        
        calc.add_to_history(expression, result, success)
        
        if success:
            result_str = calc.format_number(result)
            print(result_str)
        else:
            print(f"错误: {error}", file=sys.stderr)
            sys.exit(1)
        
        # 如果还指定了交互式模式，则继续进入交互式
        if not args.interactive:
            return
    
    # 进入交互式模式
    cli.run()


if __name__ == '__main__':
    main()

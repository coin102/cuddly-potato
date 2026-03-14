#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
密码生成器工具
=============
功能：生成安全、随机的密码，支持自定义长度和字符类型
运行环境：Windows/macOS/Linux，Python 3.6+，无需第三方库
界面：命令行交互式界面

使用方法：
    python password_generator.py
    
功能特点：
    - 支持生成随机密码
    - 可自定义密码长度
    - 可选择包含的字符类型（大写、小写、数字、特殊字符）
    - 密码强度检测
    - 批量生成多个密码
    - 支持保存到文件
"""

import argparse
import secrets
import string
import sys
from typing import List, Optional


class PasswordGenerator:
    """密码生成器类"""
    
    # 字符集定义
    LOWERCASE = string.ascii_lowercase  # 小写字母: abcdefghijklmnopqrstuvwxyz
    UPPERCASE = string.ascii_uppercase  # 大写字母: ABCDEFGHIJKLMNOPQRSTUVWXYZ
    DIGITS = string.digits              # 数字: 0123456789
    SPECIAL = "!@#$%^&*()_+-=[]{}|;:,.<>?"  # 特殊字符
    
    def __init__(self):
        """初始化密码生成器"""
        self.length: int = 12
        self.use_uppercase: bool = True
        self.use_lowercase: bool = True
        self.use_digits: bool = True
        self.use_special: bool = True
        self.exclude_ambiguous: bool = False  # 排除易混淆字符
        
        # 易混淆字符
        self.ambiguous_chars = "0O1lI"
    
    def get_character_pool(self) -> str:
        """
        获取可用的字符池
        
        Returns:
            可用的字符集合字符串
        """
        pool = ""
        
        if self.use_lowercase:
            pool += self.LOWERCASE
        if self.use_uppercase:
            pool += self.UPPERCASE
        if self.use_digits:
            pool += self.DIGITS
        if self.use_special:
            pool += self.SPECIAL
        
        # 排除易混淆字符
        if self.exclude_ambiguous:
            pool = ''.join(c for c in pool if c not in self.ambiguous_chars)
        
        return pool
    
    def generate(self) -> str:
        """
        生成单个密码
        
        Returns:
            生成的密码字符串
        """
        pool = self.get_character_pool()
        
        if not pool:
            raise ValueError("至少选择一种字符类型")
        
        # 确保每种选中的字符类型至少出现一次
        password_chars = []
        
        if self.use_lowercase:
            chars = self.LOWERCASE
            if self.exclude_ambiguous:
                chars = ''.join(c for c in chars if c not in self.ambiguous_chars)
            password_chars.append(secrets.choice(chars))
        
        if self.use_uppercase:
            chars = self.UPPERCASE
            if self.exclude_ambiguous:
                chars = ''.join(c for c in chars if c not in self.ambiguous_chars)
            password_chars.append(secrets.choice(chars))
        
        if self.use_digits:
            chars = self.DIGITS
            if self.exclude_ambiguous:
                chars = ''.join(c for c in chars if c not in self.ambiguous_chars)
            password_chars.append(secrets.choice(chars))
        
        if self.use_special:
            password_chars.append(secrets.choice(self.SPECIAL))
        
        # 填充剩余长度
        remaining_length = self.length - len(password_chars)
        if remaining_length > 0:
            password_chars.extend(secrets.choice(pool) for _ in range(remaining_length))
        
        # 打乱顺序
        import random
        random.shuffle(password_chars)
        
        return ''.join(password_chars)
    
    def generate_batch(self, count: int) -> List[str]:
        """
        批量生成密码
        
        Args:
            count: 生成密码的数量
            
        Returns:
            密码列表
        """
        return [self.generate() for _ in range(count)]
    
    def check_strength(self, password: str) -> dict:
        """
        检测密码强度
        
        Args:
            password: 要检测的密码
            
        Returns:
            包含强度信息的字典
        """
        score = 0
        feedback = []
        
        # 长度评分
        length = len(password)
        if length >= 16:
            score += 4
            feedback.append("✓ 长度优秀")
        elif length >= 12:
            score += 3
            feedback.append("✓ 长度良好")
        elif length >= 8:
            score += 2
            feedback.append("△ 长度一般")
        else:
            score += 1
            feedback.append("✗ 长度过短")
        
        # 字符类型评分
        has_lower = any(c in self.LOWERCASE for c in password)
        has_upper = any(c in self.UPPERCASE for c in password)
        has_digit = any(c in self.DIGITS for c in password)
        has_special = any(c in self.SPECIAL for c in password)
        
        char_types = sum([has_lower, has_upper, has_digit, has_special])
        score += char_types
        
        if has_lower:
            feedback.append("✓ 包含小写字母")
        if has_upper:
            feedback.append("✓ 包含大写字母")
        if has_digit:
            feedback.append("✓ 包含数字")
        if has_special:
            feedback.append("✓ 包含特殊字符")
        
        # 确定强度等级
        if score >= 7:
            strength = "非常强"
            level = 4
        elif score >= 5:
            strength = "强"
            level = 3
        elif score >= 3:
            strength = "中等"
            level = 2
        else:
            strength = "弱"
            level = 1
        
        return {
            'score': score,
            'max_score': 8,
            'strength': strength,
            'level': level,
            'feedback': feedback,
            'length': length,
            'char_types': char_types
        }
    
    def print_strength_bar(self, level: int):
        """
        打印密码强度条
        
        Args:
            level: 强度等级 (1-4)
        """
        bars = ['▓' * i + '░' * (4 - i) for i in range(1, 5)]
        colors = ['\033[91m', '\033[93m', '\033[92m', '\033[92m']  # 红、黄、绿、绿
        reset = '\033[0m'
        
        if sys.platform == 'win32':
            # Windows 命令行可能不支持颜色，使用纯文本
            bar = '█' * level + '░' * (4 - level)
            print(f"强度: {bar}")
        else:
            bar = bars[level - 1]
            print(f"强度: {colors[level - 1]}{bar}{reset}")


class PasswordGeneratorCLI:
    """密码生成器命令行界面类"""
    
    def __init__(self):
        """初始化 CLI"""
        self.generator = PasswordGenerator()
    
    def clear_screen(self):
        """清屏"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """打印标题"""
        print("=" * 60)
        print("           🔐  密 码 生 成 器  🔐")
        print("=" * 60)
        print()
    
    def get_input(self, prompt: str, allow_empty: bool = False) -> str:
        """
        获取用户输入
        
        Args:
            prompt: 提示信息
            allow_empty: 是否允许空输入
            
        Returns:
            用户输入的字符串
        """
        while True:
            try:
                value = input(prompt).strip()
                if not value and not allow_empty:
                    print("⚠️  输入不能为空")
                    continue
                return value
            except KeyboardInterrupt:
                print("\n\n👋 程序已退出")
                sys.exit(0)
    
    def get_integer_input(self, prompt: str, min_val: int, max_val: int, default: int) -> int:
        """
        获取整数输入
        
        Args:
            prompt: 提示信息
            min_val: 最小值
            max_val: 最大值
            default: 默认值
            
        Returns:
            有效的整数
        """
        while True:
            value = self.get_input(prompt, allow_empty=True)
            
            if not value:
                return default
            
            try:
                num = int(value)
                if min_val <= num <= max_val:
                    return num
                else:
                    print(f"⚠️  请输入 {min_val} 到 {max_val} 之间的数字")
            except ValueError:
                print("⚠️  请输入有效的数字")
    
    def get_yes_no_input(self, prompt: str, default: bool = True) -> bool:
        """
        获取是/否输入
        
        Args:
            prompt: 提示信息
            default: 默认值
            
        Returns:
            True/False
        """
        default_str = "Y/n" if default else "y/N"
        
        while True:
            value = self.get_input(f"{prompt} [{default_str}]: ", allow_empty=True)
            
            if not value:
                return default
            
            if value.lower() in ['y', 'yes', '是']:
                return True
            elif value.lower() in ['n', 'no', '否']:
                return False
            else:
                print("⚠️  请输入 y 或 n")
    
    def configure(self):
        """配置生成器参数"""
        self.clear_screen()
        self.print_header()
        
        print("📋 配置密码生成选项")
        print("-" * 60)
        
        # 密码长度
        self.generator.length = self.get_integer_input(
            "密码长度 (4-128, 默认 16): ",
            min_val=4,
            max_val=128,
            default=16
        )
        
        # 字符类型选择
        print("\n选择包含的字符类型:")
        self.generator.use_lowercase = self.get_yes_no_input("包含小写字母", True)
        self.generator.use_uppercase = self.get_yes_no_input("包含大写字母", True)
        self.generator.use_digits = self.get_yes_no_input("包含数字", True)
        self.generator.use_special = self.get_yes_no_input("包含特殊字符", True)
        
        # 检查至少选择了一种字符类型
        if not any([
            self.generator.use_lowercase,
            self.generator.use_uppercase,
            self.generator.use_digits,
            self.generator.use_special
        ]):
            print("⚠️  至少选择一种字符类型，已默认启用小写字母")
            self.generator.use_lowercase = True
        
        # 排除易混淆字符
        self.generator.exclude_ambiguous = self.get_yes_no_input(
            "排除易混淆字符 (0, O, 1, l, I)",
            False
        )
        
        print("\n✅ 配置完成!")
    
    def generate_single(self):
        """生成单个密码"""
        self.clear_screen()
        self.print_header()
        
        password = self.generator.generate()
        strength = self.generator.check_strength(password)
        
        print("🎲 生成的密码:")
        print("-" * 60)
        print(f"\n  {password}\n")
        print("-" * 60)
        
        # 显示强度
        print(f"\n📊 密码强度: {strength['strength']}")
        self.generator.print_strength_bar(strength['level'])
        print(f"评分: {strength['score']}/{strength['max_score']}")
        
        # 显示详细反馈
        print("\n详细分析:")
        for item in strength['feedback']:
            print(f"  {item}")
        
        # 复制到剪贴板（如果可能）
        self.copy_to_clipboard(password)
        
        print()
    
    def generate_multiple(self):
        """生成多个密码"""
        self.clear_screen()
        self.print_header()
        
        count = self.get_integer_input(
            "生成数量 (1-50, 默认 5): ",
            min_val=1,
            max_val=50,
            default=5
        )
        
        print(f"\n🎲 生成 {count} 个密码:")
        print("-" * 60)
        
        passwords = self.generator.generate_batch(count)
        
        for i, pwd in enumerate(passwords, 1):
            strength = self.generator.check_strength(pwd)
            print(f"{i:2}. {pwd:<30} [强度: {strength['strength']}]")
        
        # 询问是否保存
        if self.get_yes_no_input("\n是否保存到文件", False):
            self.save_to_file(passwords)
        
        print()
    
    def copy_to_clipboard(self, text: str):
        """
        尝试复制文本到剪贴板
        
        Args:
            text: 要复制的文本
        """
        try:
            import platform
            
            system = platform.system()
            
            if system == "Windows":
                import subprocess
                subprocess.run(['clip'], input=text.encode('utf-8'), check=True)
                print("\n📋 密码已复制到剪贴板")
            elif system == "Darwin":  # macOS
                import subprocess
                subprocess.run(['pbcopy'], input=text.encode('utf-8'), check=True)
                print("\n📋 密码已复制到剪贴板")
            elif system == "Linux":
                # 尝试使用 xclip 或 xsel
                import subprocess
                try:
                    subprocess.run(['xclip', '-selection', 'clipboard'], 
                                 input=text.encode('utf-8'), check=True)
                    print("\n📋 密码已复制到剪贴板")
                except:
                    pass
        except:
            pass  # 复制失败不显示错误
    
    def save_to_file(self, passwords: List[str]):
        """
        保存密码到文件
        
        Args:
            passwords: 密码列表
        """
        filename = self.get_input("请输入文件名 (默认: passwords.txt): ", allow_empty=True)
        if not filename:
            filename = "passwords.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("# 生成的密码列表\n")
                f.write(f"# 生成时间: {__import__('datetime').datetime.now().isoformat()}\n")
                f.write("#\n\n")
                for i, pwd in enumerate(passwords, 1):
                    strength = self.generator.check_strength(pwd)
                    f.write(f"{i:2}. {pwd}  [强度: {strength['strength']}]\n")
            
            print(f"✅ 密码已保存到: {filename}")
        except Exception as e:
            print(f"❌ 保存失败: {e}")
    
    def check_password_strength(self):
        """检测密码强度"""
        self.clear_screen()
        self.print_header()
        
        password = self.get_input("请输入要检测的密码: ")
        
        if not password:
            print("⚠️  密码不能为空")
            return
        
        strength = self.generator.check_strength(password)
        
        print("\n📊 密码强度分析:")
        print("-" * 60)
        print(f"密码长度: {strength['length']}")
        print(f"字符类型: {strength['char_types']}/4")
        print(f"强度等级: {strength['strength']}")
        self.generator.print_strength_bar(strength['level'])
        print(f"评分: {strength['score']}/{strength['max_score']}")
        
        print("\n详细分析:")
        for item in strength['feedback']:
            print(f"  {item}")
        
        # 改进建议
        print("\n💡 改进建议:")
        suggestions = []
        if strength['length'] < 12:
            suggestions.append("- 增加密码长度至 12 位以上")
        if strength['char_types'] < 3:
            suggestions.append("- 增加更多类型的字符（大小写、数字、特殊字符）")
        
        if suggestions:
            for s in suggestions:
                print(f"  {s}")
        else:
            print("  密码强度很好，无需改进！")
        
        print()
    
    def show_menu(self):
        """显示主菜单"""
        self.clear_screen()
        self.print_header()
        
        print("主菜单:")
        print("-" * 60)
        print("  [1] 生成单个密码")
        print("  [2] 批量生成密码")
        print("  [3] 检测密码强度")
        print("  [4] 配置生成选项")
        print("  [5] 退出")
        print("-" * 60)
        print()
    
    def run(self):
        """运行主程序"""
        try:
            # 首次运行时配置
            self.configure()
            
            while True:
                self.show_menu()
                
                choice = self.get_input("请选择操作 (1-5): ")
                
                if choice == '1':
                    self.generate_single()
                elif choice == '2':
                    self.generate_multiple()
                elif choice == '3':
                    self.check_password_strength()
                elif choice == '4':
                    self.configure()
                elif choice == '5':
                    print("\n👋 感谢使用，再见！")
                    break
                else:
                    print("⚠️  无效选择，请输入 1-5")
                
                input("\n按回车键继续...")
                
        except KeyboardInterrupt:
            print("\n\n👋 程序已退出")


def create_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        description='密码生成器 - 生成安全随机的密码',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用示例:
  %(prog)s                    # 交互式模式
  %(prog)s -l 20              # 生成长度为 20 的密码
  %(prog)s -n 10 -o pwd.txt   # 生成 10 个密码并保存
  %(prog)s --no-special       # 不包含特殊字符
        '''
    )
    
    parser.add_argument(
        '-l', '--length',
        type=int,
        default=16,
        help='密码长度 (默认: 16)'
    )
    
    parser.add_argument(
        '-n', '--count',
        type=int,
        default=1,
        help='生成数量 (默认: 1)'
    )
    
    parser.add_argument(
        '--no-upper',
        action='store_true',
        help='不包含大写字母'
    )
    
    parser.add_argument(
        '--no-lower',
        action='store_true',
        help='不包含小写字母'
    )
    
    parser.add_argument(
        '--no-digits',
        action='store_true',
        help='不包含数字'
    )
    
    parser.add_argument(
        '--no-special',
        action='store_true',
        help='不包含特殊字符'
    )
    
    parser.add_argument(
        '--no-ambiguous',
        action='store_true',
        help='排除易混淆字符'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='输出文件路径'
    )
    
    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='交互式模式'
    )
    
    return parser


def main():
    """程序入口"""
    # 检查 Python 版本
    if sys.version_info < (3, 6):
        print("❌ 错误: 需要 Python 3.6 或更高版本")
        sys.exit(1)
    
    parser = create_parser()
    args = parser.parse_args()
    
    # 交互式模式或无参数时进入交互式界面
    if args.interactive or len(sys.argv) == 1:
        cli = PasswordGeneratorCLI()
        cli.run()
    else:
        # 命令行模式
        generator = PasswordGenerator()
        generator.length = args.length
        generator.use_uppercase = not args.no_upper
        generator.use_lowercase = not args.no_lower
        generator.use_digits = not args.no_digits
        generator.use_special = not args.no_special
        generator.exclude_ambiguous = args.no_ambiguous
        
        # 检查至少选择了一种字符类型
        if not any([
            generator.use_uppercase,
            generator.use_lowercase,
            generator.use_digits,
            generator.use_special
        ]):
            print("❌ 错误: 至少选择一种字符类型")
            sys.exit(1)
        
        # 生成密码
        passwords = generator.generate_batch(args.count)
        
        # 输出
        output_lines = []
        for i, pwd in enumerate(passwords, 1):
            if args.count > 1:
                output_lines.append(f"{i:2}. {pwd}")
            else:
                output_lines.append(pwd)
        
        result = '\n'.join(output_lines)
        
        # 保存到文件或打印
        if args.output:
            try:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(result)
                print(f"✅ 密码已保存到: {args.output}")
            except Exception as e:
                print(f"❌ 保存失败: {e}")
                sys.exit(1)
        else:
            print(result)


if __name__ == '__main__':
    main()

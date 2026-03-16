#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件批量重命名工具
==================
功能：批量重命名文件，支持序号命名、替换字符、添加前缀/后缀等功能
运行环境：Windows/macOS/Linux，无需安装第三方库
界面：命令行交互式界面

使用方法：
    1. 直接运行：python file_renamer.py
    2. 按照提示输入目标文件夹路径
    3. 选择重命名模式
    4. 确认预览结果后执行重命名
"""

import os
import re
import sys
from datetime import datetime
from typing import List, Tuple, Optional


class FileRenamer:
    """文件批量重命名器类"""
    
    def __init__(self):
        """初始化重命名器"""
        self.target_dir = ""
        self.files: List[str] = []
        self.rename_plan: List[Tuple[str, str]] = []
    
    def clear_screen(self):
        """清屏"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title: str):
        """打印标题头"""
        print("=" * 60)
        print(f"  {title}")
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
                    print("⚠️  输入不能为空，请重新输入。")
                    continue
                return value
            except KeyboardInterrupt:
                print("\n\n👋 程序已取消")
                sys.exit(0)
            except Exception as e:
                print(f"⚠️  输入错误: {e}")
    
    def select_directory(self) -> bool:
        """
        选择目标目录
        
        Returns:
            是否成功选择目录
        """
        self.print_header("步骤 1: 选择目标文件夹")
        print("提示: 请输入要处理的文件夹路径")
        print("      或直接按回车使用当前文件夹")
        print()
        
        path = self.get_input("文件夹路径 (默认当前目录): ", allow_empty=True)
        
        # 使用当前目录
        if not path:
            path = os.getcwd()
        
        # 展开用户目录符号 (~)
        path = os.path.expanduser(path)
        
        # 转换为绝对路径
        path = os.path.abspath(path)
        
        # 检查路径是否存在
        if not os.path.exists(path):
            print(f"❌ 错误: 路径不存在 - {path}")
            return False
        
        if not os.path.isdir(path):
            print(f"❌ 错误: 这不是一个文件夹 - {path}")
            return False
        
        self.target_dir = path
        print(f"✅ 已选择文件夹: {path}")
        return True
    
    def scan_files(self, extensions: Optional[List[str]] = None) -> bool:
        """
        扫描目录中的文件
        
        Args:
            extensions: 文件扩展名过滤列表，如 ['.txt', '.jpg']
            
        Returns:
            是否找到文件
        """
        try:
            all_items = os.listdir(self.target_dir)
            
            # 过滤出文件（排除子目录）
            self.files = [
                f for f in all_items 
                if os.path.isfile(os.path.join(self.target_dir, f))
            ]
            
            # 按扩展名过滤
            if extensions:
                extensions = [ext.lower() if ext.startswith('.') else f'.{ext.lower()}' 
                             for ext in extensions]
                self.files = [f for f in self.files 
                             if any(f.lower().endswith(ext) for ext in extensions)]
            
            # 排序
            self.files.sort()
            
            if not self.files:
                print("⚠️  未找到符合条件的文件")
                return False
            
            print(f"📁 找到 {len(self.files)} 个文件")
            return True
            
        except PermissionError:
            print("❌ 错误: 没有权限访问该文件夹")
            return False
        except Exception as e:
            print(f"❌ 扫描文件时出错: {e}")
            return False
    
    def show_files(self):
        """显示文件列表"""
        print("\n文件列表:")
        print("-" * 60)
        for i, filename in enumerate(self.files[:20], 1):
            print(f"  {i:3}. {filename}")
        
        if len(self.files) > 20:
            print(f"  ... 还有 {len(self.files) - 20} 个文件 ...")
        print("-" * 60)
    
    def select_rename_mode(self) -> int:
        """
        选择重命名模式
        
        Returns:
            模式编号 (1-6)
        """
        self.print_header("步骤 2: 选择重命名模式")
        
        modes = [
            ("1", "序号命名", "将文件重命名为 001, 002, 003... 格式"),
            ("2", "添加前缀", "在文件名前添加指定文字"),
            ("3", "添加后缀", "在文件名（不含扩展名）后添加指定文字"),
            ("4", "替换字符", "替换文件名中的指定字符"),
            ("5", "修改扩展名", "批量修改文件扩展名"),
            ("6", "添加日期前缀", "在文件名前添加当前日期"),
        ]
        
        for num, name, desc in modes:
            print(f"  [{num}] {name:12} - {desc}")
        print()
        
        while True:
            choice = self.get_input("请选择模式 (1-6): ")
            if choice in ['1', '2', '3', '4', '5', '6']:
                return int(choice)
            print("⚠️  无效选择，请输入 1-6 之间的数字")
    
    def generate_rename_plan(self, mode: int) -> bool:
        """
        生成重命名计划
        
        Args:
            mode: 重命名模式
            
        Returns:
            是否成功生成计划
        """
        self.rename_plan = []
        
        try:
            if mode == 1:  # 序号命名
                prefix = self.get_input("请输入文件名前缀 (默认: file): ", allow_empty=True) or "file"
                start_num = self.get_input("起始序号 (默认: 1): ", allow_empty=True) or "1"
                try:
                    start_num = int(start_num)
                except ValueError:
                    start_num = 1
                
                digits = len(str(len(self.files) + start_num - 1))
                
                for i, old_name in enumerate(self.files):
                    ext = os.path.splitext(old_name)[1]
                    new_name = f"{prefix}{str(start_num + i).zfill(digits)}{ext}"
                    self.rename_plan.append((old_name, new_name))
            
            elif mode == 2:  # 添加前缀
                prefix = self.get_input("请输入要添加的前缀: ")
                for old_name in self.files:
                    new_name = f"{prefix}{old_name}"
                    self.rename_plan.append((old_name, new_name))
            
            elif mode == 3:  # 添加后缀
                suffix = self.get_input("请输入要添加的后缀: ")
                for old_name in self.files:
                    name, ext = os.path.splitext(old_name)
                    new_name = f"{name}{suffix}{ext}"
                    self.rename_plan.append((old_name, new_name))
            
            elif mode == 4:  # 替换字符
                old_str = self.get_input("请输入要替换的字符: ")
                if not old_str:
                    print("⚠️  要替换的字符不能为空")
                    return False
                new_str = self.get_input("请输入替换后的字符 (可为空): ", allow_empty=True)
                
                for old_name in self.files:
                    new_name = old_name.replace(old_str, new_str)
                    self.rename_plan.append((old_name, new_name))
            
            elif mode == 5:  # 修改扩展名
                new_ext = self.get_input("请输入新的扩展名 (如: txt, jpg): ")
                new_ext = new_ext.lstrip('.')
                
                for old_name in self.files:
                    name, _ = os.path.splitext(old_name)
                    new_name = f"{name}.{new_ext}"
                    self.rename_plan.append((old_name, new_name))
            
            elif mode == 6:  # 添加日期前缀
                date_format = self.get_input("日期格式 (默认: YYYYMMDD): ", allow_empty=True) or "%Y%m%d"
                try:
                    date_str = datetime.now().strftime(date_format)
                except Exception:
                    print("⚠️  日期格式无效，使用默认格式")
                    date_str = datetime.now().strftime("%Y%m%d")
                
                separator = self.get_input("分隔符 (默认: _): ", allow_empty=True) or "_"
                
                for old_name in self.files:
                    new_name = f"{date_str}{separator}{old_name}"
                    self.rename_plan.append((old_name, new_name))
            
            # 检查是否有重复的新文件名
            new_names = [new for _, new in self.rename_plan]
            if len(new_names) != len(set(new_names)):
                print("⚠️  警告: 重命名后会出现重复文件名，请修改规则")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ 生成重命名计划时出错: {e}")
            return False
    
    def preview_rename(self) -> bool:
        """
        预览重命名结果
        
        Returns:
            用户是否确认执行
        """
        self.print_header("步骤 3: 预览重命名结果")
        
        print(f"{'序号':<6} {'原文件名':<30} {'→':<4} {'新文件名'}")
        print("-" * 80)
        
        unchanged_count = 0
        for i, (old_name, new_name) in enumerate(self.rename_plan[:15], 1):
            # 截断长文件名
            old_display = (old_name[:27] + '...') if len(old_name) > 30 else old_name
            new_display = (new_name[:35] + '...') if len(new_name) > 38 else new_name
            
            if old_name == new_name:
                unchanged_count += 1
                print(f"{i:<6} {old_display:<30} {'→':<4} {new_display} (无变化)")
            else:
                print(f"{i:<6} {old_display:<30} {'→':<4} {new_display}")
        
        if len(self.rename_plan) > 15:
            print(f"  ... 还有 {len(self.rename_plan) - 15} 个文件 ...")
        
        if unchanged_count > 0:
            print(f"\n⚠️  有 {unchanged_count} 个文件名将保持不变")
        
        print("-" * 80)
        print()
        
        confirm = self.get_input("确认执行重命名? (yes/no): ").lower()
        return confirm in ['yes', 'y', '是', '确认']
    
    def execute_rename(self) -> bool:
        """
        执行重命名操作
        
        Returns:
            是否全部成功
        """
        self.print_header("步骤 4: 执行重命名")
        
        success_count = 0
        error_count = 0
        error_list = []
        
        for old_name, new_name in self.rename_plan:
            if old_name == new_name:
                continue
            
            old_path = os.path.join(self.target_dir, old_name)
            new_path = os.path.join(self.target_dir, new_name)
            
            try:
                os.rename(old_path, new_path)
                success_count += 1
                print(f"✅ {old_name} → {new_name}")
            except FileExistsError:
                error_count += 1
                error_list.append(f"{old_name}: 目标文件已存在")
                print(f"❌ {old_name}: 目标文件已存在")
            except PermissionError:
                error_count += 1
                error_list.append(f"{old_name}: 权限不足")
                print(f"❌ {old_name}: 权限不足")
            except Exception as e:
                error_count += 1
                error_list.append(f"{old_name}: {e}")
                print(f"❌ {old_name}: {e}")
        
        print()
        print("=" * 60)
        print(f"重命名完成: 成功 {success_count} 个, 失败 {error_count} 个")
        print("=" * 60)
        
        if error_list:
            print("\n错误详情:")
            for error in error_list:
                print(f"  - {error}")
        
        return error_count == 0
    
    def run(self):
        """运行主程序"""
        try:
            self.clear_screen()
            self.print_header("文件批量重命名工具")
            
            # 步骤1: 选择目录
            if not self.select_directory():
                input("\n按回车键退出...")
                return
            
            # 询问是否过滤扩展名
            filter_ext = self.get_input("\n是否按扩展名过滤文件? (yes/no, 默认no): ", 
                                        allow_empty=True).lower()
            extensions = None
            if filter_ext in ['yes', 'y', '是']:
                ext_input = self.get_input("请输入扩展名 (多个用逗号分隔, 如: txt,jpg,png): ")
                extensions = [e.strip() for e in ext_input.split(',') if e.strip()]
            
            # 扫描文件
            if not self.scan_files(extensions):
                input("\n按回车键退出...")
                return
            
            # 显示文件列表
            self.show_files()
            
            # 步骤2: 选择模式并生成计划
            while True:
                mode = self.select_rename_mode()
                if not self.generate_rename_plan(mode):
                    retry = self.get_input("\n是否重新选择模式? (yes/no): ").lower()
                    if retry not in ['yes', 'y', '是']:
                        return
                    continue
                break
            
            # 步骤3: 预览
            if not self.preview_rename():
                print("\n已取消操作")
                input("按回车键退出...")
                return
            
            # 步骤4: 执行
            self.execute_rename()
            
            print("\n✨ 操作完成!")
            input("按回车键退出...")
            
        except KeyboardInterrupt:
            print("\n\n👋 程序已取消")
        except Exception as e:
            print(f"\n❌ 程序出错: {e}")
            input("按回车键退出...")


def main():
    """程序入口"""
    # 检查 Python 版本
    if sys.version_info < (3, 6):
        print("❌ 错误: 需要 Python 3.6 或更高版本")
        sys.exit(1)
    
    # 创建并运行重命名器
    renamer = FileRenamer()
    renamer.run()


if __name__ == "__main__":
    main()

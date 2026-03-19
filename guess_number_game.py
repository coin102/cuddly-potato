#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
猜数字游戏
==========
游戏规则：系统随机生成一个目标数字，玩家通过输入猜测，系统提示"大了"或"小了"，
直到猜中为止。记录猜测次数，支持多轮游戏。

运行环境：Python 3.6+，Windows/macOS/Linux 均可
无需安装第三方库
"""

import random
import sys
from typing import Optional


class GuessNumberGame:
    """猜数字游戏类"""
    
    def __init__(self):
        """初始化游戏"""
        self.target_number: int = 0      # 目标数字
        self.guess_count: int = 0        # 当前轮次猜测次数
        self.min_range: int = 1          # 最小范围
        self.max_range: int = 100        # 最大范围
        self.game_history: list = []     # 游戏历史记录
    
    def clear_screen(self):
        """清屏，兼容 Windows 和 Unix 系统"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_title(self):
        """打印游戏标题"""
        print("=" * 50)
        print("           🎮  猜 数 字 游 戏  🎮")
        print("=" * 50)
        print()
    
    def get_input(self, prompt: str) -> str:
        """
        获取用户输入，处理键盘中断异常
        
        Args:
            prompt: 输入提示文字
            
        Returns:
            用户输入的字符串
        """
        try:
            return input(prompt).strip()
        except KeyboardInterrupt:
            print("\n\n👋 游戏已退出")
            sys.exit(0)
    
    def get_valid_number(self, prompt: str, min_val: int, max_val: int) -> int:
        """
        获取有效的数字输入
        
        Args:
            prompt: 输入提示
            min_val: 最小允许值
            max_val: 最大允许值
            
        Returns:
            有效的整数
        """
        while True:
            user_input = self.get_input(prompt)
            
            # 检查是否为空
            if not user_input:
                print("⚠️  输入不能为空，请重新输入")
                continue
            
            # 检查是否为数字
            if not user_input.lstrip('-').isdigit():
                print("⚠️  请输入有效的数字")
                continue
            
            try:
                number = int(user_input)
                # 检查范围
                if number < min_val or number > max_val:
                    print(f"⚠️  数字必须在 {min_val} 到 {max_val} 之间")
                    continue
                return number
            except ValueError:
                print("⚠️  数字格式错误，请重新输入")
    
    def set_difficulty(self) -> int:
        """
        设置游戏难度，返回范围上限
        
        Returns:
            数字范围上限
        """
        print("请选择难度级别：")
        print("  [1] 简单   (1-50)")
        print("  [2] 中等   (1-100)")
        print("  [3] 困难   (1-500)")
        print("  [4] 地狱   (1-1000)")
        print()
        
        while True:
            choice = self.get_input("请输入选项 (1-4，默认2): ")
            
            # 默认选择中等
            if not choice:
                return 100
            
            if choice == '1':
                return 50
            elif choice == '2':
                return 100
            elif choice == '3':
                return 500
            elif choice == '4':
                return 1000
            else:
                print("⚠️  无效选项，请重新选择")
    
    def generate_target(self, max_range: int) -> int:
        """
        生成随机目标数字
        
        Args:
            max_range: 数字范围上限
            
        Returns:
            随机生成的目标数字
        """
        return random.randint(1, max_range)
    
    def give_hint(self, guess: int) -> str:
        """
        根据猜测给出提示
        
        Args:
            guess: 玩家猜测的数字
            
        Returns:
            提示信息
        """
        if guess > self.target_number:
            return "📉  太大了！往小猜"
        elif guess < self.target_number:
            return "📈  太小了！往大猜"
        else:
            return "🎉  恭喜你，猜对了！"
    
    def play_round(self) -> dict:
        """
        进行一轮游戏
        
        Returns:
            本轮游戏记录字典
        """
        # 设置难度
        self.max_range = self.set_difficulty()
        self.min_range = 1
        self.target_number = self.generate_target(self.max_range)
        self.guess_count = 0
        
        self.clear_screen()
        self.print_title()
        print(f"🎯 游戏开始！数字范围: {self.min_range} - {self.max_range}")
        print("💡 输入 'q' 可随时退出游戏")
        print("-" * 50)
        print()
        
        # 游戏主循环
        while True:
            # 获取玩家猜测
            user_input = self.get_input(f"第 {self.guess_count + 1} 次猜测: ")
            
            # 检查退出命令
            if user_input.lower() == 'q':
                print(f"\n👋 游戏结束，目标数字是: {self.target_number}")
                return {
                    'completed': False,
                    'target': self.target_number,
                    'guesses': self.guess_count
                }
            
            # 验证输入
            if not user_input.lstrip('-').isdigit():
                print("⚠️  请输入数字或 'q' 退出")
                continue
            
            try:
                guess = int(user_input)
            except ValueError:
                print("⚠️  无效的数字格式")
                continue
            
            # 检查范围
            if guess < self.min_range or guess > self.max_range:
                print(f"⚠️  数字超出范围 ({self.min_range}-{self.max_range})")
                continue
            
            # 增加猜测次数
            self.guess_count += 1
            
            # 给出提示
            hint = self.give_hint(guess)
            print(f"   {hint}")
            print()
            
            # 猜对了
            if guess == self.target_number:
                self.show_victory_message()
                return {
                    'completed': True,
                    'target': self.target_number,
                    'guesses': self.guess_count,
                    'range': self.max_range
                }
    
    def show_victory_message(self):
        """显示胜利信息"""
        print("=" * 50)
        print("           🎊  胜 利 ！🎊")
        print("=" * 50)
        print(f"\n🎯 目标数字: {self.target_number}")
        print(f"🔢 猜测次数: {self.guess_count}")
        
        # 评价
        if self.guess_count <= 5:
            rating = "🏆 天才！"
        elif self.guess_count <= 10:
            rating = "⭐ 优秀！"
        elif self.guess_count <= 15:
            rating = "👍 不错！"
        else:
            rating = "💪 继续加油！"
        
        print(f"📊 评价: {rating}")
        print()
    
    def show_statistics(self):
        """显示游戏统计"""
        if not self.game_history:
            return
        
        print("=" * 50)
        print("           📈  游 戏 统 计  📈")
        print("=" * 50)
        
        completed_games = [g for g in self.game_history if g.get('completed')]
        total_games = len(self.game_history)
        
        print(f"\n总游戏次数: {total_games}")
        print(f"完成次数: {len(completed_games)}")
        
        if completed_games:
            avg_guesses = sum(g['guesses'] for g in completed_games) / len(completed_games)
            best_game = min(completed_games, key=lambda x: x['guesses'])
            print(f"平均猜测次数: {avg_guesses:.1f}")
            print(f"最佳记录: {best_game['guesses']} 次 (范围 1-{best_game['range']})")
        
        print()
    
    def ask_play_again(self) -> bool:
        """
        询问是否再来一局
        
        Returns:
            是否继续游戏
        """
        while True:
            choice = self.get_input("是否再来一局? (y/n): ").lower()
            if choice in ['y', 'yes', '是', '好']:
                return True
            elif choice in ['n', 'no', '否', '不']:
                return False
            else:
                print("⚠️  请输入 y 或 n")
    
    def run(self):
        """运行游戏主循环"""
        self.clear_screen()
        
        while True:
            self.print_title()
            
            # 进行一轮游戏
            result = self.play_round()
            self.game_history.append(result)
            
            # 显示统计
            self.show_statistics()
            
            # 询问是否继续
            if not self.ask_play_again():
                print("\n👋 感谢游玩，再见！")
                break
            
            self.clear_screen()


def main():
    """程序入口"""
    # 检查 Python 版本
    if sys.version_info < (3, 6):
        print("❌ 错误: 需要 Python 3.6 或更高版本")
        sys.exit(1)
    
    # 创建游戏实例并运行
    game = GuessNumberGame()
    game.run()


if __name__ == "__main__":
    main()

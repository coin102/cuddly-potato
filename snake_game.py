#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
贪吃蛇游戏 (Snake Game)
=======================
使用 Pygame 库制作的经典贪吃蛇小游戏

安装依赖:
    pip install pygame

运行方式:
    python snake_game.py

操作说明:
    ↑ ↓ ← →  - 控制蛇的移动方向
    C        - 游戏结束后重新开始
    Q        - 游戏结束后退出游戏
    ESC      - 游戏中退出
"""

import sys
import random

# 尝试导入 pygame，如果未安装则给出友好提示
try:
    import pygame
    from pygame.locals import *
except ImportError:
    print("=" * 60)
    print("错误：未找到 Pygame 库！")
    print("=" * 60)
    print("\n请先安装 Pygame：")
    print("    pip install pygame")
    print("\n或者：")
    print("    python -m pip install pygame")
    print("\n安装完成后再次运行本程序。")
    print("=" * 60)
    sys.exit(1)


# ==================== 游戏配置常量 ====================
# 窗口大小
WINDOW_WIDTH = 800      # 窗口宽度（像素）
WINDOW_HEIGHT = 600     # 窗口高度（像素）

# 网格大小（每个格子的大小）
GRID_SIZE = 20          # 每个格子 20x20 像素
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE    # 横向格子数
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE  # 纵向格子数

# 游戏速度（每秒帧数，数值越大速度越快）
FPS = 10

# 颜色定义 (R, G, B)
COLOR_BLACK = (0, 0, 0)           # 黑色 - 背景色
COLOR_WHITE = (255, 255, 255)     # 白色 - 文字颜色
COLOR_GREEN = (0, 255, 0)         # 绿色 - 蛇身颜色
COLOR_DARK_GREEN = (0, 200, 0)    # 深绿色 - 蛇头颜色
COLOR_RED = (255, 0, 0)           # 红色 - 食物颜色
COLOR_GRAY = (128, 128, 128)      # 灰色 - 网格线颜色


class Snake:
    """
    蛇类
    负责管理蛇的位置、移动、绘制和碰撞检测
    """
    
    def __init__(self):
        """
        初始化蛇
        蛇初始位置在屏幕中央，初始长度为3格，向右移动
        """
        # 蛇身由一系列坐标组成，每个坐标是 (x, y) 格子位置
        # 列表第一个元素是蛇头，最后一个元素是蛇尾
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2
        self.body = [
            (start_x, start_y),      # 蛇头
            (start_x - 1, start_y),  # 蛇身第1节
            (start_x - 2, start_y),  # 蛇身第2节
        ]
        
        # 初始移动方向：向右
        self.direction = (1, 0)  # (x方向, y方向)，(1,0)表示向右
        
        # 下一个要移动的方向（用于防止快速按键导致的反向移动）
        self.next_direction = self.direction
        
        # 生长标记：吃到食物后增长的节数
        self.grow_pending = 0
    
    def change_direction(self, new_direction):
        """
        改变蛇的移动方向
        
        Args:
            new_direction: 新方向，格式为 (dx, dy)
                          例如：(1, 0) 向右, (-1, 0) 向左
                               (0, 1) 向下, (0, -1) 向上
        """
        # 防止 180 度转向（不能直接反向移动）
        # 例如：如果当前向右，不能直接向左
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.next_direction = new_direction
    
    def move(self):
        """
        移动蛇
        根据当前方向移动蛇头，并更新蛇身位置
        """
        # 更新当前方向为下一个方向
        self.direction = self.next_direction
        
        # 计算新的蛇头位置
        head_x, head_y = self.body[0]
        new_head = (
            head_x + self.direction[0],
            head_y + self.direction[1]
        )
        
        # 将新蛇头插入到列表最前面
        self.body.insert(0, new_head)
        
        # 如果没有生长标记，则移除蛇尾（保持长度不变）
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()
    
    def grow(self, amount=1):
        """
        增加蛇的长度
        
        Args:
            amount: 增长的节数，默认为1
        """
        self.grow_pending += amount
    
    def check_self_collision(self):
        """
        检查蛇是否撞到自己
        
        Returns:
            如果蛇头与身体任何部分重合，返回 True
        """
        # 蛇头位置
        head = self.body[0]
        # 检查蛇头是否与身体的其他部分重合
        return head in self.body[1:]
    
    def check_wall_collision(self):
        """
        检查蛇是否撞到墙
        
        Returns:
            如果蛇头超出边界，返回 True
        """
        head_x, head_y = self.body[0]
        # 检查是否超出左右边界或上下边界
        return head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT
    
    def get_head_position(self):
        """
        获取蛇头位置
        
        Returns:
            蛇头坐标 (x, y)
        """
        return self.body[0]
    
    def draw(self, surface):
        """
        在屏幕上绘制蛇
        
        Args:
            surface: Pygame 绘图表面
        """
        for i, segment in enumerate(self.body):
            # 计算格子的像素坐标
            rect = pygame.Rect(
                segment[0] * GRID_SIZE,
                segment[1] * GRID_SIZE,
                GRID_SIZE - 1,  # 减1留出间隙，看起来更清晰
                GRID_SIZE - 1
            )
            
            # 蛇头用深绿色，身体用绿色
            if i == 0:
                pygame.draw.rect(surface, COLOR_DARK_GREEN, rect)
            else:
                pygame.draw.rect(surface, COLOR_GREEN, rect)


class Food:
    """
    食物类
    负责管理食物的位置和绘制
    """
    
    def __init__(self):
        """初始化食物，随机生成位置"""
        self.position = (0, 0)
        self.randomize_position()
    
    def randomize_position(self, snake_body=None):
        """
        随机生成食物位置
        
        Args:
            snake_body: 蛇身位置列表，用于避免食物生成在蛇身上
        """
        while True:
            # 随机生成坐标
            self.position = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1)
            )
            
            # 如果提供了蛇身位置，确保食物不在蛇身上
            if snake_body is None or self.position not in snake_body:
                break
    
    def draw(self, surface):
        """
        在屏幕上绘制食物
        
        Args:
            surface: Pygame 绘图表面
        """
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE,
            self.position[1] * GRID_SIZE,
            GRID_SIZE - 1,
            GRID_SIZE - 1
        )
        pygame.draw.rect(surface, COLOR_RED, rect)


class Game:
    """
    游戏主类
    负责管理游戏循环、事件处理和游戏逻辑
    """
    
    def __init__(self):
        """初始化游戏"""
        # 初始化 Pygame
        pygame.init()
        
        # 创建游戏窗口
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("贪吃蛇游戏 - Snake Game")
        
        # 创建时钟对象，用于控制游戏帧率
        self.clock = pygame.time.Clock()
        
        # 初始化字体（用于显示文字）
        self.font_large = pygame.font.SysFont("simhei", 50)  # 大号字体
        self.font_medium = pygame.font.SysFont("simhei", 30)  # 中号字体
        self.font_small = pygame.font.SysFont("simhei", 20)   # 小号字体
        
        # 初始化游戏对象
        self.reset_game()
    
    def reset_game(self):
        """重置游戏状态（开始新游戏）"""
        self.snake = Snake()           # 创建新蛇
        self.food = Food()             # 创建新食物
        self.food.randomize_position(self.snake.body)  # 确保食物不在蛇身上
        self.score = 0                 # 重置分数
        self.game_over = False         # 游戏状态设为进行中
    
    def handle_events(self):
        """
        处理用户输入事件
        返回 False 表示用户想要退出游戏
        """
        for event in pygame.event.get():
            # 处理退出事件（点击窗口关闭按钮）
            if event.type == QUIT:
                return False
            
            # 处理键盘按键事件
            if event.type == KEYDOWN:
                # ESC 键退出游戏
                if event.key == K_ESCAPE:
                    return False
                
                # 游戏结束时的按键处理
                if self.game_over:
                    if event.key == K_c:  # C 键重新开始
                        self.reset_game()
                    elif event.key == K_q:  # Q 键退出
                        return False
                else:
                    # 游戏进行中的方向控制
                    if event.key == K_UP or event.key == K_w:
                        self.snake.change_direction((0, -1))  # 向上
                    elif event.key == K_DOWN or event.key == K_s:
                        self.snake.change_direction((0, 1))   # 向下
                    elif event.key == K_LEFT or event.key == K_a:
                        self.snake.change_direction((-1, 0))  # 向左
                    elif event.key == K_RIGHT or event.key == K_d:
                        self.snake.change_direction((1, 0))   # 向右
        
        return True
    
    def update(self):
        """更新游戏逻辑"""
        if self.game_over:
            return
        
        # 移动蛇
        self.snake.move()
        
        # 检查是否撞墙
        if self.snake.check_wall_collision():
            self.game_over = True
            return
        
        # 检查是否撞到自己
        if self.snake.check_self_collision():
            self.game_over = True
            return
        
        # 检查是否吃到食物
        if self.snake.get_head_position() == self.food.position:
            self.snake.grow(1)  # 蛇增长一节
            self.score += 10    # 增加分数
            # 重新生成食物
            self.food.randomize_position(self.snake.body)
    
    def draw_grid(self):
        """绘制背景网格线（可选，让游戏更美观）"""
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, COLOR_GRAY, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, COLOR_GRAY, (0, y), (WINDOW_WIDTH, y))
    
    def draw_score(self):
        """在屏幕上显示分数"""
        score_text = self.font_medium.render(f"得分: {self.score}", True, COLOR_WHITE)
        self.screen.blit(score_text, (10, 10))
    
    def draw_game_over(self):
        """显示游戏结束画面"""
        # 创建半透明遮罩
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)  # 设置透明度
        overlay.fill(COLOR_BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # 显示"游戏结束"文字
        game_over_text = self.font_large.render("游 戏 结 束", True, COLOR_RED)
        text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        self.screen.blit(game_over_text, text_rect)
        
        # 显示最终得分
        score_text = self.font_medium.render(f"最终得分: {self.score}", True, COLOR_WHITE)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
        self.screen.blit(score_text, score_rect)
        
        # 显示操作提示
        hint_text = self.font_small.render("按 C 重新开始 | 按 Q 退出", True, COLOR_WHITE)
        hint_rect = hint_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80))
        self.screen.blit(hint_text, hint_rect)
    
    def draw(self):
        """绘制游戏画面"""
        # 填充背景色
        self.screen.fill(COLOR_BLACK)
        
        # 绘制网格（可选）
        # self.draw_grid()
        
        # 绘制食物
        self.food.draw(self.screen)
        
        # 绘制蛇
        self.snake.draw(self.screen)
        
        # 显示分数
        self.draw_score()
        
        # 如果游戏结束，显示结束画面
        if self.game_over:
            self.draw_game_over()
        
        # 更新屏幕显示
        pygame.display.flip()
    
    def run(self):
        """
        游戏主循环
        这是游戏的核心循环，持续运行直到游戏结束
        """
        try:
            running = True
            while running:
                # 处理事件
                running = self.handle_events()
                
                # 更新游戏逻辑
                self.update()
                
                # 绘制画面
                self.draw()
                
                # 控制游戏速度
                self.clock.tick(FPS)
            
        except Exception as e:
            # 异常处理：显示错误信息
            print(f"\n游戏发生错误: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            # 清理资源
            pygame.quit()
            print("\n感谢游玩！再见！")


def main():
    """
    程序入口函数
    检查 Python 版本并启动游戏
    """
    # 检查 Python 版本
    if sys.version_info < (3, 6):
        print("错误: 需要 Python 3.6 或更高版本")
        sys.exit(1)
    
    print("=" * 60)
    print("           贪吃蛇游戏 - Snake Game")
    print("=" * 60)
    print("\n操作说明:")
    print("  ↑ ↓ ← →  或  W A S D  - 控制移动方向")
    print("  ESC                    - 退出游戏")
    print("\n游戏结束后:")
    print("  C - 重新开始")
    print("  Q - 退出游戏")
    print("=" * 60)
    print("\n游戏启动中...")
    
    # 创建游戏实例并运行
    game = Game()
    game.run()


# 程序入口点
if __name__ == "__main__":
    main()

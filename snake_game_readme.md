# 🐍 贪吃蛇游戏

使用 Pygame 库制作的经典贪吃蛇小游戏，支持方向键控制、分数统计和游戏重新开始功能。

---

## 一、安装依赖

### 安装 Pygame

```bash
# 使用 pip 安装
pip install pygame

# 或者使用 Python 模块方式安装
python -m pip install pygame

# 如果安装较慢，可以使用国内镜像
pip install pygame -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 验证安装

```bash
python -c "import pygame; print(pygame.__version__)"
```

如果显示版本号（如 `2.5.2`），说明安装成功。

---

## 二、运行游戏

```bash
python snake_game.py
```

---

## 三、游戏操作说明

### 基本操作

| 按键 | 功能 |
|------|------|
| `↑` 上方向键 | 向上移动 |
| `↓` 下方向键 | 向下移动 |
| `←` 左方向键 | 向左移动 |
| `→` 右方向键 | 向右移动 |
| `W` | 向上移动（备用） |
| `S` | 向下移动（备用） |
| `A` | 向左移动（备用） |
| `D` | 向右移动（备用） |
| `ESC` | 退出游戏 |

### 游戏结束后

| 按键 | 功能 |
|------|------|
| `C` | 重新开始游戏 |
| `Q` | 退出游戏 |

---

## 四、游戏规则

1. **控制蛇移动**：使用方向键控制绿色蛇的移动
2. **吃食物**：吃到红色食物后，蛇身变长，得分 +10
3. **游戏结束条件**：
   - 蛇头撞到墙壁
   - 蛇头撞到自己的身体
4. **重新开始**：游戏结束后按 `C` 键可以重新开始

---

## 五、游戏界面

```
┌────────────────────────────────────────┐
│  得分: 50                              │  ← 分数显示
│                                        │
│    🟢                                  │
│    🟢🟢🟢                             │  ← 蛇（绿色）
│          🟢                            │
│                                        │
│              🔴                        │  ← 食物（红色）
│                                        │
│                                        │
│                                        │
└────────────────────────────────────────┘
```

### 游戏结束画面

```
┌────────────────────────────────────────┐
│                                        │
│         游 戏 结 束                    │  ← 红色大字
│                                        │
│       最终得分: 100                    │  ← 显示得分
│                                        │
│   按 C 重新开始 | 按 Q 退出            │  ← 操作提示
│                                        │
└────────────────────────────────────────┘
```

---

## 六、代码结构

```
snake_game.py
├── 配置常量                    # 窗口大小、颜色、速度等
│   ├── WINDOW_WIDTH/HEIGHT    # 窗口尺寸
│   ├── GRID_SIZE              # 格子大小
│   ├── FPS                    # 游戏速度
│   └── 颜色定义               # 黑、白、绿、红等
│
├── Snake 类                   # 蛇的类
│   ├── __init__()             # 初始化蛇的位置和方向
│   ├── change_direction()     # 改变移动方向
│   ├── move()                 # 移动蛇
│   ├── grow()                 # 增长蛇身
│   ├── check_self_collision() # 检查是否撞到自己
│   ├── check_wall_collision() # 检查是否撞墙
│   └── draw()                 # 绘制蛇
│
├── Food 类                    # 食物的类
│   ├── __init__()             # 初始化食物位置
│   ├── randomize_position()   # 随机生成位置
│   └── draw()                 # 绘制食物
│
├── Game 类                    # 游戏主类
│   ├── __init__()             # 初始化 Pygame
│   ├── reset_game()           # 重置游戏
│   ├── handle_events()        # 处理用户输入
│   ├── update()               # 更新游戏逻辑
│   ├── draw()                 # 绘制游戏画面
│   └── run()                  # 游戏主循环
│
└── main()                     # 程序入口
```

---

## 七、游戏特点

### ✅ 完整功能
- 方向键控制蛇移动
- 吃到食物增长和加分
- 撞墙/撞身检测
- 游戏结束和重新开始

### ✅ 代码质量
- 详细中文注释
- 结构清晰，面向对象设计
- 适合新手学习

### ✅ 异常处理
- Pygame 未安装提示
- 运行异常捕获
- 资源正确释放

### ✅ 扩展性
- 可调整游戏速度（修改 FPS 常量）
- 可调整窗口大小
- 可修改颜色主题

---

## 八、自定义修改

### 修改游戏速度

编辑代码中的 `FPS` 常量：

```python
FPS = 15  # 数值越大，蛇移动越快
```

### 修改窗口大小

```python
WINDOW_WIDTH = 1000   # 窗口宽度
WINDOW_HEIGHT = 800   # 窗口高度
```

### 修改颜色

```python
COLOR_GREEN = (0, 255, 0)      # 蛇身颜色（绿色）
COLOR_RED = (255, 0, 0)        # 食物颜色（红色）
COLOR_BLACK = (0, 0, 0)        # 背景颜色（黑色）
```

### 修改食物分值

在 `update()` 方法中修改：

```python
if self.snake.get_head_position() == self.food.position:
    self.snake.grow(1)
    self.score += 20  # 改为 20 分
```

---

## 九、常见问题

### Q: 运行提示 "No module named 'pygame'"

**A**: 需要先安装 Pygame 库：
```bash
pip install pygame
```

### Q: 游戏运行很卡

**A**: 尝试降低 FPS 值：
```python
FPS = 8  # 降低速度
```

### Q: 如何调整游戏难度

**A**: 可以通过以下方式调整：
1. 增加 FPS 值让蛇移动更快
2. 减小 GRID_SIZE 让格子更小
3. 增加蛇的初始长度

### Q: 游戏窗口可以调整大小吗

**A**: 可以修改 `WINDOW_WIDTH` 和 `WINDOW_HEIGHT` 常量，注意需要能被 `GRID_SIZE` 整除。

---

## 十、技术要点

### Pygame 基础

```python
# 初始化
pygame.init()

# 创建窗口
screen = pygame.display.set_mode((800, 600))

# 游戏主循环
running = True
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    
    # 更新游戏逻辑
    # ...
    
    # 绘制画面
    screen.fill((0, 0, 0))  # 黑色背景
    # ... 绘制游戏元素 ...
    pygame.display.flip()    # 更新屏幕
    
    # 控制帧率
    clock.tick(10)
```

### 贪吃蛇核心算法

```python
# 移动蛇
new_head = (head_x + direction_x, head_y + direction_y)
body.insert(0, new_head)  # 添加新头部

if 吃到食物:
    # 不删除尾部，蛇变长
    pass
else:
    body.pop()  # 删除尾部，保持长度
```

---

## 十一、文件清单

```
d:\clone\
├── snake_game.py           # 游戏主程序
└── snake_game_readme.md    # 游戏说明文档
```

---

**祝您游戏愉快！🎮🐍**

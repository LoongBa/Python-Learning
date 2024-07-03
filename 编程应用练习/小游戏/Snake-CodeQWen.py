import pygame
import random

# 初始化Pygame
pygame.init()

# 设置窗口大小
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 300
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# 蛇的初始位置和方向
snake = [(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)]
direction = 'right'

# 游戏主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'down':
                direction = 'up'
            elif event.key == pygame.K_DOWN and direction != 'up':
                direction = 'down'
            elif event.key == pygame.K_LEFT and direction != 'right':
                direction = 'left'
            elif event.key == pygame.K_RIGHT and direction != 'left':
                direction = 'right'

    # 移动蛇
    move_snake()

    # 检查碰撞
    if check_collision():
        running = False

    # 生成食物
    food = generate_food()

    # 清除屏幕
    screen.fill(WHITE)

    # 绘制蛇和食物
    for pos in snake:
        pygame.draw.rect(screen, BLACK, pygame.Rect(pos[0], pos[1]))
    pygame.draw.rect(screen, GREEN, pygame.Rect(food[0], food[1]))

    # 更新显示
    pygame.display.flip()

    # 延迟以控制游戏帧率
    pygame.time.Clock().tick(60)

# 退出Pygame
pygame.quit()
import pygame
import random

# 初始化 pygame
pygame.init()

# 设置窗口大小
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# 设置标题
pygame.display.set_caption("贪吃蛇")

# 定义一些常量
BLOCK_SIZE = 20
SNAKE_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 0, 0)

# 初始化 snake 和 food
snake = [(100, 100), (120, 100), (140, 100)]
food = (random.randint(0, screen_width - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE,
        random.randint(0, screen_height - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE)

# 游戏主循环
while True:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 更新 snake
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        snake.append((snake[-1][0], snake[-1][1] - BLOCK_SIZE))
    elif keys[pygame.K_DOWN]:
        snake.append((snake[-1][0], snake[-1][1] + BLOCK_SIZE))
    elif keys[pygame.K_LEFT]:
        snake.append((snake[-1][0] - BLOCK_SIZE, snake[-1][1]))
    elif keys[pygame.K_RIGHT]:
        snake.append((snake[-1][0] + BLOCK_SIZE, snake[-1][1]))

    # 检查是否吃到食物
    if snake[-1] == food:
        food = (random.randint(0, screen_width - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE,
                random.randint(0, screen_height - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE)
    else:
        snake.pop(0)

    # 画图
    screen.fill((255, 255, 255))
    for x, y in snake:
        pygame.draw.rect(screen, SNAKE_COLOR, (x, y, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, FOOD_COLOR, (food[0], food[1], BLOCK_SIZE, BLOCK_SIZE))

    # 更新屏幕
    pygame.display.flip()
    pygame.time.Clock().tick(10)
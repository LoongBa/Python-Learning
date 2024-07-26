# 初始化游戏
import pygame
import random

pygame.init()

# 设置游戏窗口
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("贪吃蛇游戏")

# 设置颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# 设置蛇和食物
SNAKE_BLOCK_SIZE = 20
SNAKE_SPEED = 15
snake_list = []
snake_length = 1
snake_head = [WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2]

food_x = round(random.randrange(0, WINDOW_WIDTH - SNAKE_BLOCK_SIZE) / 20.0) * 20.0
food_y = round(random.randrange(0, WINDOW_HEIGHT - SNAKE_BLOCK_SIZE) / 20.0) * 20.0

# 设置游戏循环
game_over = False
clock = pygame.time.Clock()

# 定义函数
def draw_snake(snake_block_size, snake_list):
    for x in snake_list:
        pygame.draw.rect(window, BLACK, [x[0], x[1], snake_block_size, snake_block_size])

def draw_food(food_x, food_y):
    pygame.draw.rect(window, RED, [food_x, food_y, SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE])

# 游戏循环
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # 移动蛇
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        snake_head[0] -= SNAKE_BLOCK_SIZE
    if keys[pygame.K_RIGHT]:
        snake_head[0] += SNAKE_BLOCK_SIZE
    if keys[pygame.K_UP]:
        snake_head[1] -= SNAKE_BLOCK_SIZE
    if keys[pygame.K_DOWN]:
        snake_head[1] += SNAKE_BLOCK_SIZE

    # 检查是否吃到食物
    if snake_head[0] == food_x and snake_head[1] == food_y:
        food_x = round(random.randrange(0, WINDOW_WIDTH - SNAKE_BLOCK_SIZE) / 20.0) * 20.0
        food_y = round(random.randrange(0, WINDOW_HEIGHT - SNAKE_BLOCK_SIZE) / 20.0) * 20.0
        snake_length += 1

    # 更新蛇的身体
    snake_list.append(list(snake_head))
    if len(snake_list) > snake_length:
        del snake_list[0]

    # 检查是否撞到自己的身体
    for x in snake_list[:-1]:
        if x == snake_head:
            game_over = True

    # 绘制游戏窗口
    window.fill(WHITE)
    draw_snake(SNAKE_BLOCK_SIZE, snake_list)
    draw_food(food_x, food_y)
    pygame.display.update()

    # 设置游戏速度
    clock.tick(SNAKE_SPEED)

# 退出游戏
pygame.quit()

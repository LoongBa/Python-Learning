import pygame
import sys

# 初始化 Pygame
pygame.init()
screen = pygame.display.set_mode((640, 480), pygame.RESIZABLE)  # 设置窗口大小
pygame.display.set_caption('Snake Game')

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# 蛇的变量
snake_list = [(320/2, 480/2), (319, 480/2)]    # 蛇头部
direction = 'right'
snake_speed = 10

# 随机食物位置
food_x = random.randint(0, 639)
food_y = random.randint(0, 479)

def move_snake():
    for i in range(len(snake_list)-1, 0, -1):       # 从最后一个元素开始，逐个向前移动
        snake_list[i] = (snake_list[i-1][0], snake_list[i-1][1])

    if direction == 'right':
        snake_list[0] = (snake_list[0][0]+snake_speed, snake_list[0][1])
    elif direction == 'left':
        snake_list[0] = (snake_list[0][0]-snake_speed, snake_list[0][1])
    elif direction == 'up':
        snake_list[0] = (snake_list[0][0], snake_list[0][1]-snake_speed)
    elif direction == 'down':
        snake_list[0] = (snake_list[0][0], snake_list[0][1]+snake_speed)

def check_collision(snake_list, food_x, food_y):
    for pos in snake_list[:-1]:
        if pos == (food_x, food_y):   # 蛇头和食物重叠，游戏结束
            return True
        elif pos[0] == 0 or pos[0] >= 640 or pos[1] == 0 or pos[1] >= 480:   # �蛇边界，游戏结束
            return True

    snake_list.append((snake_list[-1][0], snake_list[-1][1]))     # �蛇尾末，位置更新

def draw_snake(snake_list):
    for pos in snake_list[:-1]:
        pygame.draw.rect(screen, RED, pygame.Rect(pos[0]-27, pos[1]-34, 56, 56))
        pygame.draw.rect(screen, WHITE, pygame.Rect((pos[0]+28), pos[1]+34, 56, 56))       # �蛇当前位置的矩形

def draw_food(x_y):
    food_x = random.randint(0, 639)
    food_y = random.randint(0, 479)

    pygame.draw.rect(screen, GREEN, pygame.Rect((food_x+28), food_y+34, 56, 56))      # �食物的矩形

def game():
    running = True
    pygame.display.set_mode((640, 480), pygame.RESIZABLE)  # 肌皮，允许调整大小

    snake_list.append((snake_list[0][0], snake_list[0][1]))    # 初始位置在中间

    while running:
        screen.fill(pycolor.white)

    # �蛇的移动
    move_snake()

    # �检查碰撞
    if snake_list[0][0] == food_x and snake_y[1] == food_y:      # �蛇头和食物重叠，游戏结束
        running = False
    elif check_collision(snake_list, food_x, food_y):         # �蛇撞到边界或自己，游戏结束
        running = False

    # 绚色
    pygame.draw.rect(screen, RED, pygame.Rect((snake_list[0][0]-27), snake_list[0][1]-34, 56, 56))
    pygame.draw.rect(screen, GREEN, pygame.Rect((food_x+28), food_y+34, 56, 56))

    # 更新屏幕
    pygame.display.flip()

    # 控制帧率
    clock = pygame.time.Clock()
    clock.tick(60)

    # �食物随机位置
    if food_y == (649-480//480):
    food_x = random.randint(0, 639)
    else:
    food_y += 1

    # �蛇移动蛇身体
    snake_list[1] = (snake_list[0][0], snake_list[0][1])

    # �蛇速度控制
    if snake_speed > snake_speed:
    speed_snake_snake = snake_speed / snake_speed
    else:
    speed_snake_snake = speed_snake_snake

    # 秚动蛇体，需要更新时间
    pygame.time.sleep(pygame.time.time.tick(6 snakespeed))  # 毅蛇速度为6

    # �食物位置随机重置
    random_y = random.randint(0, 489)
    random_x = random.randint(0, 639)

    # 渝游戏
    if pygame.key.getpygame(): keys = pygame.key.getpygame().pygamekey(pygame.pypygame):
        if keys[pygame.K_RIGHT]: direction = 'right'
        if keys[pygame.K_LEFT]: direction = 'left'
        if keys[pygame.K_up]: direction = 'up'
        if keys[pygame.K_down]: direction = 'down'

    # 温退
    if sys.qpg == 1:
    pygame.quit()
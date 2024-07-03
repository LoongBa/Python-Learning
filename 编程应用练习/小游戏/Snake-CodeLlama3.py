import pygame
import random

# 设置屏幕大小和标题
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
TITLE = "贪吃蛇"

# 初始化 Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)

# 设置游戏速度
SPEED = 10

# 定义游戏对象
class Snake:
    def __init__(self):
        self.body = [(100, 100), (90, 100), (80, 100)]
        self.direction = 'right'
        self.length = len(self.body)
    
    def move(self):
        if self.direction == 'right':
            head = self.body[0]
            new_head = (head[0] + 10, head[1])
            self.body.insert(0, new_head)
            self.body.pop()
        elif self.direction == 'left':
            head = self.body[0]
            new_head = (head[0] - 10, head[1])
            self.body.insert(0, new_head)
            self.body.pop()
        elif self.direction == 'up':
            head = self.body[0]
            new_head = (head[0], head[1] - 10)
            self.body.insert(0, new_head)
            self.body.pop()
        elif self.direction == 'down':
            head = self.body[0]
            new_head = (head[0], head[1] + 10)
            self.body.insert(0, new_head)
            self.body.pop()

class Food:
    def __init__(self):
        self.position = (random.randint(0, SCREEN_WIDTH - 10), random.randint(0, SCREEN_HEIGHT - 10))

# 创建游戏对象
snake = Snake()
food = Food()

# 游戏主循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and snake.direction != 'right':
                snake.direction = 'left'
            elif event.key == pygame.K_RIGHT and snake.direction != 'left':
                snake.direction = 'right'
            elif event.key == pygame.K_UP and snake.direction != 'down':
                snake.direction = 'up'
            elif event.key == pygame.K_DOWN and snake.direction != 'up':
                snake.direction = 'down'

    # 更新游戏
    snake.move()
    if snake.body[0] == food.position:
        snake.length += 1
        food = Food()

    # 绘制游戏
    screen.fill((255, 255, 255))
    for pos in snake.body:
        pygame.draw.rect(screen, (0, 0, 0), (pos[0], pos[1], 10, 10))
    pygame.draw.rect(screen, (255, 0, 0), food.position + (10, 10))

    # 更新屏幕
    pygame.display.flip()
    pygame.time.Clock().tick(SPEED)

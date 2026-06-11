# AimTester - 瞄准测试游戏 (喵准测试) v2
# 增加移动目标 + 不同大小难度

import pygame
import random
import sys
from datetime import datetime

# 初始化 Pygame
pygame.init()

# 屏幕设置
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AimTester - 喵准测试 v2")

# 颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)

# 字体
font = pygame.font.SysFont("simhei", 36)
small_font = pygame.font.SysFont("simhei", 24)

# 游戏变量
score = 0
targets_hit = 0
time_left = 60
targets = []
clock = pygame.time.Clock()
running = True
game_over = False

class Target:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.radius = random.randint(15, 35)  # 不同大小
        self.x = random.randint(self.radius, WIDTH - self.radius)
        self.y = random.randint(self.radius, HEIGHT - self.radius)
        self.speed_x = random.uniform(-3, 3)
        self.speed_y = random.uniform(-3, 3)
        self.color = RED
    
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        
        # 反弹
        if self.x - self.radius < 0 or self.x + self.radius > WIDTH:
            self.speed_x *= -1
        if self.y - self.radius < 0 or self.y + self.radius > HEIGHT:
            self.speed_y *= -1
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.radius - 5)

# 创建初始目标
for _ in range(6):
    targets.append(Target())

# 主循环
start_time = pygame.time.get_ticks()

while running:
    current_time = pygame.time.get_ticks()
    elapsed = (current_time - start_time) // 1000
    time_left = max(0, 60 - elapsed)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for i, target in enumerate(targets[:]):
                distance = ((mouse_x - target.x)**2 + (mouse_y - target.y)**2)**0.5
                if distance <= target.radius:
                    score += int(50 / target.radius * 10)  # 小目标分数更高
                    targets_hit += 1
                    targets.pop(i)
                    targets.append(Target())
                    break

    if time_left <= 0:
        game_over = True

    # 更新移动目标
    for target in targets:
        target.update()

    # 绘制
    screen.fill(BLACK)

    for target in targets:
        target.draw(screen)

    # HUD
    score_text = font.render(f"分数: {score}", True, WHITE)
    hits_text = small_font.render(f"命中: {targets_hit}", True, GREEN)
    time_text = font.render(f"时间: {time_left}s", True, WHITE)
    level_text = small_font.render("难度: 移动目标", True, BLUE)
    screen.blit(score_text, (20, 20))
    screen.blit(hits_text, (20, 70))
    screen.blit(time_text, (WIDTH - 200, 20))
    screen.blit(level_text, (20, 110))

    if game_over:
        game_over_text = font.render(f"时间到！最终分数: {score}", True, RED)
        restart_text = small_font.render("按 R 重新开始", True, WHITE)
        screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 50))
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 20))

    pygame.display.flip()
    clock.tick(60)

    # 重新开始
    if game_over and pygame.key.get_pressed()[pygame.K_r]:
        score = 0
        targets_hit = 0
        start_time = pygame.time.get_ticks()
        game_over = False
        targets.clear()
        for _ in range(6):
            targets.append(Target())

pygame.quit()
sys.exit()
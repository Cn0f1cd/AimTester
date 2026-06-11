# AimTester - 瞄准测试游戏 (喵准测试)
# 使用 Pygame 实现简单的鼠标瞄准训练工具

import pygame
import random
import sys
from datetime import datetime

# 初始化 Pygame
pygame.init()

# 屏幕设置
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AimTester - 喵准测试")

# 颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)

# 字体
font = pygame.font.SysFont("simhei", 36)  # 支持中文
small_font = pygame.font.SysFont("simhei", 24)

# 游戏变量
score = 0
targets_hit = 0
time_left = 60  # 60秒挑战模式
target_radius = 20
targets = []
clock = pygame.time.Clock()
running = True
game_over = False

# 生成目标
def create_target():
    x = random.randint(target_radius, WIDTH - target_radius)
    y = random.randint(target_radius, HEIGHT - target_radius)
    return [x, y, target_radius]

# 初始目标
for _ in range(5):
    targets.append(create_target())

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
                tx, ty, tr = target
                distance = ((mouse_x - tx)**2 + (mouse_y - ty)**2)**0.5
                if distance <= tr:
                    # 命中！
                    score += 10
                    targets_hit += 1
                    targets.pop(i)
                    targets.append(create_target())
                    break

    if time_left <= 0:
        game_over = True

    # 绘制
    screen.fill(BLACK)

    # 绘制目标
    for target in targets:
        pygame.draw.circle(screen, RED, (target[0], target[1]), target[2])
        pygame.draw.circle(screen, WHITE, (target[0], target[1]), target[2] - 5)

    # HUD
    score_text = font.render(f"分数: {score}", True, WHITE)
    hits_text = small_font.render(f"命中: {targets_hit}", True, GREEN)
    time_text = font.render(f"时间: {time_left}s", True, WHITE)
    screen.blit(score_text, (20, 20))
    screen.blit(hits_text, (20, 70))
    screen.blit(time_text, (WIDTH - 200, 20))

    if game_over:
        game_over_text = font.render("时间到！最终分数: " + str(score), True, RED)
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
        for _ in range(5):
            targets.append(create_target())

pygame.quit()
sys.exit()
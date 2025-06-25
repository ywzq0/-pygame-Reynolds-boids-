import pygame
import random
import sys
from pygame.locals import *
from settings import *
from entities.boid import Boid
from entities.predator import Predator
from entities.obstacle import Obstacle
from utils import init_fonts, draw_text, draw_stats
from pygame.math import Vector2

def main():
    # 初始化Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Reynolds Boids 模型")
    
    # 初始化字体
    font, title_font = init_fonts()
    
    # 创建初始实体
    boids = [Boid(random.randint(0, WIDTH), random.randint(0, HEIGHT)) 
             for _ in range(INITIAL_BOIDS)]
    predators = []
    obstacles = []
    
    # 高亮一个Boid
    highlighted_boid = random.choice(boids)
    highlighted_boid.highlight = True
    highlight_timer = 0
    
    # 主循环
    clock = pygame.time.Clock()
    paused = False
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    paused = not paused
                elif event.key == K_r:  # 重置模拟
                    boids = [Boid(random.randint(0, WIDTH), random.randint(0, HEIGHT)) 
                            for _ in range(INITIAL_BOIDS)]
                    predators = []
                    obstacles = []
                    highlighted_boid = random.choice(boids)
                    highlighted_boid.highlight = True
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键添加障碍物
                    obstacles.append(Obstacle(event.pos[0], event.pos[1], random.randint(20, 50)))
                elif event.button == 3:  # 右键添加捕食者
                    predators.append(Predator(event.pos[0], event.pos[1]))

        if not paused:
            # 更新高亮计时器
            highlight_timer += 1
            if highlight_timer > 300:  # 每300帧切换高亮Boid
                highlighted_boid.highlight = False
                highlighted_boid = random.choice(boids)
                highlighted_boid.highlight = True
                highlight_timer = 0

            # 更新Boids
            for boid in boids:
                # 应用群体行为规则
                alignment = boid.align(boids)
                cohesion = boid.cohesion(boids)
                separation = boid.separation(boids)
                
                # 应用力
                boid.apply_force(alignment * 1.0)
                boid.apply_force(cohesion * 1.2)
                boid.apply_force(separation * 1.5)
                
                # 如果有障碍物，应用避障行为
                if obstacles:
                    obstacle_avoidance = boid.avoid_obstacles(obstacles)
                    boid.apply_force(obstacle_avoidance * 2.0)
                
                # 如果有捕食者，应用逃离行为
                if predators:
                    flee = Vector2(0, 0)
                    for predator in predators:
                        flee += boid.flee(predator)
                    boid.apply_force(flee * 2.5)
                
                boid.update()

            # 更新捕食者
            for predator in predators:
                chase_force = predator.chase(boids)
                predator.apply_force(chase_force * 1.5)
                predator.update()

        # 绘制
        screen.fill(BACKGROUND)
        
        # 绘制障碍物（如果有）
        for obstacle in obstacles:
            obstacle.draw(screen)
        
        # 绘制Boids
        for boid in boids:
            boid.draw(screen)
        
        # 绘制捕食者（如果有）
        for predator in predators:
            predator.draw(screen)
        
        # 绘制所有文本
        draw_text(screen, font, title_font)
        draw_stats(screen, font, boids, predators, obstacles, paused)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
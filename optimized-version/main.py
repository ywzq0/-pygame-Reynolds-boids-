import pygame
import random
import sys
from pygame.locals import *
from settings import *
from entities.boid import Boid
from entities.predator import Predator
from entities.obstacle import Obstacle
from utils import init_fonts, draw_text, draw_stats, SpatialGrid, draw_grid, draw_force_field
from pygame.math import Vector2

def main():
    # 初始化Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Optimized Reynolds Boids Model")
    
    # 初始化字体
    font, title_font = init_fonts()
    
    # 创建实体和空间分区网格
    boids = [Boid(random.randint(0, WIDTH), random.randint(0, HEIGHT)) 
             for _ in range(INITIAL_BOIDS)]
    predators = []
    obstacles = []
    grid = SpatialGrid(WIDTH, HEIGHT, GRID_CELL_SIZE)

    # 模拟参数
    sim_params = {
        "align_weight": ALIGN_WEIGHT,
        "cohesion_weight": COHESION_WEIGHT,
        "separation_weight": SEPARATION_WEIGHT,
    }
    
    # 高亮Boid作为领导者
    highlighted_boid = random.choice(boids)
    highlighted_boid.is_leader = True
    
    # 主循环控制
    clock = pygame.time.Clock()
    paused = False
    debug_grid = False
    debug_forces = False
    
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
                    highlighted_boid.is_leader = True
                elif event.key == K_g: # 切换网格可视化
                    debug_grid = not debug_grid
                elif event.key == K_f: # 切换力场可视化
                    debug_forces = not debug_forces
                # 动态参数调整
                elif event.key == K_UP:
                    sim_params["separation_weight"] += 0.1
                elif event.key == K_DOWN:
                    sim_params["separation_weight"] -= 0.1
                elif event.key == K_RIGHT:
                    sim_params["cohesion_weight"] += 0.1
                elif event.key == K_LEFT:
                    sim_params["cohesion_weight"] -= 0.1
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键添加障碍物
                    obstacles.append(Obstacle(event.pos[0], event.pos[1], random.randint(20, 50)))
                elif event.button == 3:  # 右键添加捕食者
                    predators.append(Predator(event.pos[0], event.pos[1]))

        if not paused:
            # --- 更新阶段 ---
            
            # 1. 将Boids放入空间网格以优化邻居查找
            grid.clear()
            for boid in boids:
                grid.add(boid)

            # 2. 更新Boids
            for boid in boids:
                # 从网格获取近邻，避免O(n^2)计算
                neighbors = grid.get_neighbors(boid, boid.perception)
                boid.apply_behaviors(neighbors, predators, obstacles, sim_params)
                boid.update()

            # 3. 更新捕食者
            for predator in predators:
                # 从网格获取Boid目标
                nearby_boids = grid.get_neighbors(predator, predator.perception)
                predator.apply_behaviors(nearby_boids)
                predator.update()

        # --- 绘制阶段 ---
        screen.fill(BACKGROUND)
        
        # 可选的可视化
        if debug_grid:
            draw_grid(screen, grid)
        if debug_forces:
            draw_force_field(screen, boids)
        
        for obstacle in obstacles:
            obstacle.draw(screen)
        
        for predator in predators:
            predator.draw(screen)
            
        for boid in boids:
            boid.draw(screen)
        
        draw_text(screen, font, title_font)
        draw_stats(screen, font, boids, predators, obstacles, paused, sim_params)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
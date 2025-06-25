import pygame
from settings import *
from pygame.math import Vector2

def init_fonts():
    """初始化字体"""
    pygame.font.init()
    try:
        font = pygame.font.SysFont('microsoftyahei', FONT_SIZE)
        title_font = pygame.font.SysFont('microsoftyahei', TITLE_FONT_SIZE)
    except:
        font = pygame.font.SysFont(None, FONT_SIZE + 5)
        title_font = pygame.font.SysFont(None, TITLE_FONT_SIZE + 5)
    return font, title_font

def draw_text(screen, font, title_font):
    """绘制所有文本"""
    title = title_font.render("Optimized Boids Model", True, HIGHLIGHT_COLOR)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))
    
    instructions = [
        "空格键: 停止/继续, R: 重置, ESC: 退出, G: 显示/隐藏网络, F: 显示/隐藏力场",
        "鼠标左键: 添加障碍物, 鼠标右键: 添加捕食者",
        "上/下键: 调整分离权重, 左/右键: 调整聚合权重",
    ]
    
    for i, text in enumerate(instructions):
        text_surf = font.render(text, True, TEXT_COLOR)
        screen.blit(text_surf, (20, HEIGHT - 90 + i * 25))

def draw_stats(screen, font, boids, predators, obstacles, paused, params):
    """绘制统计数据和参数"""
    if paused:
        pause_surf = font.render("PAUSED", True, HIGHLIGHT_COLOR)
        screen.blit(pause_surf, (WIDTH // 2 - pause_surf.get_width() // 2, HEIGHT / 2))
        
    stats = [
        f"Boids数量: {len(boids)}",
        f"捕食者数量: {len(predators)}",
        f"障碍物数量: {len(obstacles)}",
        "--- 权重 ---",
        f"碰撞规避: {params['separation_weight']:.1f}",
        f"群体中心定位: {params['cohesion_weight']:.1f}",
        f"速度匹配: {params['align_weight']:.1f}",
    ]
    
    for i, text in enumerate(stats):
        text_surf = font.render(text, True, TEXT_COLOR)
        screen.blit(text_surf, (WIDTH - 250, 20 + i * 25))

def draw_grid(screen, grid):
    """绘制空间分区网格"""
    for x in range(0, WIDTH, grid.cell_size):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, grid.cell_size):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))

def draw_force_field(screen, boids):
    """可视化Boid的速度场"""
    for y in range(0, HEIGHT, 40):
        for x in range(0, WIDTH, 40):
            pos = Vector2(x, y)
            avg_vel = Vector2()
            count = 0
            for boid in boids:
                if pos.distance_to(boid.position) < 80:
                    avg_vel += boid.velocity
                    count += 1
            if count > 0:
                avg_vel /= count
                if avg_vel.length() > 0:
                    end_pos = pos + avg_vel.normalize() * 15
                    pygame.draw.line(screen, FORCE_COLOR, pos, end_pos, 1)

class SpatialGrid:
    """空间分区网格，用于优化邻居查找"""
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid_width = (width // cell_size) + 1
        self.grid_height = (height // cell_size) + 1
        self.clear()

    def clear(self):
        self.grid = [[] for _ in range(self.grid_width * self.grid_height)]

    def _get_cell_index(self, position):
        x = max(0, min(self.grid_width - 1, int(position.x // self.cell_size)))
        y = max(0, min(self.grid_height - 1, int(position.y // self.cell_size)))
        return y * self.grid_width + x

    def add(self, entity):
        index = self._get_cell_index(entity.position)
        self.grid[index].append(entity)

    def get_neighbors(self, entity, radius):
        neighbors = []
        center_x = int(entity.position.x // self.cell_size)
        center_y = int(entity.position.y // self.cell_size)
        
        # 检查周围九个单元格（包括中心）
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                nx, ny = center_x + dx, center_y + dy
                if 0 <= nx < self.grid_width and 0 <= ny < self.grid_height:
                    index = ny * self.grid_width + nx
                    for neighbor in self.grid[index]:
                        if neighbor is not entity:
                            dist_sq = entity.position.distance_squared_to(neighbor.position)
                            if dist_sq < radius * radius:
                                neighbors.append(neighbor)
        return neighbors
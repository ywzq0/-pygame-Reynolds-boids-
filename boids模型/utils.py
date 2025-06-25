import pygame
from settings import *

def init_fonts():
    """初始化字体"""
    pygame.font.init()
    font = pygame.font.SysFont('microsoftyahei', FONT_SIZE)
    title_font = pygame.font.SysFont('microsoftyahei', TITLE_FONT_SIZE)
    return font, title_font

def draw_text(screen, font, title_font):
    """绘制所有文本"""
    # 绘制标题
    title = title_font.render("Reynolds Boids 群体行为模拟", True, HIGHLIGHT_COLOR)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))
    
    # 绘制说明文字
    instructions = [
        "群体行为规则: 碰撞规避(Coliision Avoidance),速度匹配(Velocity Matching),群体中心定位(Flock Centering)",
        "操作指南: 空格键暂停/继续, R键重置, ESC键退出",
        "鼠标左键: 添加障碍物, 鼠标右键: 添加捕食者"
    ]
    
    for i, text in enumerate(instructions):
        text_surf = font.render(text, True, TEXT_COLOR)
        screen.blit(text_surf, (20, HEIGHT - 100 + i * 30))
    
    return font, title_font

def draw_stats(screen, font, boids, predators, obstacles, paused):
    """绘制统计数据"""
    stats = [
        f"Boids数量: {len(boids)}",
        f"捕食者数量: {len(predators)}",
        f"障碍物数量: {len(obstacles)}",
    ]
    
    for i, text in enumerate(stats):
        text_surf = font.render(text, True, TEXT_COLOR)
        screen.blit(text_surf, (WIDTH - 250, 20 + i * 30))

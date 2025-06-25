# 屏幕设置
WIDTH, HEIGHT = 1200, 800
FPS = 60

# 颜色定义
BACKGROUND = (10, 20, 30)
BOID_COLOR = (100, 200, 255)
TRAIL_COLOR = (80, 180, 240, 50)
PREDATOR_COLOR = (255, 80, 80)
OBSTACLE_COLOR = (120, 100, 180)
TEXT_COLOR = (200, 220, 255)
HIGHLIGHT_COLOR = (255, 215, 80)

# 字体设置
FONT_SIZE = 15
TITLE_FONT_SIZE = 25

# Boid默认参数
BOID_DEFAULTS = {
    "max_speed": 5.0,
    "max_force": 0.2,
    "perception": 80,
    "size": 6,
    "max_trail": 10
}

# Predator默认参数
PREDATOR_DEFAULTS = {
    "max_speed": 4.0,
    "max_force": 0.3,
    "perception": 150,
    "size": 10
}

# 初始数量
INITIAL_BOIDS = 120
INITIAL_PREDATORS = 0
INITIAL_OBSTACLES = 0
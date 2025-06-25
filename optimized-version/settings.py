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
GRID_COLOR = (30, 50, 70)
FORCE_COLOR = (80, 255, 80, 150)

# 字体设置
FONT_SIZE = 15
TITLE_FONT_SIZE = 25

# --- Boid 优化参数 ---
# 行为权重 (可在运行时调整)
ALIGN_WEIGHT = 1.0
COHESION_WEIGHT = 1.0
SEPARATION_WEIGHT = 1.6

# 感知系统
BOID_FOV_ANGLE = 140  # Boid的视野范围（度）
PREDICTION_FACTOR = 0.5 # 预测性避障的未来时间（秒）

# 状态机和动态权重
THREAT_AWARENESS_RADIUS = 180 # 感知到威胁的范围
FLEE_WEIGHT_MULTIPLIER = 3.0
SEPARATION_THREAT_MULTIPLIER = 2.5

# Boid默认参数
BOID_DEFAULTS = {
    "max_speed": 4.5,
    "max_force": 0.2,
    "perception": 70,
    "size": 6,
    "max_trail": 10
}

# Predator默认参数
PREDATOR_DEFAULTS = {
    "max_speed": 4.0,
    "max_force": 0.3,
    "perception": 180,
    "size": 10
}

# 性能优化
GRID_CELL_SIZE = 80  # 空间分区网格大小

# 初始数量
INITIAL_BOIDS = 120
INITIAL_PREDATORS = 0
INITIAL_OBSTACLES = 0
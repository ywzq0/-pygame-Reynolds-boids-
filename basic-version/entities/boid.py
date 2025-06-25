import pygame
import math
import random
from pygame import Vector2
from settings import *

class Boid:
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.velocity = Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.velocity.scale_to_length(random.uniform(1.5, 3.5))
        self.acceleration = Vector2(0, 0)
        self.max_speed = BOID_DEFAULTS["max_speed"]
        self.max_force = BOID_DEFAULTS["max_force"]
        self.perception = BOID_DEFAULTS["perception"]
        self.size = BOID_DEFAULTS["size"]
        self.trail = []
        self.max_trail = BOID_DEFAULTS["max_trail"]
        self.color = BOID_COLOR
        self.highlight = False

    def update(self):
        # 保存位置到轨迹
        self.trail.append((self.position.x, self.position.y))
        if len(self.trail) > self.max_trail:
            self.trail.pop(0)
            
        # 更新速度和位置
        self.velocity += self.acceleration
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)
        self.position += self.velocity
        self.acceleration = Vector2(0, 0)
        
        # 边界处理 - 环绕
        self._wrap_around()

    def _wrap_around(self):
        if self.position.x < -self.size:
            self.position.x = WIDTH + self.size
        elif self.position.x > WIDTH + self.size:
            self.position.x = -self.size
        if self.position.y < -self.size:
            self.position.y = HEIGHT + self.size
        elif self.position.y > HEIGHT + self.size:
            self.position.y = -self.size

    def apply_force(self, force):
        self.acceleration += force

    def align(self, boids):
        steering = Vector2(0, 0)
        total = 0
        for boid in boids:
            if boid != self and self.position.distance_to(boid.position) < self.perception:
                steering += boid.velocity
                total += 1
        if total > 0:
            steering /= total
            steering.scale_to_length(self.max_speed)
            steering -= self.velocity
            if steering.length() > self.max_force:
                steering.scale_to_length(self.max_force)
        return steering

    def cohesion(self, boids):
        steering = Vector2(0, 0)
        total = 0
        for boid in boids:
            if boid != self and self.position.distance_to(boid.position) < self.perception:
                steering += boid.position
                total += 1
        if total > 0:
            steering /= total
            steering -= self.position
            if steering.length() > 0:
                steering.scale_to_length(self.max_speed)
            steering -= self.velocity
            if steering.length() > self.max_force:
                steering.scale_to_length(self.max_force)
        return steering

    def separation(self, boids):
        steering = Vector2(0, 0)
        total = 0
        for boid in boids:
            distance = self.position.distance_to(boid.position)
            if boid != self and distance < self.perception * 0.6:
                diff = self.position - boid.position
                diff /= distance * distance  # 距离越近，排斥力越大
                steering += diff
                total += 1
        if total > 0:
            steering /= total
            if steering.length() > 0:
                steering.scale_to_length(self.max_speed)
            steering -= self.velocity
            if steering.length() > self.max_force:
                steering.scale_to_length(self.max_force)
        return steering

    def avoid_obstacles(self, obstacles):
        steering = Vector2(0, 0)
        for obstacle in obstacles:
            distance = self.position.distance_to(obstacle.position)
            if distance < obstacle.radius + self.perception * 0.8:
                diff = self.position - obstacle.position
                diff /= distance * distance
                steering += diff * 1.5
        if steering.length() > 0:
            steering.scale_to_length(self.max_speed)
            steering -= self.velocity
            if steering.length() > self.max_force:
                steering.scale_to_length(self.max_force)
        return steering

    def flee(self, predator):
        steering = Vector2(0, 0)
        distance = self.position.distance_to(predator.position)
        if distance < self.perception * 1.5:
            diff = self.position - predator.position
            diff /= distance
            steering += diff * 3.0
        if steering.length() > 0:
            steering.scale_to_length(self.max_speed * 1.5)
            steering -= self.velocity
            if steering.length() > self.max_force * 2:
                steering.scale_to_length(self.max_force * 2)
        return steering

    def draw(self, screen):
        # 绘制轨迹
        if len(self.trail) > 1:
            for i in range(1, len(self.trail)):
                alpha = int(255 * i / len(self.trail))
                pygame.draw.line(screen, (*TRAIL_COLOR[:3], alpha), 
                               self.trail[i-1], self.trail[i], 1)
        
        # 绘制Boid主体
        color = HIGHLIGHT_COLOR if self.highlight else self.color
        angle = math.atan2(self.velocity.y, self.velocity.x)
        
        # 绘制三角形表示方向
        points = [
            (self.position.x + self.size * 2 * math.cos(angle), 
             self.position.y + self.size * 2 * math.sin(angle)),
            (self.position.x + self.size * math.cos(angle + 2.5), 
             self.position.y + self.size * math.sin(angle + 2.5)),
            (self.position.x + self.size * math.cos(angle - 2.5), 
             self.position.y + self.size * math.sin(angle - 2.5))
        ]
        
        pygame.draw.polygon(screen, color, points)
        
        # 高亮显示感知范围
        if self.highlight:
            pygame.draw.circle(screen, (*color, 50), 
                             (int(self.position.x), int(self.position.y)), 
                             self.perception, 1)
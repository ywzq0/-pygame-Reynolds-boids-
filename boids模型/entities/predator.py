import pygame
import math
import random
from pygame import Vector2
from settings import *

class Predator:
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.velocity = Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.velocity.scale_to_length(2.5)
        self.acceleration = Vector2(0, 0)
        self.max_speed = PREDATOR_DEFAULTS["max_speed"]
        self.max_force = PREDATOR_DEFAULTS["max_force"]
        self.perception = PREDATOR_DEFAULTS["perception"]
        self.size = PREDATOR_DEFAULTS["size"]
        self.color = PREDATOR_COLOR

    def update(self):
        self.velocity += self.acceleration
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)
        self.position += self.velocity
        self.acceleration = Vector2(0, 0)
        
        # 边界处理 - 反弹
        self._bounce_off_walls()

    def _bounce_off_walls(self):
        if self.position.x < self.size:
            self.velocity.x *= -0.8
            self.position.x = self.size
        elif self.position.x > WIDTH - self.size:
            self.velocity.x *= -0.8
            self.position.x = WIDTH - self.size
        if self.position.y < self.size:
            self.velocity.y *= -0.8
            self.position.y = self.size
        elif self.position.y > HEIGHT - self.size:
            self.velocity.y *= -0.8
            self.position.y = HEIGHT - self.size

    def apply_force(self, force):
        self.acceleration += force

    def chase(self, boids):
        steering = Vector2(0, 0)
        total = 0
        for boid in boids:
            distance = self.position.distance_to(boid.position)
            if distance < self.perception:
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

    def draw(self, screen):
        # 绘制捕食者
        angle = math.atan2(self.velocity.y, self.velocity.x)
        
        # 绘制三角形表示方向
        points = [
            (self.position.x + self.size * 2.5 * math.cos(angle), 
             self.position.y + self.size * 2.5 * math.sin(angle)),
            (self.position.x + self.size * 1.5 * math.cos(angle + 2.2), 
             self.position.y + self.size * 1.5 * math.sin(angle + 2.2)),
            (self.position.x + self.size * 1.5 * math.cos(angle - 2.2), 
             self.position.y + self.size * 1.5 * math.sin(angle - 2.2))
        ]
        
        pygame.draw.polygon(screen, self.color, points)
        
        # 绘制感知范围
        pygame.draw.circle(screen, (*self.color, 40), 
                         (int(self.position.x), int(self.position.y)), 
                         self.perception, 1)
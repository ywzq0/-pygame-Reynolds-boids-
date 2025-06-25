import pygame
import math
import random
from pygame.math import Vector2
from settings import *

class Predator:
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.velocity = Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * 2.5
        self.acceleration = Vector2()
        self.max_speed = PREDATOR_DEFAULTS["max_speed"]
        self.max_force = PREDATOR_DEFAULTS["max_force"]
        self.perception = PREDATOR_DEFAULTS["perception"]
        self.size = PREDATOR_DEFAULTS["size"]
        self.color = PREDATOR_COLOR

    def apply_behaviors(self, boids):
        """计算并应用追逐行为"""
        chase_force = self.chase(boids)
        self.apply_force(chase_force * 1.5)

    def update(self):
        self.velocity += self.acceleration
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)
        self.position += self.velocity
        self.acceleration *= 0
        self._bounce_off_walls()

    def apply_force(self, force):
        self.acceleration += force

    def seek(self, target):
        desired = (target - self.position).normalize() * self.max_speed
        steering = (desired - self.velocity)
        if steering.length() > self.max_force:
            steering.scale_to_length(self.max_force)
        return steering

    def chase(self, boids):
        """追逐视野内最近的Boid"""
        closest_boid = None
        min_dist_sq = float('inf')
        
        for boid in boids:
            dist_sq = self.position.distance_squared_to(boid.position)
            if dist_sq < self.perception * self.perception and dist_sq < min_dist_sq:
                min_dist_sq = dist_sq
                closest_boid = boid
        
        if closest_boid:
            return self.seek(closest_boid.position)
        
        return Vector2()

    def _bounce_off_walls(self):
        margin = self.size * 2
        if self.position.x < margin:
            self.velocity.x *= -1
            self.position.x = margin
        elif self.position.x > WIDTH - margin:
            self.velocity.x *= -1
            self.position.x = WIDTH - margin
        if self.position.y < margin:
            self.velocity.y *= -1
            self.position.y = margin
        elif self.position.y > HEIGHT - margin:
            self.velocity.y *= -1
            self.position.y = HEIGHT - margin

    def draw(self, screen):
        angle = self.velocity.angle_to(Vector2(1, 0))
        points = [
            Vector2(self.size, 0).rotate(-angle) + self.position,
            Vector2(-self.size, self.size * 0.7).rotate(-angle) + self.position,
            Vector2(-self.size, -self.size * 0.7).rotate(-angle) + self.position,
        ]
        pygame.draw.polygon(screen, self.color, points)
        pygame.draw.circle(screen, (*self.color, 40), self.position, self.perception, 1)
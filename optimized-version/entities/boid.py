import pygame
import math
import random
from pygame.math import Vector2
from settings import *

class Boid:
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.velocity = Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * random.uniform(2, 4)
        self.acceleration = Vector2()
        
        # Boid属性
        self.max_speed = BOID_DEFAULTS["max_speed"]
        self.max_force = BOID_DEFAULTS["max_force"]
        self.perception = BOID_DEFAULTS["perception"]
        self.size = BOID_DEFAULTS["size"]
        self.fov_angle = BOID_FOV_ANGLE
        
        # 状态与可视化
        self.state = "FLOCKING" # FSM: FLOCKING, FLEEING
        self.is_leader = False
        self.leader_target = Vector2(random.randint(0, WIDTH), random.randint(0, HEIGHT))
        self.color = BOID_COLOR
        self.trail = []
        self.max_trail = BOID_DEFAULTS["max_trail"]

    def apply_behaviors(self, neighbors, predators, obstacles, params):
        """根据环境和状态计算并应用所有行为力"""
        self._update_state(predators)
        
        total_force = Vector2()
        
        if self.state == "FLEEING":
            flee_force = self.flee_from_predators(predators) * FLEE_WEIGHT_MULTIPLIER
            sep_force = self.separation(neighbors) * SEPARATION_THREAT_MULTIPLIER
            total_force += flee_force + sep_force
        
        elif self.state == "FLOCKING":
            if self.is_leader:
                # 领导者有一种漫游行为
                if self.position.distance_to(self.leader_target) < 100 or random.random() < 0.01:
                    self.leader_target = Vector2(random.randint(0, WIDTH), random.randint(0, HEIGHT))
                total_force += self.seek(self.leader_target) * 0.5
            
            align_force = self.align(neighbors) * params["align_weight"]
            cohesion_force = self.cohesion(neighbors) * params["cohesion_weight"]
            separation_force = self.separation(neighbors) * params["separation_weight"]
            total_force += align_force + cohesion_force + separation_force

        obstacle_force = self.avoid_obstacles(obstacles) * 2.0
        total_force += obstacle_force
        
        self.apply_force(total_force)

    def _update_state(self, predators):
        """有限状态机：根据威胁更新Boid状态"""
        if predators:
            closest_predator_dist = min(self.position.distance_to(p.position) for p in predators)
            if closest_predator_dist < THREAT_AWARENESS_RADIUS:
                self.state = "FLEEING"
                return
        self.state = "FLOCKING"

    def update(self):
        self.trail.append(self.position.copy())
        if len(self.trail) > self.max_trail:
            self.trail.pop(0)
            
        self.velocity += self.acceleration
        self.velocity.scale_to_length(min(self.max_speed, self.velocity.length()))
        self.position += self.velocity
        self.acceleration *= 0
        self._wrap_around()

    def apply_force(self, force):
        self.acceleration += force

    def _in_view(self, other_pos):
        """检查另一个位置是否在Boid的视野内"""
        to_other = other_pos - self.position
        if to_other.length_squared() == 0: return False
        angle = self.velocity.angle_to(to_other)
        return abs(angle) < self.fov_angle / 2

    def seek(self, target):
        """朝向目标移动的力"""
        desired = (target - self.position).normalize() * self.max_speed
        steering = (desired - self.velocity)
        if steering.length() > self.max_force:
            steering.scale_to_length(self.max_force)
        return steering

    def align(self, neighbors):
        steering = Vector2()
        count = 0
        for other in neighbors:
            if self._in_view(other.position):
                steering += other.velocity
                count += 1
        if count > 0:
            steering /= count
            steering.normalize_ip()
            steering *= self.max_speed
            steering -= self.velocity
            if steering.length() > self.max_force:
                steering.scale_to_length(self.max_force)
        return steering

    def cohesion(self, neighbors):
        center_of_mass = Vector2()
        count = 0
        for other in neighbors:
            if self._in_view(other.position):
                center_of_mass += other.position
                count += 1
        if count > 0:
            center_of_mass /= count
            return self.seek(center_of_mass)
        return Vector2()

    def separation(self, neighbors):
        steering = Vector2()
        count = 0
        for other in neighbors:
            dist = self.position.distance_to(other.position)
            # 即使不在视野内也要避开太近的同伴
            if dist < self.perception * 0.6: 
                diff = self.position - other.position
                if dist > 0:
                    diff /= (dist * dist) # 距离越近，力越大
                steering += diff
                count += 1
        if count > 0:
            steering /= count
            if steering.length() > 0:
                steering.normalize_ip()
                steering *= self.max_speed
            steering -= self.velocity
            if steering.length() > self.max_force:
                steering.scale_to_length(self.max_force)
        return steering

    def avoid_obstacles(self, obstacles):
        """预测性避障"""
        steering = Vector2()
        future_pos = self.position + self.velocity * PREDICTION_FACTOR * FPS * 0.1
        for obs in obstacles:
            dist_to_future = future_pos.distance_to(obs.position)
            if dist_to_future < obs.radius + self.size * 5:
                # 从障碍物中心产生一个排斥力
                away_from_obs = self.position - obs.position
                # 力的强度与距离成反比
                steering += away_from_obs.normalize() * (1 - dist_to_future / (obs.radius + self.perception))
        if steering.length() > self.max_force:
            steering.scale_to_length(self.max_force)
        return steering

    def flee_from_predators(self, predators):
        """从所有感知到的捕食者处逃离"""
        steering = Vector2()
        for predator in predators:
            dist = self.position.distance_to(predator.position)
            if dist < THREAT_AWARENESS_RADIUS:
                steering += self.position - predator.position
        if steering.length() > 0:
            steering.normalize_ip()
            steering *= self.max_speed
            steering -= self.velocity
            if steering.length() > self.max_force:
                steering.scale_to_length(self.max_force * 2) # 逃跑时力更大
        return steering

    def _wrap_around(self):
        if self.position.x < -self.size: self.position.x = WIDTH + self.size
        if self.position.x > WIDTH + self.size: self.position.x = -self.size
        if self.position.y < -self.size: self.position.y = HEIGHT + self.size
        if self.position.y > HEIGHT + self.size: self.position.y = -self.size

    def draw(self, screen):
        # 轨迹
        if len(self.trail) > 1:
            points = [(int(p.x), int(p.y)) for p in self.trail]
            pygame.draw.lines(screen, (*TRAIL_COLOR[:3], 100), False, points, 1)

        # Boid主体
        color = HIGHLIGHT_COLOR if self.is_leader else self.color
        angle = self.velocity.angle_to(Vector2(1, 0))
        
        points = [
            Vector2(self.size, 0).rotate(-angle) + self.position,
            Vector2(-self.size / 2, self.size / 2).rotate(-angle) + self.position,
            Vector2(-self.size / 2, -self.size / 2).rotate(-angle) + self.position,
        ]
        pygame.draw.polygon(screen, color, points)

        if self.is_leader:
            pygame.draw.circle(screen, (*color, 60), self.position, self.perception, 1)
            # 绘制视野范围
            fov_line1 = self.position + Vector2(self.perception, 0).rotate(-angle - self.fov_angle / 2)
            fov_line2 = self.position + Vector2(self.perception, 0).rotate(-angle + self.fov_angle / 2)
            pygame.draw.line(screen, (*color, 60), self.position, fov_line1, 1)
            pygame.draw.line(screen, (*color, 60), self.position, fov_line2, 1)
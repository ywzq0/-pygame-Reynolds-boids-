import pygame
from pygame import Vector2
from settings import *

class Obstacle:
    def __init__(self, x, y, radius):
        self.position = Vector2(x, y)
        self.radius = radius
        self.color = OBSTACLE_COLOR

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, 
                         (int(self.position.x), int(self.position.y)), 
                         self.radius)
        pygame.draw.circle(screen, (*self.color, 100), 
                         (int(self.position.x), int(self.position.y)), 
                         self.radius + 20, 2)
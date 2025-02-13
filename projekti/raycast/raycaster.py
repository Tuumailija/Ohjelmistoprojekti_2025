import pygame
import math
from .ray import Ray

class RayCaster:
    def __init__(self, screen, ray_length=300):
        self.screen = screen
        self.rays = []
        self.ray_length = ray_length  # Maksimipituus säteille
        self.obstacles = []  # Lista esteille

    def set_obstacles(self, obstacles):
        """Asettaa esteet, joihin säteet voivat osua."""
        self.obstacles = obstacles

    def update_rays(self, pos, num_rays=360):
        """Luo säteet hiiren sijainnista."""
        self.rays = [Ray(pos, math.radians(a), self.ray_length) for a in range(0, num_rays, 1)]

    def cast_rays(self):
        """Laskee säteiden loppupisteet ottaen huomioon esteet."""
        return [ray.cast(self.obstacles) for ray in self.rays]

    def draw(self, pos):
        """Piirtää säteet alkaen hiiren sijainnista."""
        points = self.cast_rays()
        for point in points:
            pygame.draw.line(self.screen, (255, 255, 255), pos, point, 1)
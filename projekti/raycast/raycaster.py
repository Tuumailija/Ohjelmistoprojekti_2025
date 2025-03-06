from numpy import linspace
import pygame
import math
from .ray import Ray

rayNumber = (360//2)
fieldOfVision = linspace(0, 360/4, rayNumber)

class RayCaster:
    def __init__(self, screen, ray_length=300):
        self.screen = screen
        self.rays = []
        self.ray_length = ray_length  # Maksimipituus säteille
        self.obstacles = []  # Lista esteille

    def set_obstacles(self, obstacles):
        """Asettaa esteet, joihin säteet voivat osua (odottaa pygame.Rect-listaa)."""
        self.obstacles = obstacles

    def update_rays(self, pos, angle):
        """Luo säteet pelaajan sijainnista."""
        self.rays = [Ray(pos, math.radians(a + angle - 45), self.ray_length) for a in fieldOfVision]

    def cast_rays(self):
        """Laskee säteiden loppupisteet ottaen huomioon suorakulmioesteet."""
        return [ray.cast(self.obstacles) for ray in self.rays]

    def draw(self, pos):
        """Piirtää säteet alkaen pelaajan sijainnista."""
        points = self.cast_rays()
        for point in points:
            pygame.draw.line(self.screen, (255, 255, 255), pos, point[1], 1)
            if len(point) > 2:
                for i in range(len(point)-2):
                    pygame.draw.line(self.screen, (255, 255, 255), point[i+1], point[i+2], 1)

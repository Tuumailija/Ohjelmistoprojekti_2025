from numpy import linspace
import pygame
import math
from .ray import Ray

rayNumber = (360//32)
fieldOfVision = linspace(0, 360/4, rayNumber)

class RayCaster:
    def __init__(self, screen, ray_length=300):
        self.screen = screen
        self.rays = []
        self.ray_length = ray_length  # Maksimipituus säteille
        self.obstacles = []  # Lista esteille
        self.valot = []
        self.cam_x = 0
        self.cam_y = 0

    def set_obstacles(self, obstacles):
        self.obstacles = [pygame.Rect(wall.x - self.cam_x, wall.y - self.cam_y, wall.width, wall.height) for wall in obstacles]

    def set_valot(self, valo_pos):
        self.valot = [valo_pos]

    def set_cam(self, x, y):
        self.cam_x = x
        self.cam_y = y

    def update_rays(self, pos, angle):
        """Luo säteet pelaajan sijainnista."""
        self.rays = [Ray(pos, math.radians(a + angle - 45), self.ray_length) for a in fieldOfVision]

    def cast_rays(self):
        """Laskee säteiden loppupisteet ottaen huomioon suorakulmioesteet."""
        return [ray.cast(self.obstacles) for ray in self.rays]

    def draw(self, pos):
        """Piirtää säteet alkaen pelaajan sijainnista."""
        ray_points = self.cast_rays()
        for points in ray_points:
            if points:
                for point in points:
                    pygame.draw.circle(self.screen, (255, 255, 0), point, 2)
                    pygame.draw.line(self.screen, (255, 255, 255), pos, point, 1)
                    if self.valot:
                        for light_pos in self.valot:
                            light_hit = Ray(point, 0, point.distance_to(light_pos)).cast_to_light(light_pos, self.obstacles)
                            pygame.draw.line(self.screen, (255, 255, 255), point, light_hit, 1)
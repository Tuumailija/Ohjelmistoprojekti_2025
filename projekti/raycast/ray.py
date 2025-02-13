import pygame
import math

class Ray:
    def __init__(self, pos, angle, ray_length):
        self.pos = pygame.Vector2(pos)
        self.dir = pygame.Vector2(math.cos(angle), math.sin(angle))
        self.ray_length = ray_length  # Säteen maksimipituus

    def cast(self, obstacles):
        closest = None
        min_dist = self.ray_length
        end_point = self.pos + self.dir * self.ray_length
        
        for wall in obstacles:
            x1, y1, x2, y2 = wall
            x3, y3 = self.pos
            x4, y4 = self.pos + self.dir * self.ray_length
            
            den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            if den == 0:
                continue
            
            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
            u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den
            
            if 0 < t < 1 and 0 < u < min_dist:
                pt = pygame.Vector2(x1 + t * (x2 - x1), y1 + t * (y2 - y1))
                dist = self.pos.distance_to(pt)
                if dist < min_dist:
                    min_dist = dist
                    closest = pt
        
        return closest if closest else end_point
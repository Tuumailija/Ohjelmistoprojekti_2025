import pygame
import math

class Ray:
    def __init__(self, pos, angle, ray_length):
        self.pos = pygame.Vector2(pos)
        self.dir = pygame.Vector2(math.cos(angle), math.sin(angle)).normalize()
        self.ray_length = ray_length  # Maksimipituus säteelle

    def cast(self, obstacles):
        points = [self.pos]
        ray_start = self.pos
        ray_dir = self.dir
        reflections = 0
        max_reflections = 3

        while reflections <= max_reflections:
            closest = None
            min_dist = self.ray_length
            ray_end = ray_start + ray_dir * self.ray_length

            for rect in obstacles:
                hit_point, normal = self.raycast_rect(ray_start, ray_end, rect)
                if hit_point and normal.length() > 0:
                    dist = ray_start.distance_to(hit_point)
                    if dist < min_dist:
                        min_dist = dist
                        closest = hit_point
                        hit_normal = normal

            if closest and hit_normal.length() > 0:
                points.append(closest)
                reflections += 1
                ray_dir = ray_dir.reflect(hit_normal).normalize()
                ray_start = closest + hit_normal * 1  # Siirrä törmäyspisteestä pois kunnolla
            else:
                points.append(ray_end)
                break

        return points

    def raycast_rect(self, start, end, rect):
        clipped = rect.clipline(start, end)
        if clipped:
            hit_start = pygame.Vector2(clipped[0])
            hit_end = pygame.Vector2(clipped[1])
            normal = self.get_normal(hit_start, rect)
            if start.distance_to(hit_start) < start.distance_to(hit_end):
                return hit_start, normal
            else:
                return hit_end, normal
        return None, None

    def get_normal(self, point, rect):
        epsilon = 1e-3
        #if abs(point.x - rect.left) < epsilon:
        #    print("Vasen seinä")
        #if abs(point.x - rect.right) < epsilon:
        #    print("Oikea seinä")
        #if abs(point.y - rect.top) < epsilon:
        #    print("Yläseinä")
        #if abs(point.y - rect.bottom) < epsilon:
        #    print("Alaseinä")

        #!!!!!! TÄSSÄ EHKÄ VÄÄRIN LISÄTYT (1) ARVOT, MUISTUTUS JOS EI YHTÄKKIÄ TOIMI !!!!!!
        if abs(point.x - rect.left) < epsilon: return pygame.Vector2(-1, 0)  # Vasen seinä
        if abs(point.x + 1 - rect.right) < epsilon: return pygame.Vector2(1, 0)  # Oikea seinä
        if abs(point.y - rect.top) < epsilon: return pygame.Vector2(0, -1)  # Yläseinä
        if abs(point.y + 1 - rect.bottom) < epsilon: return pygame.Vector2(0, 1)  # Alaseinä
        return pygame.Vector2(0, 0)
